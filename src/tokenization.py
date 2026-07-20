from typing import Any


def tokens_genrate(all_chunks: list[dict[str, Any]]) -> list[list[str]]:
    """genrate a valid toknz from the code_base"""
    all_tokens = []
    UNWANTED_CHARS = set(".,:;()[]{}<>=+-*/\\|&!?@#$%^~`\"'")
    for chunk in all_chunks:
        search_text = chunk["title"] + "\n" + chunk["content"]
        splited_text = search_text.split()
        tokens = ["".join([c for c in token.lower()
                           if c not in UNWANTED_CHARS])
                  for token in splited_text]
        valid_token = [token for token in tokens if token]
        all_tokens.append(valid_token)

    return all_tokens


def calc_docs_lenghts(all_tokens: list[list[str]]) -> list[int]:
    """calc the docmments lenght"""
    i = 0
    all_docs_lenght = []
    while i < len(all_tokens):
        all_docs_lenght.append(len(all_tokens[i]))
        i += 1

    return all_docs_lenght


def document_frequency(all_tokens: list[list[str]]) -> dict[str, int]:
    """count the docmments frequency for all tokens genrated"""
    df: dict[str, int] = {}

    for tokens in all_tokens:
        unique_tokens = set(tokens)
        for token in unique_tokens:
            if token not in df:
                df[token] = 1
            else:
                df[token] += 1

    return df
