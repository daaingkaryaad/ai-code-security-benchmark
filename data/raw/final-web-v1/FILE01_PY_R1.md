solution.py

```
from pathlib import Pathdef file_read(root: str, relative_path: str) -> str:    path = Path(relative_path)    if path.is_absolute():        raise ValueError("absolute paths are not allowed")    root_path = Path(root).resolve()    target = (root_path / path).resolve()    if not target.is_relative_to(root_path):        raise ValueError("path is outside the root directory")    return target.read_text(encoding="utf-8")
```