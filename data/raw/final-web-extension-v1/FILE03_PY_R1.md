download solution.py

```
from pathlib import Pathdef directory_list(root: str, relative_path: str) -> list[str]:    relative = Path(relative_path)    if relative.is_absolute():        raise ValueError("relative_path must be relative")    root_path = Path(root).resolve()    target = (root_path / relative).resolve()    if not target.is_relative_to(root_path):        raise ValueError("path escapes root")    return sorted(entry.name for entry in target.iterdir())
```

the implementation uses only the python standard library, rejects absolute paths and paths escaping the root, returns immediate entry names in lexicographic order, and leaves the filesystem unchanged.