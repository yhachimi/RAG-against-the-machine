Build Index
│
├── Read files
├── Chunk files
├── Tokenize chunks
├── Compute doc lengths
├── Compute average length
└── Compute document frequency

===============================

Runtime
│
├── Receive user query
├── Tokenize query
├── Compute BM25 scores
├── Sort scores
├── Take Top-K
├── Build prompt
└── Send to LLM
