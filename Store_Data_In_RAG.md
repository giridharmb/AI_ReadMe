## Storing Data in RAG for Google ADK Integration

This repository explains how to store data in a Retrieval-Augmented Generation (RAG) system to support query processing in a multi-agent system powered by Google’s Agent Development Kit (ADK), alongside Model Context Protocol (MCP) servers and Large Language Models (LLMs). The focus is on preparing, indexing, and storing data in a RAG system to enable efficient retrieval for augmenting LLM responses. The repository includes a Python script (gen_d.py) to visualize the ADK-RAG-MCP-LLM interaction.

#### Overview

RAG enhances LLM responses by retrieving relevant data from a knowledge base, which is indexed in a vector store. In the ADK context, RAG provides domain-specific data (e.g., AI research papers) for queries like “How to build an AI?”. This README details the process of storing data in RAG, ensuring compatibility with ADK’s query processing pipeline.
Repository Contents

#### Storing Data in RAG

Storing data in RAG involves preparing, chunking, embedding, and indexing data for retrieval. Below are the key steps:

1. Prepare the Data

- Sources: Collect documents (e.g., PDFs, web pages), databases, or enterprise data (e.g., AI research papers).
- Cleaning: Normalize text (e.g., remove noise, standardize format) using tools like pandas or BeautifulSoup.
- Example: Extract text from ai_paper.pdf and remove formatting artifacts.

2. Chunk the Data

Purpose: Split large documents into smaller chunks (e.g., 100-200 words) for efficient embedding and retrieval.

Methods:

Fixed-length (e.g., 500 characters).
Semantic (e.g., by paragraphs).
Overlap (e.g., 10% overlap for context).

Tools: langchain.text_splitter, nltk, or custom splitters.

Example: Split a 10-page PDF into 50 chunks of 150 words each.

3. Generate Embeddings

- Purpose: Convert chunks into numerical vectors capturing semantic meaning.
- Process: Use an embedding model (e.g., text-embedding-gecko, all-MiniLM-L6-v2).
- Tools: sentence-transformers, Google Vertex AI embeddings, or Hugging Face transformers.
- Example: Generate 768-dimensional vectors for each chunk using SentenceTransformer.

4. Store in a Vector Store

Purpose: Index embeddings for fast similarity search.

Options:

- Chroma: Lightweight, local.
- Pinecone: Scalable, cloud-based.
- FAISS: High-performance local search.
- Google Vertex AI Vector Search: Enterprise-grade, ADK-compatible.

- Process: Store embeddings with metadata (e.g., source, chunk ID) using Chroma.add() or Pinecone.upsert().
- Example: Index 50 embeddings in Chroma with metadata like { "source": "ai_paper.pdf" }.

5. Build the Knowledge Base

- Purpose: Combine vector store with metadata for comprehensive retrieval.
- Structure: Pair vector store with a metadata database (e.g., SQLite) or full-text index (e.g., Elasticsearch).
- Example: Store paper abstracts in Chroma, with titles and dates in SQLite.

6. Update and Maintain

- Updates: Refresh data periodically (e.g., monthly for papers).
- Re-Indexing: Regenerate embeddings for updated data or model changes.
- Automation: Use pipelines (e.g., Google Cloud Workflows) for updates.
- Example: Script to add new AI papers daily.

#### ADK Integration

- RAG Tool: ADK’s LlmAgent invokes RAG to query the vector store for domain-specific data (e.g., “Recent AI research”).
- Workflow: Configured via Python, RAG connects to the vector store (e.g., Chroma) to retrieve chunks.
- Security: Use secure storage (e.g., Google Cloud with IAM) for sensitive data.
- Maintenance: ADK can trigger update scripts as custom tools.

- Example Code

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from chromadb import Client

# Prepare and chunk
documents = ["text from ai_paper.pdf"]
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.split_text("\n".join(documents))

# Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)

# Store in Chroma
chroma_client = Client()
collection = chroma_client.create_collection("ai_knowledge_base")
for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[embedding.tolist()],
        metadatas=[{"source": "ai_paper.pdf", "chunk_id": i}],
        documents=[chunk]
    )
```