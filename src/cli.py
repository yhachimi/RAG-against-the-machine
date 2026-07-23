from pathlib import Path

from .codebase_reader import (codebase_reader, markdown_chunker,
                              python_code_chunker, split_chunks)
from .models import BM25_DATA, Chunk
from .tokenization import (calc_docs_lenghts, document_frequency,
                           inverse_docs_frequency, tokens_genrate)


class Rag:
    def index(self, max_chunk_size: int = 2000) -> None:
        """this methode is represonting the indexing part
        markdown  and python code chunking chunks indexing
        and calc the bm25 needed data like idf and df"""
        self.all_chunks: list[Chunk] = []
        code_base = codebase_reader("vllm-0.10.1")
        for document in code_base:
            suffix = Path(document["file_path"]).suffix
            if suffix == ".py":
                chunked = python_code_chunker(document)
                if chunked:
                    self.all_chunks.extend(chunked)
            elif suffix == ".md":
                chunked = markdown_chunker(document)
                self.all_chunks.extend(chunked)

        for chunk_id, chunk in enumerate(self.all_chunks):
            chunk.id = chunk_id
        self.all_chunks = split_chunks(self.all_chunks, max_chunk_size)
        for chunk_id, chunk in enumerate(self.all_chunks):
            chunk.id = chunk_id

        all_tokens = tokens_genrate(self.all_chunks)
        all_docs_lenghts = calc_docs_lenghts(all_tokens)
        avg_doc_lenght = sum(all_docs_lenghts) / len(all_docs_lenghts)
        documnts_frequency: dict[str, int] = document_frequency(all_tokens)
        idf: dict[str, float] = inverse_docs_frequency(
            documnts_frequency, len(self.all_chunks))
        self.bm25_data = BM25_DATA(
            all_tokens=all_tokens,
            all_docs_lenghts=all_docs_lenghts,
            avg_doc_lenght=avg_doc_lenght,
            documnts_frequency=documnts_frequency,
            idf=idf)

    def search(self, query: str, k: int, max_chunk_size: int = 2000) -> None:
        pass
