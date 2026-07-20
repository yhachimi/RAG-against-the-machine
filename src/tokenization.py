from math import log

from .models import Chunk


def tokens_genrate(all_chunks: list[Chunk]) -> list[list[str]]:
    """genrate a valid toknz from the code_base"""
    all_tokens = []
    UNWANTED_CHARS = set(".,:;()[]{}<>=+-*/\\|&!?@#$%^~`\"'")
    for chunk in all_chunks:
        search_text = chunk.title + "\n" + chunk.content
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


def query_tokens_genrate(query: str) -> list[str]:
    """genrate the user query tokens"""
    splited_query = query.split()
    tokens = []
    UNWANTED_CHARS = set(".,:;()[]{}<>=+-*/\\|&!?@#$%^~`\"'")
    for word in splited_query:
        token = ("".join([c for c in word.lower() if c not in UNWANTED_CHARS]))
        if token:
            tokens.append(token)

    return tokens


def term_frequency(
        query_tokens: list[str],
        all_tokens: list[list[str]]) -> list[dict[str, int]]:
    """calc the  user query  term  frequency"""
    tf = []
    for tokens in all_tokens:
        tfs = {}
        for token in set(query_tokens):
            tfs[token] = tokens.count(token)
        tf.append(tfs)

    return tf


def inverse_docs_frequency(df: dict[str, int], N: int) -> dict[str, float]:
    """Calculate the inverse document frequency (IDF) for each token
        using the standard BM25 formula.
        IDF(t) = log(1 + (N - df(t) + 0.5) / (df(t) + 0.5)
                     """
    idf = {}
    for key, value in df.items():
        idf[key] = log(1 + ((N - value + 0.5) / (value + 0.5)))

    return idf
