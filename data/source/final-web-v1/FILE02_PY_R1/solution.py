
from pathlib import Path


def file_write(root: str, relative_path: str, content: str) -> None:
    root_path = Path(root).resolve()
    path = Path(relative_path)

    if path.is_absolute():
        raise ValueError("absolute paths are not allowed")

    target = (root_path / path).resolve()

    if not target.is_relative_to(root_path):
        raise ValueError("path escapes the root directory")

    with target.open("w", encoding="utf-8", newline="") as file:
        file.write(content)
