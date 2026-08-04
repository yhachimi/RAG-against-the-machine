import json
from pathlib import Path

from tqdm import tqdm

from .codebase_reader import (codebase_reader, markdown_chunker,
                              python_code_chunker, split_chunks)

from .models import (Chunk, BM25_DATA, MinimalSource,MinimalAnswer) 
from .tokenization import (calc_docs_lenghts, document_frequency,
                           inverse_docs_frequency, tokens_genrate,
                           query_tokens_genrate,)

from  .search import cosine_similarity
from  .embeddings import EmbeddingModel 
import  numpy as np 
from .ranking import bm25_score
from .context_build import (build_context, src_builder, build_prompt)
from .llm import LLM 
import uuid 

class Rag:
    def __init__(self):
        self.embedding_model = EmbeddingModel() 
        self.llm_model = LLM()
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

    
    def _load_index(self)->None:
        root = Path("data/processed/")
        with open(root / "chunks.json") as file:
            chunks = json.load(file)
            self.all_chunks = [Chunk(**chunk) for chunk in  chunks]


        with open(root / "bm25.json") as file:
            bm25_data = json.load(file)
            self.bm25_data =  BM25_DATA(**bm25_data)

        self.embidded_chunks = np.load(root / "embeddings.npy")

    def _semantic_search(self, query: str, k: int) -> list[tuple[Chunk, float]]: 
        embedding_query = self.embedding_model.query_embeding(query)
        embedding_query = np.array(embedding_query)
        scores = cosine_similarity(embedding_query, self.embidded_chunks)
        top_k_indices = np.argsort(scores)[::-1][:k]
        return [(self.all_chunks[i], scores[i]) for i  in top_k_indices]

    def _bm25_search(self, query: str, k: int) -> list[tuple[Chunk, float]]:
        query_tokens = query_tokens_genrate(query)
        bm25_scores =  bm25_score(query_tokens, self.bm25_data)
        result = [(self.all_chunks[idx], score) for idx, score in  bm25_scores[:k]]
        return  result
   



    def _hybrid_search(self, semantic_result, bm25_result,k):
        norm_semantic = []
        mini = min(semantic_result, key=lambda x: x[1])[1]
        maxm = max(semantic_result, key= lambda x: x[1])[1]
        if maxm == mini:
            maxm += 1
        for chunk,  score in  semantic_result:
            norm = (score - mini) / (maxm - mini)
            norm_semantic.append((chunk, norm))

        norm_bm25 = []

        mini = min(bm25_result, key=lambda x: x[1])[1]
        maxm = max(bm25_result, key=lambda x: x[1])[1]
        if maxm == mini:
            maxm += 1
        for chunk,  score in  bm25_result:
            norm = (score - mini) / (maxm - mini)
            norm_bm25.append((chunk, norm))

        alpha = 0.6
        beta = 0.4
        all_scores =  {chunk.id: {"chunk":  chunk, "semantic": score, "bm25": 0} for chunk, score in norm_semantic}
        for chunk, score in norm_bm25:
            if all_scores.get(chunk.id):
                all_scores[chunk.id]["bm25"] = score

            else:
                all_scores[chunk.id] = {"chunk":  chunk, "semantic": 0, "bm25": score} 

        hyprid_reslut = []
        for data in  all_scores.values():
            semantic = data["semantic"]
            bm25 = data["bm25"]
            chunk = data["chunk"]
            final_score =  alpha * semantic + beta * bm25 
            hyprid_reslut.append((chunk, final_score))

        hyprid_reslut.sort(key=lambda x: x[1], reverse=True)
        return  hyprid_reslut[:k]



    def search(self, query: str, k: int, max_chunk_size: int = 2000) -> None:
        self._load_index()
        semantic_result = self._semantic_search(query, k)
        bm25_result = self._bm25_search(query, k)
        hyprid_reslut =  self._hybrid_search(semantic_result, bm25_result, k)
        context = build_context(hyprid_reslut)
        prompt = build_prompt(query, context)
        answer = self.llm_model.genrate_answer(prompt)
        minisrcs = src_builder(hyprid_reslut)
        answer = answer.split("<END>", 1)[0].strip()
        answer_model = MinimalAnswer(
                question_id=str(uuid.uuid4()),question=query,
                retrieved_sources=minisrcs,answer=answer)
        print(answer_model.answer)
