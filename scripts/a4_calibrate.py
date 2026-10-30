#!/usr/bin/env python3
"""scan all 24 controls and the original corpus; preserve separate new outputs.

run from the repository after copying in the additions. requires semgrep on PATH.
no source files or original scan outputs are changed.
"""
import argparse
import csv
import datetime as dt
import hashlib
import gzip
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request
import urllib.error

SCRIPT_VERSION = '1.1.0'


def identify_rule_document(body):
    """accept json or yaml rules; semgrep performs full schema validation."""
    try:
        text = body.decode('utf-8-sig').strip()
    except UnicodeDecodeError as exc:
        raise ValueError('the registry response is not utf-8 rules text') from exc
    if not text:
        raise ValueError('the registry returned an empty response')
    if text.startswith('<'):
        raise ValueError('the registry returned an html page instead of a rule file')
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        # the registry commonly serves yaml. do not require pyyaml in the
        # user's separate python installation: semgrep parses the saved file.
        if not re.search(r'(?m)^\s*(?:rules|"rules"|\'rules\')\s*:', text):
            raise ValueError('the response contains neither json nor a yaml rules mapping')
        return 'yaml', None
    if not isinstance(payload,dict) or not isinstance(payload.get('rules'),list) or not payload['rules']:
        raise ValueError('the json response does not contain a nonempty rules list')
    return 'json', len(payload['rules'])


def check_project(root, include_extension=False):
    required = ['fixtures/calibration/manifest.csv', 'protocol/final_schedule_18.csv']
    missing = [p for p in required if not (root/p).is_file()]
    sources = [p for p in (root/'data/source/final-web-v1').rglob('*')
               if p.is_file() and p.suffix in ['.py','.mjs','.java']]
    if missing or len(sources) != 18:
        raise ValueError(
            'this folder is not the complete research project (found '+str(len(sources))+
            ' original final source files; expected 18). copy the contents of a4_additions '
            'into the existing ai-code-security-benchmark folder, then run from that folder. '
            'alternatively use --repo with its full path. missing files: '+(', '.join(missing) or 'original generated sources'))
    if include_extension and not (root/'protocol/a4_collection_schedule_27.csv').is_file():
        raise ValueError('extension schedule missing from the selected project folder')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version',action='version',version='a4_calibrate '+SCRIPT_VERSION+' (json/yaml registry support)')
    ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--config', default='p/security-audit', help='original registry name or a frozen local rules file')
    ap.add_argument('--freeze-current-registry', action='store_true', help='save the current original-named registry pack before both new scans; does not recover historical rules')
    ap.add_argument('--out', type=Path)
    ap.add_argument('--include-extension',action='store_true',help='after collection, also require and scan all 27 extension sources')
    args = ap.parse_args()
    root = args.repo.resolve()
    try:
        check_project(root,args.include_extension)
    except ValueError as exc:
        print('setup error: '+str(exc),file=sys.stderr)
        return 2
    now = dt.datetime.now(dt.timezone.utc)
    out = (args.out or root/'data/processed'/('a4-calibration-'+now.strftime('%Y%m%dT%H%M%S%fZ'))).resolve()
    out.mkdir(parents=True, exist_ok=False)
    exe = shutil.which('semgrep')
    meta = {'recorded_utc':now.isoformat(), 'config':args.config,
            'instrument_version':SCRIPT_VERSION,
            'instrument_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'config_is_frozen':Path(args.config).is_file(), 'semgrep_executable':exe,
            'historical_semgrep_version':'1.182.0', 'runs':[]}
    if args.freeze_current_registry:
        if args.config != 'p/security-audit':
            raise ValueError('--freeze-current-registry is only for the original named ruleset')
        if not exe:
            meta['status'] = 'blocked: semgrep executable unavailable; no download or scan executed'
            (out/'run_record.json').write_text(json.dumps(meta,indent=2)+'\n')
            print(meta['status'])
            return 2
        url = 'https://semgrep.dev/c/p/security-audit'
        request=urllib.request.Request(url,headers={
            'Accept':'application/json, application/yaml, text/yaml, text/plain;q=0.9',
            'User-Agent':'rmt-a4-calibration/1.1'})
        try:
            with urllib.request.urlopen(request,timeout=60) as response:
                raw_body=response.read()
                meta['registry_http_content_type']=response.headers.get('Content-Type','')
                encoding=response.headers.get('Content-Encoding','').lower()
            (out/'registry_response.bin').write_bytes(raw_body)
            body=gzip.decompress(raw_body) if encoding=='gzip' else raw_body
            rule_format,rule_count=identify_rule_document(body)
        except (urllib.error.URLError,TimeoutError,OSError,ValueError) as exc:
            meta.update(status='blocked: rule download or format validation failed; no scan executed',
                        registry_url=url,download_error=str(exc))
            (out/'run_record.json').write_text(json.dumps(meta,indent=2)+'\n')
            print(meta['status']+'\n'+str(exc)+'\nresults folder: '+str(out),file=sys.stderr)
            return 2
        saved = out/('registry_snapshot.'+rule_format)
        saved.write_bytes(body)
        args.config = str(saved)
        meta.update(config_is_frozen=True, registry_url=url, registry_downloaded_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                    registry_format=rule_format,registry_rule_count=rule_count,
                    snapshot_validation='semgrep performs complete parsing and rule validation during both scans',
                    historical_rule_identity='unknown; this is a current snapshot, not the historical pack')
    if Path(args.config).is_file():
        config = Path(args.config).resolve()
        body = config.read_bytes()
        (out/'resolved_rules.yaml').write_bytes(body)
        meta['config_sha256'] = hashlib.sha256(body).hexdigest()
        config_arg = str(out/'resolved_rules.yaml')
    else:
        config_arg = args.config
        meta['rule_snapshot_limitation'] = 'registry contents are not frozen; cannot prove identity with historical rules'
    if not exe:
        meta['status'] = 'blocked: semgrep executable unavailable; no calibration scan executed'
        (out/'run_record.json').write_text(json.dumps(meta,indent=2)+'\n')
        print(meta['status'])
        return 2
    version = subprocess.run([exe,'--version'],capture_output=True,text=True,timeout=30)
    meta['version_stdout'] = version.stdout.strip()
    meta['version_stderr'] = version.stderr.strip()
    manifest = list(csv.DictReader((root/'fixtures/calibration/manifest.csv').open()))
    if len(manifest) != 24 or len({r['fixture_id'] for r in manifest}) != 24:
        raise ValueError('expected exactly 24 unique control cases')
    expected_cells = {(c,l,s) for c in ['CWE-89','CWE-22','CWE-256','CWE-798']
                      for l in ['PY','JAVA','JS'] for s in ['0','1']}
    if {(r['target_cwe'],r['language'],r['expected_positive']) for r in manifest} != expected_cells:
        raise ValueError('control design is unbalanced or labels invalid')
    for row in manifest:
        if hashlib.sha256((root/row['source_path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('fixture hash mismatch: '+row['fixture_id'])

    def normal(p):
        path = Path(p)
        if path.is_absolute():
            try: return path.relative_to(root).as_posix()
            except ValueError: return path.as_posix()
        return path.as_posix().removeprefix('./')

    expected_sources = {
        'calibration':{r['source_path'] for r in manifest},
        'final_r1':{str(p.relative_to(root)) for p in (root/'data/source/final-web-v1').rglob('*')
                    if p.is_file() and p.suffix in ['.py','.mjs','.java']}}
    if len(expected_sources['final_r1']) != 18:
        raise ValueError('expected exactly 18 archived r1 sources')
    targets=[('calibration','fixtures/calibration'), ('final_r1','data/source/final-web-v1')]
    if args.include_extension:
        entries=list(csv.DictReader((root/'protocol/a4_collection_schedule_27.csv').open()))
        expected_sources['extension']={r['source_path'] for r in entries}
        if len(expected_sources['extension'])!=27 or any(not (root/p).is_file() for p in expected_sources['extension']):
            raise ValueError('extension scan requires all 27 source files; missing attempts must be reported separately')
        targets.append(('extension','data/source/final-web-extension-v1'))
    results = {}
    for label, target in targets:
        jsonpath = out/(label+'_semgrep.json')
        command = [exe,'scan','--config='+config_arg,'--metrics=off','--json',
                   '--no-git-ignore','--output='+str(jsonpath),target]
        run = subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=600)
        (out/(label+'_stdout.txt')).write_text(run.stdout)
        (out/(label+'_stderr.txt')).write_text(run.stderr)
        record = {'label':label,'command':command,'returncode':run.returncode}
        if jsonpath.exists():
            try:
                payload = json.loads(jsonpath.read_text())
                if not isinstance(payload.get('results'),list) or not isinstance(payload.get('errors'),list):
                    raise ValueError('missing scan result or error list')
                record.update(alerts=len(payload['results']),errors=len(payload['errors']),
                              scanned_paths=len(payload.get('paths',{}).get('scanned',[])),version=payload.get('version'))
                observed_paths = {normal(p) for p in payload.get('paths',{}).get('scanned',[])}
                record['all_expected_paths_scanned'] = expected_sources[label] <= observed_paths
                record['missing_paths'] = sorted(expected_sources[label]-observed_paths)
                results[label] = payload
            except (ValueError,TypeError) as exc:
                record['json_error'] = str(exc)
        meta['runs'].append(record)

    calibration = results.get('calibration',{})
    scan_ok = bool(meta['runs'][0]['returncode'] == 0 and calibration and not calibration.get('errors'))
    scanned = {normal(p) for p in calibration.get('paths',{}).get('scanned',[])}
    verdicts = []
    for fixture in manifest:
        alerts = [a for a in calibration.get('results',[]) if normal(a.get('path','')) == fixture['source_path']]
        cwes = sorted({c for a in alerts for c in re.findall(r'CWE-\d+',json.dumps(a.get('extra',{}).get('metadata',{})))})
        # a hardcoded-password label (259) is a declared subtype match for 798.
        target_hit = fixture['target_cwe'] in cwes or (fixture['target_cwe']=='CWE-798' and 'CWE-259' in cwes)
        eligible = scan_ok and fixture['source_path'] in scanned
        expected = fixture['expected_positive']=='1'
        if not eligible:
            decision = 'not_evaluated'
        elif alerts and not target_hit:
            decision = 'review_needed'
        else:
            decision = ('TP' if target_hit else 'FN') if expected else ('FP' if target_hit else 'TN')
        verdicts.append({**fixture,'scan_valid':eligible,'any_alert_count':len(alerts),
                         'reported_cwes':';'.join(cwes),'target_label_hit':target_hit,
                         'candidate_classification':decision,
                         'rule_ids':';'.join(a.get('check_id','') for a in alerts)})
    with (out/'calibration_outcomes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=verdicts[0]);w.writeheader();w.writerows(verdicts)
    summary = {'mapping':'target CWE metadata; CWE-259 also matches target CWE-798; unclassified/other-CWE alerts need review',
               'scope':'candidate label agreement on these authored controls; no general scanner accuracy claim',
               'groups':[]}
    for cwe in ['CWE-89','CWE-22','CWE-256','CWE-798']:
        subset=[v for v in verdicts if v['target_cwe']==cwe]
        counts={s:sum(v['candidate_classification']==s for v in subset)
                for s in ['TP','FN','TN','FP','review_needed','not_evaluated']}
        # fractions exist only if all 6 cases are evaluated and automatically classifiable.
        complete = counts['review_needed']==0 and counts['not_evaluated']==0
        summary['groups'].append({'cwe':cwe,**counts,
            'candidate_sensitivity':counts['TP']/(counts['TP']+counts['FN']) if complete else None,
            'candidate_specificity':counts['TN']/(counts['TN']+counts['FP']) if complete else None})
    meta['status']='complete scan session' if all(r['returncode']==0 and r.get('errors')==0 and r.get('all_expected_paths_scanned') for r in meta['runs']) else 'incomplete scan session; inspect errors or missing paths'
    (out/'run_record.json').write_text(json.dumps(meta,indent=2)+'\n')
    (out/'calibration_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'output':str(out),'status':meta['status'],'calibration':summary}))
    return 0 if meta['status']=='complete scan session' else 2


if __name__=='__main__':
    raise SystemExit(main())
