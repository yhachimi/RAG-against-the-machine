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
    """move the python code into chunks using the ast  model"""
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
                "title": "__imports__",
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
            data["title"] = node.name
            start = node.lineno - 1
            if node.end_lineno is None:
                continue
            end = node.end_lineno
            data["type"] = type(node).__name__
            data["content"] = "\n".join(lines[start: end])
            data["start"] = start
            data["end"] = end
            data["file_path"] = python_code["file_path"]
            result.append(data)

    return result


def markdown_chunker(markdown: dict[str, str]) -> list[dict[str, Any]]:
    content = markdown["content"]
    lines = content.splitlines()
    current_title = "__intro__"
    current_lines: list[str] = []
    sections = []
    start = 1
    for lineno, line in enumerate(lines, start=1):
        if line.startswith("#"):
            if current_title:
                sections.append(
                    {"title": current_title,
                     "type": "markdown_section",
                     "content": "\n".join(current_lines),
                     "file_path": markdown["file_path"],
                     "start": start,
                     "end": lineno - 1},)

            current_title = line.lstrip("# ").strip()
            start = lineno
            current_lines = []
        else:
            current_lines.append(line)
    sections.append(
        {
            "type": "markdown_section",
            "title": current_title,
            "content": "\n".join(current_lines),
            "file_path": markdown["file_path"],
            "start": start,
            "end": len(lines)
        }
    )
    return sections
