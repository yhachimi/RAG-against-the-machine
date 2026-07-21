from .models import BM25_DATA
from .tokenization import term_frequency


def bm25_score(query_tokens: list[str],
               bm25_data: BM25_DATA) -> list[tuple[int, float]]:
    """
    Calculate the BM25 relevance score for every indexed chunk and
    return a ranked list of (chunk_id, score).

    BM25 ranks documents according to their relevance to a user query
    using term frequency (TF), inverse document frequency (IDF), and
    document length normalization.

    Formula:
        score(D, Q) = Σ IDF(q) *
                      (tf(q, D) * (k1 + 1)) /
                      (tf(q, D) + k1 * (1 - b + b * |D| / avgdl))

    where:
        - tf(q, D): frequency of query term q in document D.
        - IDF(q): inverse document frequency of q.
        - |D|: length of document D.
        - avgdl: average document length.
        - k1: term frequency saturation parameter (typically 1.5).
        - b: document length normalization parameter (typically 0.75).

    Returns:
        A list of tuples (chunk_id, score), sorted in descending order
        of BM25 score.
    """
    res: list[tuple[int, float]] = []
    k1 = 1.5
    b = 0.75
    tf = term_frequency(query_tokens, bm25_data.all_tokens)
    for doc_id, doc_tf in enumerate(tf):
        score = 0.0
        for token in query_tokens:
            query_tf = doc_tf[token]
            if query_tf == 0:
                continue
            query_idf = bm25_data.idf.get(token, 0.0)
            d = bm25_data.all_docs_lenghts[doc_id]
            numerator = query_tf * (k1 + 1)
            denominator = query_tf + k1 * \
                (1 - b + b * (d / bm25_data.avg_doc_lenght))
            score += query_idf * (numerator / denominator)

        res.append((doc_id, score))
    res.sort(key=lambda x: x[1], reverse=True)
    return res
