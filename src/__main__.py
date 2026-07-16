from pathlib import Path

from .codebase_reader import (codebase_reader, markdown_chunker,
                              python_code_chunker)

RED = '\033[0;31m'
RESET = '\033[1;37m'
BLUE = "\033[34m"
GREEN = "\033[92m"
GRAY = '\033[37m'


def main() -> None:
    """the main functions where the code starts"""
    all_chunks = []
    code_base = codebase_reader("vllm-0.10.1")
    for document in code_base:
        suffix = Path(document["file_path"]).suffix
        if suffix == ".py":
            chunked = python_code_chunker(document)
            if chunked:
                all_chunks.extend(chunked)
        elif suffix == ".md":
            chunked = markdown_chunker(document)
            all_chunks.extend(chunked)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{RED}{e}{RESET}")
