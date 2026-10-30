from pathlib import Path


def directory_list(root: str, relative_path: str) -> list[str]:
    relative = Path(relative_path)
    if relative.is_absolute():
        raise ValueError("relative_path must be relative")

    root_path = Path(root).resolve()
    target = (root_path / relative).resolve()
    if not target.is_relative_to(root_path):
        raise ValueError("path escapes root")

    return sorted(entry.name for entry in target.iterdir())