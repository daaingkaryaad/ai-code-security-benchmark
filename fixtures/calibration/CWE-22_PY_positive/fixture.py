from pathlib import Path

def read_file(root, user_path):
    return (Path(root) / user_path).read_text(encoding="utf-8")
