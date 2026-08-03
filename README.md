                    RAG ENGINE

                        INDEX
                          │
        ┌─────────────────┴──────────────────┐
        │                                    │
Read codebase                         Read markdown
        │                                    │
        └───────────────┬────────────────────┘
                        │
                  Chunk documents
                        │
                  Split large chunks
                        │
         ┌──────────────┴──────────────┐
         │                             │
      BM25 Index                 Semantic Index
         │                             │
      Tokenize                    Embed chunks
         │                             │
Compute DF / IDF                 Save embeddings.npy
         │
Save bm25.json
         │
Save chunks.json
         │
==================== INDEX FINISHED ====================

                        SEARCH
                          │
                    Load index once
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
  Semantic Search                     BM25 Search
        │                                   │
Embed query                     Tokenize query
        │                                   │
Cosine similarity             BM25 score
        │                                   │
Top-K semantic                Top-K BM25
        └─────────────────┬─────────────────┘
                          │
                    Hybrid Search
                          │
                 Normalize both scores
                          │
          weighted_sum =
              α * semantic +
              β * bm25
                          │
                     Re-rank results
                          │
                     Final Top-K
                          │
                   Build Context
                          │
         ┌────────────────┴────────────────┐
         │                                 │
      Print context                 Send to LLM 





     """
        Combine semantic search and BM25 search into a single ranked result list.

        Hybrid search improves retrieval quality by combining:

        1. Semantic similarity (embedding cosine similarity)
        2. Lexical similarity (BM25)

        Since the two scoring methods produce values on different scales,
        both scores are first normalized using Min-Max normalization.

        Min-Max normalization:

        normalized_score = (score - min_score) / (max_score - min_score)

        This maps every score into the range [0, 1].

        After normalization, the final hybrid score is computed as a
        weighted linear combination:

        final_score = (alpha * semantic_score) +
                      (beta * bm25_score)

         where:
            - semantic_score is the normalized cosine similarity.
        - bm25_score is the normalized BM25 score.
        - alpha and beta are configurable weights controlling the
          contribution of each retrieval method.

        Finally, all documents are sorted in descending order according to
        their final hybrid score, and the top-k highest ranked chunks are
        returned.

        Returns:
        list[tuple[Chunk, float]]:
            A list of (Chunk, hybrid_score) tuples sorted from the
            highest to the lowest hybrid score."""

