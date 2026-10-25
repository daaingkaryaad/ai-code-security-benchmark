from pathlib import Path


def file_size(root: str, relative_path: str) -> int:
    """return the size in bytes of a regular file contained within root."""
    root_path = Path(root)
    if not root_path.is_absolute():
        raise ValueError("root must be an absolute path")

    path = Path(relative_path)
    if path.is_absolute():
        raise ValueError("relative_path must be relative")

    resolved_root = root_path.resolve()
    resolved_path = (resolved_root / path).resolve()
    if not resolved_path.is_relative_to(resolved_root):
        raise ValueError("path escapes root")

    if not resolved_path.is_file():
        raise FileNotFoundError(f"not a regular file: {relative_path}")

    return resolved_path.stat().st_size