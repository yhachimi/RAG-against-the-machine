from .codebase_reader import codebase_reader



data = codebase_reader("vllm-0.10.1")
for d in data:
    print(d["file_path"])

