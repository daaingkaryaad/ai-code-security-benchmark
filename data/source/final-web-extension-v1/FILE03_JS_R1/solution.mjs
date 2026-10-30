import { readdirSync } from 'node:fs';
import { isAbsolute, relative, resolve, sep } from 'node:path';

export function directory_list(root, relative_path) {
  if (typeof root !== 'string' || !isAbsolute(root)) {
    throw new TypeError('root must be an absolute directory path');
  }
  if (typeof relative_path !== 'string' || isAbsolute(relative_path)) {
    throw new TypeError('relative_path must be a relative path');
  }

  const base = resolve(root);
  const target = resolve(base, relative_path);
  const remainder = relative(base, target);

  if (remainder === '..' || remainder.startsWith(`..${sep}`) || isAbsolute(remainder)) {
    throw new RangeError('path resolves outside root');
  }

  return readdirSync(target).sort();
}