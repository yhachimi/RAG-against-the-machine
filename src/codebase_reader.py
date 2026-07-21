import ast
from pathlib import Path
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .models import Chunk


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


def metdata_solver(chunks: list[str], chunk: Chunk) -> list[Chunk]:
    current_offset = 0
    res: list[Chunk] = []
    data: dict[str, Any] = {}
    data["file_path"] = chunk.file_path
    data["type"] = chunk.type
    data["title"] = chunk.title
    data["id"] = chunk.id
    for piece in chunks:
        start = chunk.content.find(piece, current_offset)
        end = start + len(piece) - 1
        current_offset = end + 1
        data["content"] = piece
        data["first_character_index"] = chunk.first_character_index + start
        data["last_character_index"] = chunk.first_character_index + end
        data["start"] = chunk.start
        data["end"] = chunk.end
        res.append(Chunk(**data))
    return res


def split_chunks(all_chunks: list[Chunk], chunk_size: int) -> list[Chunk]:
    new_chunks: list[Chunk] = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    for chunk in all_chunks:
        if len(chunk.content) <= chunk_size:
            new_chunks.append(chunk)

        else:
            chunks = splitter.split_text(chunk.content)
            content = ""
            for c in chunks:
                if len(content + c) > chunk_size:
                    break
                content += c
                chunks.remove(c)
            chunks.append(content)
            new_chunks.extend(metdata_solver(chunks, chunk))

    return new_chunks


def python_code_chunker(python_code: dict[str, str]) -> list[Chunk]:
    """move the python code into chunks using the ast  model"""
    try:
        tree = ast.parse(python_code["content"])
    except SyntaxError:
        return []
    result: list[Chunk] = []
    imports: str = ""
    content = python_code["content"]
    lines = content.splitlines(keepends=True)
    offset = 0
    line_offsets = []
    for line in lines:
        line_offsets.append(offset)
        offset += len(line)
    all_imports = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            all_imports.append(node)
            imports += ast.unparse(node) + "\n"

    if imports:
        first_import = all_imports[0]
        last_import = all_imports[-1]
        if last_import.end_lineno is None:
            return result
        imp: dict[str, Any] = {"type": "imports",
                               "file_path": python_code["file_path"],
                               "title": "__imports__",
                               "content": imports,
                               "start": first_import.lineno - 1,
                               "end": last_import.end_lineno - 1,
                               "id": 0}
        start = imp["start"]
        end = imp["end"]
        imp["first_character_index"] = line_offsets[start]
        imp["last_character_index"] = line_offsets[end] + len(lines[end]) - 1

        result.append(Chunk(**imp))
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
            data["content"] = "".join(lines[start: end])
            data["start"] = start
            data["end"] = end
            data["file_path"] = python_code["file_path"]
            data["id"] = 0
            data["first_character_index"] = line_offsets[start]
            data["last_character_index"] = line_offsets[end - 1] + \
                len(lines[end - 1]) - 1
            result.append(Chunk(**data))

    return result


def markdown_chunker(markdown: dict[str, str]) -> list[Chunk]:
    content = markdown["content"]
    lines = content.splitlines(keepends=True)
    current_title = "__intro__"
    current_lines: list[str] = []
    sections = []
    offset = 0
    lines_offsets = []
    for line in lines:
        lines_offsets.append(offset)
        offset += len(line)

    start = 0
    for lineno, line in enumerate(lines, start=0):
        if line.startswith("#"):
            if current_title:
                section: dict[str, Any] = {
                    "title": current_title,
                    "type": "markdown_section",
                    "content": "".join(current_lines),
                    "file_path": markdown["file_path"],
                    "start": start,
                    "end": lineno - 1,
                    "id": 0}
                lc = lines_offsets[lineno - 1] + len(lines[lineno - 1]) - 1
                section["first_character_index"] = lines_offsets[start]
                section["last_character_index"] = lc
                sections.append(Chunk(**section))

            current_title = line.lstrip("# ").strip()
            start = lineno
            current_lines = []
        else:
            current_lines.append(line)
    section = {
        "type": "markdown_section",
        "title": current_title,
        "content": "\n".join(current_lines),
        "file_path": markdown["file_path"],
        "start": start,
        "end": len(lines),
        "id": 0,
    }
    section["first_character_index"] = lines_offsets[section["start"]]
    section["last_character_index"] = lines_offsets[len(
        lines) - 1] + len(lines[len(lines) - 1]) - 1
    sections.append(Chunk(**section))
    return sections
