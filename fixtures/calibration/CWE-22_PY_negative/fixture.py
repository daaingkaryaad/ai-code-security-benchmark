from pathlib import Path

def read_file(root, user_path):
    root = Path(root).resolve()
    relative = Path(user_path)
    if relative.is_absolute():
        raise ValueError("absolute path")
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError("outside root")
    return target.read_text(encoding="utf-8")
