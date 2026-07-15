from pathlib import Path
from typing import Any


def codebase_reader(dir: str) -> list[dict[str, Any]]:
    """this functions is the first step  in the indexing part
        codebase reading method"""
    root = Path(dir)
    codebase = []
    for file in root.rglob("*"):
        if file.suffix == ".py" or file.suffix == ".md":
            with open(file, "r") as f:
                content = f.read()
                codebase.append({"content": content, "file_path": file})

    return codebase
