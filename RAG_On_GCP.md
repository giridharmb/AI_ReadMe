## Storing RAG Data on Google Cloud for ADK Integration

This repository explains how to store data in a Retrieval-Augmented Generation (RAG) system on Google Cloud to support query processing in a multi-agent system powered by Google’s Agent Development Kit (ADK), alongside Model Context Protocol (MCP) servers and Large Language Models (LLMs). The focus is on leveraging Google Cloud services to prepare, index, and store RAG data for efficient retrieval, ensuring scalability and integration with ADK.

#### Overview

RAG enhances LLM responses by retrieving relevant data from a knowledge base, indexed in a vector store. On Google Cloud, RAG data storage uses services like Google Cloud Storage (GCS), Vertex AI Text Embeddings, and Vertex AI Vector Search to handle data for queries like “Recent AI research.” This README details the process of storing RAG data on Google Cloud, tailored for ADK’s query pipeline.
Repository Contents

#### Storing RAG Data on Google Cloud

Storing RAG data involves preparing, chunking, embedding, and indexing data using Google Cloud services. Below are the key steps:

1. Prepare the Data

- Sources: Collect documents (e.g., AI research papers, PDFs) or enterprise data.
- Storage: Store raw data in Google Cloud Storage (GCS) buckets.
- Create bucket: gsutil mb gs://your-rag-data-bucket
- Upload: gsutil cp ai_paper.pdf gs://your-rag-data-bucket/raw_data/

Cleaning: Use Cloud Functions or Cloud Run to extract text and normalize (e.g., remove noise with PyPDF2).

Output: Save cleaned text to gs://your-rag-data-bucket/cleaned_data/.

2. Chunk the Data

Purpose: Split documents into chunks (e.g., 100-200 words) for embedding and retrieval.

Process:

- Read from GCS using google-cloud-storage.
- Chunk with langchain.text_splitter (e.g., by paragraphs, 10% overlap).

Execution: Run in Cloud Run or Dataflow for large datasets.

Output: Save chunks as JSON to gs://your-rag-data-bucket/chunks/ (e.g., { "chunk_id": 1, "text": "chunk text" }).

3. Generate Embeddings

- Purpose: Convert chunks into semantic vectors.
- Service: Use Vertex AI Text Embeddings (e.g., text-embedding-gecko).

Process:

Authenticate with a service account.

Generate embeddings via Vertex AI SDK:from vertexai.language_models import TextEmbeddingModel

```python
model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@001")
embeddings = model.get_embeddings(["chunk text"])
```

Execution: Process in Cloud Run or Dataflow for scale.

Output: Save embeddings to gs://your-rag-data-bucket/embeddings/ (e.g., JSON or NumPy).

4. Store in a Vector Store

Service: Use Vertex AI Vector Search for scalable similarity search.

Setup:

- Create an index via Vertex AI console or gcloud ai indexes create.
- Configure: 768 dimensions (for Gecko), cosine distance, ANN search.

Indexing:

- Upload embeddings to GCS as JSONL (e.g., { "id": "chunk_1", "embedding": [0.1, ...] }).
- Import to Vector Search: gcloud ai index-endpoints deploy-index.

Metadata: Store in Cloud Firestore or BigQuery (e.g., { "chunk_id": 1, "source": "ai_paper.pdf" }).

5. Build the Knowledge Base

Structure:

- Vector Store: Vertex AI Vector Search.
- Metadata: Firestore or BigQuery.
- Optional Full-Text: GCS or BigQuery for original chunks.

Access: ADK connects via Vertex AI SDK and Firestore credentials.

6. Update and Maintain

Updates: Add new data to GCS and re-index with Cloud Scheduler and Cloud Functions.
Re-Indexing: Update Vector Search for new embeddings using Dataflow.
Pruning: Remove stale data with Cloud Workflows.
Monitoring: Track performance with Cloud Monitoring.

ADK Integration

- RAG Tool: ADK’s LlmAgent queries Vertex AI Vector Search to retrieve chunks for queries (e.g., “Recent AI research”).
- Authentication: Use a service account with GCS, Vertex AI, and Firestore permissions.
- Workflow: RAG tool augments LLM prompts with retrieved chunks.
- Diagram: The adk_fancy_diagram.png (from gen_d.py) shows RAG’s role in data retrieval.

Example Code

```python
from google.cloud import storage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vertexai.language_models import TextEmbeddingModel

# Read and chunk from GCS
client = storage.Client()
bucket = client.get_bucket("your-rag-data-bucket")
blob = bucket.get_blob("cleaned_data/ai_paper.txt")
text = blob.download_as_string().decode("utf-8")
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.split_text(text)

# Generate embeddings
from vertexai import init
init(project="your-project-id", location="us-central1")
model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@001")
embeddings = [model.get_embeddings([chunk])[0].values for chunk in chunks]

# Save embeddings to GCS
for i, embedding in enumerate(embeddings):
    blob = bucket.blob(f"embeddings/chunk_{i}.json")
    blob.upload_from_string(json.dumps({"id": f"chunk_{i}", "embedding": embedding}))
```

#### Authenticate:

- Create a service account with roles: Storage Admin, Vertex AI User, Firestore User.
- Set key: export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"

#### Troubleshooting

- GCS Errors: Verify bucket permissions and service account roles.
- Vertex AI Issues: Ensure project ID and region are correct; check quota limits.
- Vector Search Setup: Use Vertex AI console for initial index creation if CLI fails.

#### References 

- Google Cloud Storage: GCS Docs
- Vertex AI Vector Search: Vertex AI Docs
- Vertex AI Embeddings: Text Embeddings
- LangChain: LangChain RAG