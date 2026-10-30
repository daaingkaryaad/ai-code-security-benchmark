#!/usr/bin/env python3
"""run bounded local checks on the archived python and javascript r1 sources.

the java rows are explicitly untested. all writes use temporary fixtures.
this is a declared additional instrument, not a substitute for cwe review.
"""
import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import sqlite3
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    root = args.repo.resolve()
    stamp = dt.datetime.now(dt.timezone.utc)
    out = args.out or root / 'data/processed' / ('a4-audit-' + stamp.strftime('%Y%m%dT%H%M%SZ'))
    out.mkdir(parents=True, exist_ok=False)
    work = out.resolve() / 'work'
    work.mkdir()
    rows = []

    def check(sid, name, expected, call):
        try:
            actual = call()
            status = 'pass' if actual == expected else 'fail'
            detail = ''
        except Exception as exc:
            actual, status, detail = None, 'error', type(exc).__name__ + ': ' + str(exc)
        rows.append(dict(sample_id=sid, check=name, expected=expected,
                         actual=actual, status=status, detail=detail))

    def rejected(call):
        try:
            call()
        except Exception:
            return True
        return False

    for task in ['DB01', 'DB02', 'FILE01', 'FILE02', 'AUTH01', 'AUTH02']:
        sid = task + '_PY_R1'
        source = root / 'data/source/final-web-v1' / sid / 'solution.py'
        spec = importlib.util.spec_from_file_location(sid, source)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if task.startswith('DB'):
            con = sqlite3.connect(':memory:')
            con.executescript((root / 'fixtures/database.sql').read_text())
            before = list(con.iterdump())
            if task == 'DB01':
                for term, expected_ids in [('Alex', [1, 3]), ("O'Brien", [4]),
                                           ('alex', []), ('missing', []),
                                           ("x' OR 1=1 --", [])]:
                    check(sid, 'lookup ' + repr(term), expected_ids,
                          lambda term=term: [r['id'] for r in mod.customer_lookup(con, term)])
            else:
                for term, price, expected_ids in [('Note', 7.5, [1, 2]), ('%', 10, [2]),
                                                 ('_', 10, [2]), ('note', 10, [4]),
                                                 ('', 5, [1, 3, 4]), ('missing', 10, []),
                                                 ("x' OR 1=1 --", 100, [])]:
                    check(sid, 'search ' + repr((term, price)), expected_ids,
                          lambda term=term, price=price: [r['id'] for r in mod.product_search(con, term, price)])
            check(sid, 'database unchanged', before, lambda: list(con.iterdump()))
            con.close()
        elif task.startswith('FILE'):
            with tempfile.TemporaryDirectory(prefix='a4-fixture-', dir=work) as folder:
                base = Path(folder)
                target_root = base / 'root'
                target_root.mkdir()
                outside = base / 'outside.txt'
                outside.write_text('outside marker')
                if task == 'FILE01':
                    for name, body in [('lf', b' a\nb\n'), ('crlf', b' a\r\nb\r\n'),
                                       ('cr', b' a\rb\r'), ('empty', b''),
                                       ('unicode', 'сәлем\n'.encode())]:
                        (target_root / name).write_bytes(body)
                        check(sid, 'preserve ' + name, body.decode(),
                              lambda name=name: mod.file_read(str(target_root), name))
                    check(sid, 'reject parent traversal', True,
                          lambda: rejected(lambda: mod.file_read(str(target_root), '../outside.txt')))
                    check(sid, 'reject absolute path', True,
                          lambda: rejected(lambda: mod.file_read(str(target_root), str(outside))))
                    check(sid, 'read leaves bytes unchanged', b' a\r\nb\r\n',
                          lambda: (target_root / 'crlf').read_bytes())
                else:
                    for name, body in [('crlf', ' a\r\nb\r\n'), ('empty', ''), ('unicode', 'сәлем\n')]:
                        mod.file_write(str(target_root), name, body)
                        check(sid, 'write exact ' + name, body.encode(),
                              lambda name=name: (target_root / name).read_bytes())
                    mod.file_write(str(target_root), 'crlf', 'x')
                    check(sid, 'overwrite truncates', b'x', lambda: (target_root / 'crlf').read_bytes())
                    check(sid, 'reject parent traversal', True,
                          lambda: rejected(lambda: mod.file_write(str(target_root), '../outside.txt', 'changed')))
                    check(sid, 'reject absolute path', True,
                          lambda: rejected(lambda: mod.file_write(str(target_root), str(outside), 'changed')))
                    check(sid, 'outside file unchanged', 'outside marker', outside.read_text)
        else:
            store = {}
            create = mod.register if task == 'AUTH01' else mod.create_account
            check(sid, 'create', True, lambda: create(store, 'user', 'a4-test-password-1'))
            snapshot = dict(store)
            check(sid, 'record is not plaintext', False, lambda: store['user'] == 'a4-test-password-1')
            check(sid, 'correct password', True, lambda: mod.login(store, 'user', 'a4-test-password-1'))
            check(sid, 'wrong password', False, lambda: mod.login(store, 'user', 'wrong'))
            check(sid, 'unknown user', False, lambda: mod.login(store, 'missing', 'a4-test-password-1'))
            check(sid, 'duplicate registration', False, lambda: create(store, 'user', 'other'))
            check(sid, 'failed operations preserve store', snapshot, lambda: dict(store))
            if task == 'AUTH02':
                check(sid, 'reject wrong old password', False,
                      lambda: mod.change_password(store, 'user', 'wrong', 'a4-test-password-2'))
                check(sid, 'reject unknown change', False,
                      lambda: mod.change_password(store, 'missing', 'wrong', 'a4-test-password-2'))
                check(sid, 'failed changes preserve store', snapshot, lambda: dict(store))
                check(sid, 'accept correct change', True,
                      lambda: mod.change_password(store, 'user', 'a4-test-password-1', 'a4-test-password-2'))
                check(sid, 'new password works', True, lambda: mod.login(store, 'user', 'a4-test-password-2'))
                check(sid, 'old password rejected', False, lambda: mod.login(store, 'user', 'a4-test-password-1'))

    node = shutil.which('node')
    js_instrument = Path(__file__).with_suffix('.mjs')
    node_run = subprocess.run([node, str(js_instrument), str(root), str(work)], capture_output=True, text=True, timeout=60) if node else None
    if node_run:
        (out / 'node_stdout.txt').write_text(node_run.stdout)
        (out / 'node_stderr.txt').write_text(node_run.stderr)
    if node_run and node_run.returncode == 0:
        rows.extend(json.loads(node_run.stdout))
    else:
        for task in ['DB01', 'DB02', 'FILE01', 'FILE02', 'AUTH01', 'AUTH02']:
            rows.append(dict(sample_id=task+'_JS_R1', check='javascript suite', expected=None,
                             actual=None, status='not_tested', detail='node suite unavailable or failed; inspect logs'))
    for task in ['DB01', 'DB02', 'FILE01', 'FILE02', 'AUTH01', 'AUTH02']:
        rows.append(dict(sample_id=task+'_JAVA_R1', check='java functional suite', expected=None,
                         actual=None, status='not_tested', detail='this instrument does not implement java execution'))
    work.rmdir()

    def encode(x):
        if isinstance(x, bytes):
            return {'bytes_hex': x.hex()}
        return x

    rows = json.loads(json.dumps(rows, default=encode, ensure_ascii=False))
    source_hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted((root/'data/source/final-web-v1').rglob('*'))
                     if p.is_file() and p.suffix in ['.py', '.mjs', '.java']}
    counts = {status: sum(r['status'] == status for r in rows)
              for status in ['pass', 'fail', 'error', 'not_tested']}
    result = {'recorded_utc': stamp.isoformat(), 'instrument': 'a4_functional_audit v1',
              'scope': 'archived python and javascript r1 only; java explicitly untested; synthetic local fixtures',
              'versions': {'python': sys.version, 'node': subprocess.run([node, '--version'], capture_output=True, text=True).stdout.strip() if node else None},
              'platform': platform.platform(), 'machine': platform.machine(),
              'instrument_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), js_instrument]},
              'database_fixture_sha256': hashlib.sha256((root/'fixtures/database.sql').read_bytes()).hexdigest(),
              'source_sha256': source_hashes, 'counts': counts, 'checks': rows}
    (out / 'functional_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    with (out / 'functional_checks.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['sample_id','check','expected','actual','status','detail'])
        w.writeheader()
        for row in rows:
            w.writerow({**row, 'expected':json.dumps(row['expected'],ensure_ascii=False),
                        'actual':json.dumps(row['actual'],ensure_ascii=False)})
    print(json.dumps({'output':str(out), 'counts':counts}))


if __name__ == '__main__':
    main()
