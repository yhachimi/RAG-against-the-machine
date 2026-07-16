from pathlib import Path

from .codebase_reader import codebase_reader, python_code_chunker


def main() -> None:
    """the main functions where the code starts"""
    chunked_python_code = []
    code_base = codebase_reader("vllm-0.10.1")
    for document in code_base:
        suffix = Path(document["file_path"]).suffix
        if suffix == ".py":
            chunked = python_code_chunker(document)
            if chunked:
                chunked_python_code.extend(chunked)
        elif suffix == ".md":
            continue


if __name__ == "__main__":
    main()
