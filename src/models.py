from pydantic import BaseModel


class Chunk(BaseModel):
    type: str
    file_path: str
    title: str
    content: str
    start: int
    end: int
    id: int
    first_character_index: int
    last_character_index: int


class BM25_DATA(BaseModel):
    all_tokens: list[list[str]]
    all_docs_lenghts: list[int]
    avg_doc_lenght: float
    documnts_frequency: dict[str, int]
    idf: dict[str, float]
