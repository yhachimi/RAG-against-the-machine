from typing import Any
from pathlib import Path

def codebase_reader(dir: str) -> list[dict[str: Any]]:
    root = Path(dir)
    codebase = []
    for file in root.rglob("*"):
        if file.suffix == ".py" or file.suffix == ".md":
            with open(file, "r") as f:
                content = f.read()
                codebase.append({"content": content, "file_path":file})

    return  codebase
    
