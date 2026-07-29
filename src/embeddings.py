from typing import Any

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self) -> None:
        """ the init method  where i init my modle"""
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def docs_embder(self, docs: list[str]) -> list[list[float]] | Any:
        """return lists of encoded docs"""
        embeddings: Any = self.model.encode(docs,
                                        batch_size=120,
                                        show_progress_bar=True,
                                        normalize_embeddings=True,
                                        convert_to_numpy=True,
                                        )
        return embeddings.tolist()

    def query_embeding(self, query: str) -> list[float] | Any:
        """return list of encoded query"""
        return self.model.encode(query).tolist()
