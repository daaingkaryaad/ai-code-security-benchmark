#!/usr/bin/env python3
"""Manual ChatGPT web collector for the fixed 18-slot final schedule on macOS.

Usage, from repository root:
  python3 scripts/web18.py next
  python3 scripts/web18.py code
  python3 scripts/web18.py raw
  python3 scripts/web18.py status

No API key, no model automation, and no overwriting existing research outputs.
"""
import csv
import datetime as dt
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE = ROOT / 'protocol' / 'final_schedule_18.csv'
SOURCE = ROOT / 'data' / 'source' / 'final-web-v1'
RAW = ROOT / 'data' / 'raw' / 'final-web-v1'
LOG = ROOT / 'logs' / 'final-web-v1' / 'collection_events.csv'
EXTS = {'PY': 'solution.py', 'JS': 'solution.mjs', 'JAVA': 'Solution.java'}


def rows():
    with SCHEDULE.open(newline='', encoding='utf-8') as file:
        entries = list(csv.DictReader(file))
    assert len(entries) == 18, 'expected exactly 18 final slots'
    assert len({row['sample_id'] for row in entries}) == 18, 'duplicate sample identifiers'
    assert all(row['repetition'] == '1' for row in entries)
    assert {r['task_id'] for r in entries} == {'DB01','DB02','FILE01','FILE02','AUTH01','AUTH02'}
    assert {r['language'] for r in entries} == {'PY','JS','JAVA'}
    for r in entries:
        prompt = ROOT / r['prompt_path']
        assert prompt.is_file(), f'missing prompt: {prompt}'
    return entries


def paths(r):
    return SOURCE / r['sample_id'] / EXTS[r['language']], RAW / (r['sample_id'] + '.md')


def pending(entries):
    for r in entries:
        a,b=paths(r)
        if not (a.is_file() and a.stat().st_size and b.is_file() and b.stat().st_size):
            return r
    return None


def clipboard():
    proc = subprocess.run(['pbpaste'],capture_output=True,check=True)
    if not proc.stdout.strip():
        sys.exit('empty clipboard: copy the response first')
    return proc.stdout


def record(r, event, path, body):
    LOG.parent.mkdir(parents=True,exist_ok=True)
    make_header = not LOG.exists()
    with LOG.open('a',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        if make_header:
            w.writerow(['recorded_utc','sample_id','event','path','sha256','displayed_model','thinking','interface'])
        w.writerow([dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),r['sample_id'],event,str(path.relative_to(ROOT)),hashlib.sha256(body).hexdigest(),'gpt-6','medium','chatgpt web'])


def main():
    entries=rows()
    op=sys.argv[1] if len(sys.argv)>1 else 'next'
    if op=='status':
        complete=sum(all(p.is_file() and p.stat().st_size>0 for p in paths(r)) for r in entries)
        code=sum(paths(r)[0].is_file() for r in entries)
        raw=sum(paths(r)[1].is_file() for r in entries)
        print(f'completed pairs: {complete}/18; source files: {code}/18; raw response files: {raw}/18')
        return
    if op not in ('next','code','raw'):
        sys.exit('usage: python3 scripts/web18.py [next|code|raw|status]')
    r=pending(entries)
    if r is None:
        print('all 18 final samples have source and response files. verify content and metadata before assessment.')
        return
    src,raw=paths(r)
    if op=='next':
        prompt = ROOT / r['prompt_path']
        subprocess.run(['pbcopy'],input=prompt.read_bytes(),check=True)
        print('next:',r['sample_id'],'| copied prompt:',r['prompt_path'])
        print('source:',src.relative_to(ROOT),'exists:',src.exists())
        print('raw:',raw.relative_to(ROOT),'exists:',raw.exists())
        return
    path=src if op=='code' else raw
    if path.exists():
        sys.exit('will not overwrite existing file: '+str(path.relative_to(ROOT)))
    body=clipboard()
    if op=='code' and body.strip().startswith(b'```'):
        sys.exit('clipboard begins with a markdown fence. copy only the generated code block.')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(body)
    record(r,'source_saved' if op=='code' else 'raw_saved',path,body)
    print('saved',path.relative_to(ROOT),f'({len(body)} bytes)')
    if op=='raw':
        print('if the web copy omitted an attached code file, retain the screenshot and code separately.')


if __name__=='__main__':
    main()
