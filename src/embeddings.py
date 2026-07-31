from typing import Any

from FlagEmbedding import FlagModel


class EmbeddingModel:
    def __init__(self) -> None:
        self.model = FlagModel(
            "BAAI/bge-small-en-v1.5",
            use_fp16=False,
        )

    def docs_embder(self, docs: list[str]) -> list[list[float]]:
        return self.model.encode(docs,batch_size=256).tolist()

    def query_embeding(self, query: str) -> list[float]:
        return self.model.encode([query])[0].tolist()
