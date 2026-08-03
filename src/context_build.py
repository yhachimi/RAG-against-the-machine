from .models import Chunk, MinimalSource


SYSTEM_PROMPT = ""

with open("src/prompt","r") as file:
    SYSTEM_PROMPT = file.read()


def build_context(chunks: list[tuple[Chunk, float]])->str:
    context = ""

    for chunk, _ in  chunks:
        file_path = chunk.file_path
        content = chunk.content
        context += f"========== File: {file_path} ==========\n"
        context += f"{content}\n\n"
    return  context



def src_builder(chunks: list[tuple[Chunk, float]])-> list[MinimalSource]:
    srcs: list[MinimalSource] = []
    for chunk, _ in chunks:
        src = {}
        src["file_path"] = chunk.file_path
        src["first_character_index"] = chunk.first_character_index
        src["last_character_index"] = chunk.last_character_index
        srcs.append(MinimalSource(**src))



    return srcs



def build_prompt(question: str, context: str) -> str:
        return f"""{SYSTEM_PROMPT}
==================== CONTEXT ====================
{context}
=================================================
Question:
{question}

Answer: """

