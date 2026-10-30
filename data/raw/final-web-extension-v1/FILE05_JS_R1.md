`solution.mjs`

```

import fs from 'node:fs';
import path from 'node:path';

export function file_delete(root, relative_path) {
    if (path.isAbsolute(relative_path)) {
        throw new Error('absolute paths are not allowed');
    }

    const rootPath = path.resolve(root);
    const targetPath = path.resolve(rootPath, relative_path);
    const relative = path.relative(rootPath, targetPath);

    if (
        relative === '..' ||
        relative.startsWith('..' + path.sep) ||
        path.isAbsolute(relative)
    ) {
        throw new Error('path is outside root');
    }

    let stats;

    try {
        stats = fs.statSync(targetPath);
    } catch (err) {
        if (err.code === 'ENOENT') {
            return false;
        }
        throw err;
    }

    if (!stats.isFile()) {
        throw new Error('target is not an ordinary file');
    }

    fs.unlinkSync(targetPath);
    return true;
}

```