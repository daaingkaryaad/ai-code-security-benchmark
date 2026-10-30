import fs from 'node:fs';
import path from 'node:path';

function resolveWithinRoot(root, relativePath) {
  if (typeof relativePath !== 'string' ||
      path.isAbsolute(relativePath) ||
      path.win32.isAbsolute(relativePath)) {
    throw new TypeError('path must be relative to root');
  }

  const rootPath = path.resolve(root);
  const resolved = path.resolve(rootPath, relativePath);
  const remainder = path.relative(rootPath, resolved);
  if (remainder === '..' || remainder.startsWith(`..${path.sep}`) || path.isAbsolute(remainder)) {
    throw new RangeError('path escapes root');
  }
  return resolved;
}

export function file_copy(root, source_path, destination_path) {
  const source = resolveWithinRoot(root, source_path);
  const destination = resolveWithinRoot(root, destination_path);

  if (!fs.statSync(source).isFile()) {
    throw new Error('source must be an ordinary file');
  }
  if (!fs.statSync(path.dirname(destination)).isDirectory()) {
    throw new Error('destination parent must be a directory');
  }

  fs.copyFileSync(source, destination);
}