from pydantic import BaseModel


class Chunk(BaseModel):
    type: str
    file_path: str
    title: str
    content: str
    start: int
    end: int
    id: int
