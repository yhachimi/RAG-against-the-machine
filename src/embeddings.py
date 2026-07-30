from typing import Any

from sentence_transformers import SentenceTransformer


from FlagEmbedding import FlagModel


class EmbeddingModel:
    def __init__(self) -> None:
        self.model = FlagModel(
            "BAAI/bge-small-en-v1.5",
            use_fp16=False,   # CPU
        )

    def docs_embder(self, docs: list[str]) -> list[list[float]]:
        return self.model.encode(docs).tolist()

    def query_embeding(self, query: str) -> list[float]:
        return self.model.encode([query])[0].tolist()
