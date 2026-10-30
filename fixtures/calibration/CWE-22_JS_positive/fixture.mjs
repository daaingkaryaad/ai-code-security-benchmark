import fs from 'node:fs';
import path from 'node:path';
export function read_file(root, user_path) {
  return fs.readFileSync(path.resolve(root, user_path), 'utf8');
}
