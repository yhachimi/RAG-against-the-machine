from .models import Chunk


class EmbeddingModel:
    def __init__(self) -> None:
        pass

    def docs_embder(self, chunks: list[Chunk]) -> list[list[float]]:
        res: list[list[float]] = []
        return res

    def query_embeding(self, query: str) -> list[float]:
        res: list[float] = []
        return res
