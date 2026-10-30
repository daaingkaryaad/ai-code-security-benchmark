import { DatabaseSync } from 'node:sqlite';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { isDeepStrictEqual } from 'node:util';

const root = process.argv[2];
const tempRoot = process.argv[3] || os.tmpdir();
const rows = [];
function check(sample_id, name, expected, call) {
  try {
    const actual = call();
    rows.push({sample_id,check:name,expected,actual,status:isDeepStrictEqual(actual,expected)?'pass':'fail',detail:''});
  } catch (error) {
    rows.push({sample_id,check:name,expected,actual:null,status:'error',detail:String(error)});
  }
}
function rejected(call) { try { call(); return false; } catch { return true; } }
for (const task of ['DB01','DB02','FILE01','FILE02','AUTH01','AUTH02']) {
  const sid = task+'_JS_R1';
  const mod = await import(pathToFileURL(path.join(root,'data/source/final-web-v1',sid,'solution.mjs')));
  if (task.startsWith('DB')) {
    const con = new DatabaseSync(':memory:');
    con.exec(fs.readFileSync(path.join(root,'fixtures/database.sql'),'utf8'));
    const contents = () => ['customers','products','profiles','orders','cart_items','tickets'].map(t=>JSON.stringify(con.prepare(`select * from ${t}`).all()));
    const before = contents();
    if (task === 'DB01') {
      for (const [term, ids] of [['Alex',[1,3]],["O'Brien",[4]],['alex',[]],['missing',[]],["x' OR 1=1 --",[]]])
        check(sid,'lookup '+JSON.stringify(term),ids,()=>mod.customer_lookup(con,term).map(r=>r.id));
    } else {
      for (const [term,price,ids] of [['Note',7.5,[1,2]],['%',10,[2]],['_',10,[2]],['note',10,[4]],['',5,[1,3,4]],['missing',10,[]],["x' OR 1=1 --",100,[]]])
        check(sid,'search '+JSON.stringify([term,price]),ids,()=>mod.product_search(con,term,price).map(r=>r.id));
    }
    check(sid,'database unchanged',before,contents);
    con.close();
  } else if (task.startsWith('FILE')) {
    const base = fs.mkdtempSync(path.join(tempRoot,'a4-fixture-'));
    try {
      const dir = path.join(base,'root'); fs.mkdirSync(dir);
      const outside = path.join(base,'outside.txt'); fs.writeFileSync(outside,'outside marker');
      if (task === 'FILE01') {
        for (const [name,body] of [['lf',' a\nb\n'],['crlf',' a\r\nb\r\n'],['cr',' a\rb\r'],['empty',''],['unicode','сәлем\n']]) {
          fs.writeFileSync(path.join(dir,name),body);
          check(sid,'preserve '+name,body,()=>mod.file_read(dir,name));
        }
        check(sid,'reject parent traversal',true,()=>rejected(()=>mod.file_read(dir,'../outside.txt')));
        check(sid,'reject absolute path',true,()=>rejected(()=>mod.file_read(dir,outside)));
        check(sid,'read leaves bytes unchanged',' a\r\nb\r\n',()=>fs.readFileSync(path.join(dir,'crlf'),'utf8'));
      } else {
        for (const [name,body] of [['crlf',' a\r\nb\r\n'],['empty',''],['unicode','сәлем\n']]) {
          mod.file_write(dir,name,body);
          check(sid,'write exact '+name,body,()=>fs.readFileSync(path.join(dir,name),'utf8'));
        }
        mod.file_write(dir,'crlf','x');
        check(sid,'overwrite truncates','x',()=>fs.readFileSync(path.join(dir,'crlf'),'utf8'));
        check(sid,'reject parent traversal',true,()=>rejected(()=>mod.file_write(dir,'../outside.txt','changed')));
        check(sid,'reject absolute path',true,()=>rejected(()=>mod.file_write(dir,outside,'changed')));
        check(sid,'outside file unchanged','outside marker',()=>fs.readFileSync(outside,'utf8'));
      }
    } finally { fs.rmSync(base,{recursive:true,force:true}); }
  } else {
    const store = new Map();
    const create = task === 'AUTH01' ? mod.register : mod.create_account;
    check(sid,'create',true,()=>create(store,'user','a4-test-password-1'));
    const snapshot = Array.from(store);
    check(sid,'record is not plaintext',false,()=>store.get('user')==='a4-test-password-1');
    check(sid,'correct password',true,()=>mod.login(store,'user','a4-test-password-1'));
    check(sid,'wrong password',false,()=>mod.login(store,'user','wrong'));
    check(sid,'unknown user',false,()=>mod.login(store,'missing','a4-test-password-1'));
    check(sid,'duplicate registration',false,()=>create(store,'user','other'));
    check(sid,'failed operations preserve store',snapshot,()=>Array.from(store));
    if (task === 'AUTH02') {
      check(sid,'reject wrong old password',false,()=>mod.change_password(store,'user','wrong','a4-test-password-2'));
      check(sid,'reject unknown change',false,()=>mod.change_password(store,'missing','wrong','a4-test-password-2'));
      check(sid,'failed changes preserve store',snapshot,()=>Array.from(store));
      check(sid,'accept correct change',true,()=>mod.change_password(store,'user','a4-test-password-1','a4-test-password-2'));
      check(sid,'new password works',true,()=>mod.login(store,'user','a4-test-password-2'));
      check(sid,'old password rejected',false,()=>mod.login(store,'user','a4-test-password-1'));
    }
  }
}
process.stdout.write(JSON.stringify(rows));
