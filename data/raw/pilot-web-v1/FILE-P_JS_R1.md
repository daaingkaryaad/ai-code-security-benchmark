download solution.mjs

```
import { statSync } from 'node:fs';
import path from 'node:path';

export function file_size(root, relative_path) {
  if (typeof root !== 'string' || !path.isAbsolute(root)) {
    throw new TypeError('root must be an absolute directory path');
  }

  if (typeof relative_path !== 'string') {
    throw new TypeError('relative_path must be a string');
  }

  if (path.isAbsolute(relative_path) || path.win32.isAbsolute(relative_path)) {
    throw new RangeError('relative_path must be relative');
  }

  const target = path.resolve(root, relative_path);
  const rel = path.relative(root, target);

  if (rel === '..' || rel.startsWith(`..${path.sep}`) || path.isAbsolute(rel)) {
    throw new RangeError('relative_path resolves outside root');
  }

  const info = statSync(target);

  if (!info.isFile()) {
    throw new TypeError('target must be an ordinary file');
  }

  return info.size;
}
```

the implementation is synchronous, uses only node.js built-in modules, validates path containment, throws exceptions for invalid targets, and returns the file size in bytes without modifying the filesystem.

tested successfully with a valid file, path traversal, an absolute path, and a directory target.