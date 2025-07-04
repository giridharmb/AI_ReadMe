## Google ADK with RAG, MCP, and LLM: Interaction and Decision Logic

This repository documents the interaction between Google’s Agent Development Kit (ADK), Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP) servers, and Large Language Models (LLMs) in a multi-agent system for processing user queries. It explains how ADK decides whether to use RAG or MCP servers and compares their pros and cons. The repository includes a Python script (gen_d.py) to generate a visual flowchart of the interaction.

#### Overview

The system processes user queries (e.g., “How to build an AI?”) through a pipeline orchestrated by ADK, leveraging RAG for data retrieval, MCP for external tool access, and LLMs for response generation. ADK’s LlmAgent uses LLM reasoning, predefined rules, and tool availability to decide whether to invoke RAG, MCP, or both, ensuring accurate and contextually relevant responses.

#### System Components

- Google ADK: Orchestrates agents (LlmAgent, SequentialAgent) and tools to manage query workflows.
- RAG: Retrieves domain-specific data from a knowledge base using a vector store and semantic search.
- MCP Server: Provides access to external tools (e.g., YouTube Search, database queries) via a standardized protocol.
- LLM: Generates responses (e.g., Gemini 2.0, Gemma 3) using augmented prompts from RAG and MCP outputs.

#### How ADK Decides to Use RAG or MCP

ADK’s decision to use RAG, MCP, or both is driven by the LlmAgent and workflow configuration:

#### Query Interpretation:

The LlmAgent, powered by an LLM, analyzes the query’s intent and context.

Example: “Recent AI papers” → RAG (knowledge base); “YouTube AI tutorials” → MCP (external search).

#### Tool Selection:

- Rules/Workflows: Predefined logic (e.g., via SequentialAgent) maps query types to tools.
- LLM Reasoning: The LLM evaluates whether static data (RAG) or dynamic services (MCP) are needed.
- Hybrid Queries: Complex queries (e.g., “Compare papers and videos”) use both.

#### Tool Availability:

ADK queries MCP servers for available tools (e.g., youtube_search). If none match, RAG or LLM fallback is used.

#### Session State:

ADK caches prior results (e.g., RAG data) to optimize follow-up queries.

#### Example:

Query: “What is the latest AI research?”
Action: RAG retrieves papers from a vector store.

Query: “Find YouTube AI tutorials.”
Action: MCP invokes youtube_search.

Query: “Compare AI papers and tutorials.”
Action: RAG for papers, MCP for videos, combined by LLM.

#### Pros and Cons of RAG vs. MCP

- RAG
    - Pros:
        - Retrieves curated, domain-specific data (e.g., enterprise documents).
        - Accurate, contextually relevant results reduce LLM hallucinations.
        - Offline-capable, cost-effective with pre-indexed data.
        - Customizable knowledge base for niche domains.

    - Cons:
        - Limited to static, pre-indexed data (no real-time updates).
        - Requires maintenance of knowledge base and vector store.
        - Cannot perform actions or access external services.
        - Large knowledge bases demand significant resources.

- MCP Server
    - Pros:
        - Accesses real-time data via external services (e.g., YouTube, databases).
        - Supports actions (e.g., API calls, queries), expanding capabilities.
        - Extensible with new tools via MCP’s standardized protocol.
        - Suitable for diverse, dynamic queries.

    - Cons:
        - Depends on internet and third-party APIs (latency, downtime risks).
        - API calls may incur costs or rate limits.
        - Setup and maintenance of MCP servers are complex.
        - External data quality varies, requiring filtering.

#### When to Use:

- RAG: Factual, domain-specific queries (e.g., internal documents).
- MCP: Real-time data or actions (e.g., web searches, API calls).
- Both: Hybrid queries needing static and dynamic data.

#### Interaction Flow

- User Query: Submitted via a front-end (e.g., web app).
- ADK Orchestration: LlmAgent interprets query, decides tools.
- RAG Retrieval: Fetches data from knowledge base if needed.
- MCP Access: Invokes external tools via MCP servers if required.
- LLM Generation: Processes augmented prompt (query + RAG/MCP outputs).
- Response Delivery: Returns answer to user, often with citations.