from pathlib import Path
from typing import Any


def codebase_reader(dir: str) -> list[dict[str, Any]]:
    """this functions is the first step  in the indexing part
        codebase reading method"""
    root = Path(dir)
    codebase = []
    for file in root.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix in {".py", ".md"}:
            content = file.read_text(encoding="utf-8", errors="ignore")
            codebase.append({"content": content, "file_path": str(file)})

    return codebase
