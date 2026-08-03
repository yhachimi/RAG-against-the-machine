# RAG Against the Machine

A Retrieval-Augmented Generation (RAG) engine built completely from scratch in Python.

Unlike solutions that rely on vector databases such as ChromaDB or Pinecone, this project implements the entire retrieval pipeline manually, including document indexing, chunking, semantic embeddings, BM25 ranking, cosine similarity search, and hybrid retrieval.

The goal of this project is to understand how modern retrieval systems work internally instead of treating them as black boxes.

---

# Features

* Codebase reader for Python and Markdown projects
* AST-based Python chunking
* Markdown section chunking
* Automatic large chunk splitting
* Semantic embeddings using **BAAI/bge-small-en-v1.5**
* Cosine similarity search implemented with NumPy
* BM25 keyword retrieval implemented from scratch
* Hybrid retrieval (Semantic + BM25)
* Persistent indexing
* Fast loading without rebuilding the index
* Modular architecture

---

# Project Structure

```text
src/
│
├── codebase_reader.py
├── embeddings.py
├── ranking.py
├── search.py
├── tokenization.py
├── models.py
├── rag.py
└── cli.py

data/
└── processed/
    ├── chunks.json
    ├── bm25.json
    └── embeddings.npy
```

---

# Indexing Pipeline

The indexing stage is responsible for converting an entire codebase into searchable data.

## 1. Read the codebase

Supported files:

* `.py`
* `.md`

Each file is loaded into memory together with its metadata.

---

## 2. Chunking

Python files are parsed using the Python AST.

Each chunk represents:

* imports
* classes
* functions
* methods

Markdown files are split using section headings.

Very large chunks are automatically split into smaller chunks.

---

## 3. Tokenization

Every chunk is tokenized.

The tokenizer is used to compute:

* document frequency
* inverse document frequency
* document lengths
* average document length

These values are required for BM25.

---

## 4. Semantic Embeddings

Each chunk is converted into a dense vector using:

```text
BAAI/bge-small-en-v1.5
```

Embeddings are stored inside:

```text
data/processed/embeddings.npy
```

---

## 5. Save Index

The indexing stage generates three files.

### chunks.json

Stores every searchable chunk.

### bm25.json

Stores all BM25 metadata.

### embeddings.npy

Stores semantic vectors.

After indexing, the project never needs to rebuild the embeddings unless the codebase changes.

---

# Search Pipeline

Searching consists of three independent stages.

---

## Semantic Search

The user query is embedded using the same embedding model.

Cosine similarity is computed against every stored embedding.

The highest scoring chunks are selected.

---

## BM25 Search

The query is tokenized.

BM25 scores are computed against every indexed chunk.

The highest scoring chunks are selected.

---

## Hybrid Search

Both retrieval methods are combined.

### Step 1

Normalize semantic scores using Min-Max normalization.

### Step 2

Normalize BM25 scores using Min-Max normalization.

### Step 3

Merge both results using each chunk's unique ID.

### Step 4

Compute the final score.

```text
Final Score =
α × Semantic Score +
β × BM25 Score
```

Current weights:

```text
Semantic = 0.6

BM25 = 0.4
```

Finally, the chunks are sorted and the Top-K results are returned.

---

# Search Flow

```text
User Query
      │
      ▼
Embedding Model
      │
      ▼
Semantic Search
      │
      ▼
Cosine Similarity
      │
      ▼

               Hybrid Ranking
             ▲               ▲
             │               │
             │               │
      BM25 Search      Semantic Search
             │
             ▼

      Top K Chunks
```

---

# Technologies

* Python
* NumPy
* FlagEmbedding
* tqdm
* Pydantic

---

# Future Work

* Context builder
* Prompt generation
* LLM integration
* Streaming responses
* Query caching
* Embedding caching
* Incremental indexing
* Parallel embedding generation
* Optional vector database backend
* Evaluation metrics
* Reranking models

---

# Why Build Everything From Scratch?

Most RAG frameworks hide the retrieval process behind external libraries.

This project intentionally implements the complete retrieval pipeline manually to better understand:

* AST parsing
* Chunking strategies
* Tokenization
* BM25
* Embedding generation
* Cosine similarity
* Hybrid ranking
* Index serialization
* Information retrieval fundamentals

The objective is educational as much as practical.

---

# Current Status

* ✅ Codebase reader
* ✅ Python chunking
* ✅ Markdown chunking
* ✅ Chunk splitting
* ✅ Tokenization
* ✅ BM25 indexing
* ✅ Embedding generation
* ✅ Cosine similarity
* ✅ Semantic search
* ✅ BM25 search
* ✅ Hybrid retrieval

Remaining work:

* Context builder
* Prompt construction
* LLM integration
* Final answer generation

