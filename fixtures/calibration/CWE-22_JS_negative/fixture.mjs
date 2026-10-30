import fs from 'node:fs';
import path from 'node:path';
export function read_file(root, user_path) {
  if (path.isAbsolute(user_path)) throw new Error('absolute path');
  const target = path.resolve(root, user_path);
  const rel = path.relative(path.resolve(root), target);
  if (rel === '..' || rel.startsWith('..' + path.sep) || path.isAbsolute(rel)) throw new Error('outside root');
  return fs.readFileSync(target, 'utf8');
}
