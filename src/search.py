import numpy as np

from .embeddings import EmbeddingModel
from .models import BM25_DATA, Chunk 



def cosine_similarity(embedding_query, embeddings_chunks)->list[float]:
    """
        Compute the cosine similarity between a query embedding and all indexed
        document embeddings.

        Args:
         embedding_query: A 1-D NumPy array representing the query embedding.
         embeddings_chunks: A 2-D NumPy array of shape
         (num_chunks, embedding_dim) containing the indexed document embeddings.

        Returns:
            A 1-D NumPy array containing the cosine similarity score between the
         query and each indexed document embedding """
    query_norm = np.linalg.norm(embedding_query)
    dots  = np.dot(embeddings_chunks, embedding_query)
    embedding_norms = np.linalg.norm(embeddings_chunks, axis=1)

    return dots / (embedding_norms * query_norm)
    







