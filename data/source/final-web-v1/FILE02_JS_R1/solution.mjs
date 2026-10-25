
import fs from 'node:fs';
import path from 'node:path';

export function file_write(root, relative_path, content) {
  if (path.isAbsolute(relative_path)) {
    throw new Error('absolute paths are not allowed');
  }

  const resolvedRoot = path.resolve(root);
  const targetPath = path.resolve(resolvedRoot, relative_path);
  const relative = path.relative(resolvedRoot, targetPath);

  if (
    relative === '..' ||
    relative.startsWith('..' + path.sep) ||
    path.isAbsolute(relative)
  ) {
    throw new Error('path escapes the root directory');
  }

  fs.writeFileSync(targetPath, content, { encoding: 'utf8' });
}
