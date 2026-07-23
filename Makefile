lint_flags = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs 
run_flag = index --max_chunk_size  600

install:
	@uv sync

run: 
	@uv run python3 -m src $(run_flag)

debug:
	@python3 -m pdb src/__main__.py

clean:
	@find . \
  \( -name '__pycache__' -o -name '.mypy_cache' \) \
  -type d -prune -exec rm -rf {} +  

lint:
	 flake8 src/. && mypy src/. $(lint_flags)
