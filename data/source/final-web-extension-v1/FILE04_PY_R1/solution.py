from pathlib import Path
import shutil


def file_copy(root: str, source_path: str, destination_path: str) -> None:
    base = Path(root).resolve()

    def confined(path: str) -> Path:
        relative = Path(path)
        if relative.is_absolute():
            raise ValueError("absolute paths are not allowed")
        resolved = (base / relative).resolve()
        if not resolved.is_relative_to(base):
            raise ValueError("path escapes root")
        return resolved

    source = confined(source_path)
    destination = confined(destination_path)

    if not source.is_file():
        raise ValueError("source must be an ordinary file")
    if not destination.parent.is_dir():
        raise NotADirectoryError(destination.parent)

    shutil.copyfile(source, destination)