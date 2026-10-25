`solution.mjs`

```

import { readFileSync } from 'node:fs';
import { isAbsolute, relative, resolve } from 'node:path';

export function file_read(root, relative_path) {
  if (isAbsolute(relative_path)) {
    throw new Error('absolute paths are not allowed');
  }

  const rootPath = resolve(root);
  const filePath = resolve(rootPath, relative_path);
  const rel = relative(rootPath, filePath);

  if (
    rel === '..' ||
    rel.startsWith(`..${process.platform === 'win32' ? '\\' : '/'}`) ||
    isAbsolute(rel)
  ) {
    throw new Error('path escapes root directory');
  }

  return readFileSync(filePath, 'utf8');
}

```

the function synchronously reads the complete file as utf-8, preserves whitespace and line endings, rejects absolute paths and directory traversal outside `root`, and propagates filesystem errors without modifying files.