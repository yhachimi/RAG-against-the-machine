import json
from pathlib import Path

from tqdm import tqdm

from .codebase_reader import (codebase_reader, markdown_chunker,
                              python_code_chunker, split_chunks)
from .models import BM25_DATA, Chunk
from .tokenization import (calc_docs_lenghts, document_frequency,
                           inverse_docs_frequency, tokens_genrate)

from  .search import cosine_similarity
from  .embeddings import EmbeddingModel 
import  numpy as np 


class Rag:
    def __init__(self):
        self.embedding_model = EmbeddingModel() 
    def index(self, max_chunk_size: int = 2000) -> None:
        """this methode is represonting the indexing part
        markdown  and python code chunking chunks indexing
        and calc the bm25 needed data like idf and df"""
        all_chunks: list[Chunk] = []
        code_base = codebase_reader("vllm-0.10.1")
        for document in tqdm(code_base, desc="Chunking"):
            suffix = Path(document["file_path"]).suffix
            if suffix == ".py":
                chunked = python_code_chunker(document)
                if chunked:
                    all_chunks.extend(chunked)
            elif suffix == ".md":
                chunked = markdown_chunker(document)
                all_chunks.extend(chunked)

        for chunk_id, chunk in enumerate(all_chunks):
            chunk.id = chunk_id
        all_chunks = split_chunks(all_chunks, max_chunk_size)
        for chunk_id, chunk in enumerate(all_chunks):
            chunk.id = chunk_id

        text_chunks = [chunk.content for chunk in all_chunks]
        

        root = Path("data/processed/")
        root.mkdir(parents=True, exist_ok=True)
        all_tokens = tokens_genrate(all_chunks)
        all_docs_lenghts = calc_docs_lenghts(all_tokens)
        avg_doc_lenght = sum(all_docs_lenghts) / len(all_docs_lenghts)
        documnts_frequency: dict[str, int] = document_frequency(all_tokens)
        idf: dict[str, float] = inverse_docs_frequency(
            documnts_frequency, len(all_chunks))
        bm25_data = BM25_DATA(
            all_tokens=all_tokens,
            all_docs_lenghts=all_docs_lenghts,
            avg_doc_lenght=avg_doc_lenght,
            documnts_frequency=documnts_frequency,
            idf=idf)
        embiders_chunks = self.embedding_model.docs_embder(text_chunks)
        with open(root / "chunks.json", "w", encoding="utf-8") as file:
            json.dump([chunk.model_dump()
                       for chunk in all_chunks], file, indent=4)
        with open(root / "bm25.json", "w", encoding="utf-8") as file:
            json.dump(bm25_data.model_dump(), file, indent=4)

         
        np.save(root / "embeddings.npy", embiders_chunks)
        print("✓ Indexing complete! ", end="")
        print(f"Indexed {len(all_chunks)} chunks under {root}.")

    
    def load_index(self)->None:
        root = Path("data/processed/")
        with open(root / "chunks.json") as file:
            chunks = json.load(file)
            self.all_chunks = [Chunk(**chunk) for chunk in  chunks]


        with open(root / "bm25.json") as file:
            bm25_data = json.load(file)
            self.bm25_data =  BM25_DATA(**bm25_data)

        self.embidded_chunks = np.load(root / "embeddings.npy")

    def search(self, query: str, k: int, max_chunk_size: int = 2000) -> None:
        self.load_index()
        embedding_query = self.embedding_model.query_embeding(query)
        embedding_query = np.array(embedding_query)
        cosain = cosine_similarity(embedding_query, self.embidded_chunks)

