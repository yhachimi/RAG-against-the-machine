import ast
from pathlib import Path
from typing import Any


def codebase_reader(directory: str) -> list[dict[str, Any]]:
    """this functions is the first step  in the indexing part
        codebase reading method"""
    root = Path(directory)
    codebase = []
    for file in root.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix in {".py", ".md"}:
            content = file.read_text(encoding="utf-8", errors="ignore")
            codebase.append({"content": content, "file_path": str(file)})

    return codebase


def python_code_chunker(python_code: dict[str, str]) -> list[dict[str, Any]]:
    try:
        tree = ast.parse(python_code["content"])
    except SyntaxError:
        return []
    result = []
    imports: str = ""
    content = python_code["content"]
    lines = content.splitlines()
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports += ast.unparse(node) + "\n"

    if imports:
        result.append(
            {
                "type": "imports",
                "file_path": python_code["file_path"],
                "name": "__imports__",
                "content": imports,
                "start": 0,
                "end": 0, })
    for node in tree.body:
        if isinstance(
            node,
            (ast.FunctionDef,
             ast.AsyncFunctionDef,
             ast.ClassDef)):
            data: dict[str, Any] = {}
            data["name"] = node.name
            start = node.lineno - 1
            end = node.end_lineno
            data["type"] = type(node).__name__
            data["content"] = "\n".join(lines[start: end])
            data["start"] = start
            data["end"] = end
            data["file_path"] = python_code["file_path"]
            result.append(data)

    return result
