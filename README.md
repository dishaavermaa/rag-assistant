# 🧠 Insurellm RAG Assistant

A Retrieval-Augmented Generation (RAG) system built using **Python, OpenAI, LangChain, and Gradio**, designed to deliver accurate, context-aware responses based on a structured knowledge base of company **employees** and **products**.

---

## 🚀 Overview

This project implements a **progressive RAG architecture**, evolving from a baseline keyword-driven retrieval system to an advanced **embedding-based semantic retrieval pipeline**.

The system retrieves relevant context from a local knowledge base and uses a Large Language Model (LLM) to generate **grounded, precise, and reliable responses**.

---

## 🌿 Branch Structure

This repository is organized into multiple branches to clearly separate different stages of the system's evolution:

### 🔹 `main` (Enhanced RAG System)

Contains the **current advanced implementation**, including:

* LangChain-based document loading
* Recursive chunking with overlap
* Embedding generation (HuggingFace / OpenAI)
* Chroma vector database for similarity search
* Semantic retrieval pipeline
* Context-aware LLM response generation
* Gradio-based interactive UI

This branch represents the **most complete and production-aligned version** of the system.

---

### 🚀 `feature-enhancement` (Ongoing Improvements)

Used for iterative development and experimentation on top of the enhanced pipeline.

Typical additions include:

* Retrieval optimizations
* Hybrid search (keyword + semantic)
* Reranking strategies
* Performance improvements
* Feature extensions

---

### 🧩 `legacy-code` (Baseline RAG System)

Contains the original implementation based on:

* Markdown document loading
* Text normalization and tokenization
* Keyword overlap-based scoring
* Direct prompt context injection

This version serves as a **reference for foundational RAG concepts** and highlights the evolution toward semantic retrieval.

---

## 🏗️ Project Structure

```bash
rag_assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── knowledge-base/
    ├── employees/
    └── products/
```

---

## ⚙️ Features

### Core Features

* 📂 Structured knowledge base (employees + products)
* 💬 Interactive chat interface using Gradio
* 🧠 Context-grounded LLM responses
* ❌ Controlled hallucination via prompt constraints

---

### Advanced Features (main branch)

* 🔍 Semantic search using embeddings
* ✂️ Recursive document chunking with overlap
* 🧠 Vector database (Chroma) for efficient retrieval
* 📌 Metadata-enriched document indexing
* 📊 Token and corpus analysis

---

## 🧠 System Architecture

### 🔹 Baseline (legacy-code)

```text
User Query
→ Tokenization
→ Keyword Matching
→ Document Selection
→ Prompt Injection
→ LLM Response
```

---

### 🚀 Enhanced (main branch)

```text
User Query
→ Query Embedding
→ Vector Similarity Search (Chroma)
→ Top-K Relevant Chunks
→ Context Injection
→ LLM Response
```

---

## 🧪 Example Queries

* "Who is Avery Lancaster?"
* "What does Claimllm do?"

---

## 🛠️ Installation

### 1. Clone repository

```bash
git clone https://github.com/dishaavermaa/rag-assistant.git
cd rag-assistant
```

---

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

### 5. Run the application

```bash
python app.py
```

---

## 📚 Knowledge Base Format

### Example: Employee

```md
# Avery Lancaster
 Avery Lancaster co-founded Insurellm in 2015 and has since guided the company to its current position as a leading Insurance Tech provider.
```

---

### Example: Product

```md
# Claimllm
Claimllm is Insurellm's revolutionary claims processing platform that transforms the claims experience for insurers, adjusters, and policyholders.
```

---

## ⚠️ Limitations

* Baseline branch relies on keyword matching (limited semantic understanding)
* Vector store is rebuilt on each run (can be optimized with persistence strategy)
* No reranking or retrieval evaluation metrics implemented yet

---

## 🚀 Future Enhancements

* 🔹 Persistent vector index loading
* 🔹 Hybrid retrieval (BM25 + embeddings)
* 🔹 Cross-encoder / LLM-based reranking
* 🔹 Retrieval evaluation metrics (recall@k, precision@k)
* 🔹 Streaming responses
* 🔹 Source attribution in UI

---

## 🧠 Tech Stack

* Python
* OpenAI API
* LangChain
* Chroma (Vector Database)
* HuggingFace Embeddings
* Gradio

---

## 💡 Key Insight

This project demonstrates how improving the **retrieval layer** — from keyword matching to semantic search — significantly enhances the accuracy and reliability of LLM-generated responses.

---

## 👩‍💻 Author

Disha Verma
BTech 
Web Developer | AI Engineer

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
