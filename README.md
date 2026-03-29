# 🧠 Insurellm Mini RAG System

A **simple Retrieval-Augmented Generation (RAG)** system built using **Python, OpenAI, and Gradio**, designed to answer questions about company **employees** and **products** using a local knowledge base.

---

## 🚀 Overview

This project demonstrates a **basic RAG pipeline**:

1. Load documents from local knowledge base
2. Retrieve relevant documents based on user query
3. Inject context into prompt
4. Generate response using LLM

It is designed as a **learning + interview-ready project** for understanding how RAG systems work before moving to vector databases.

---

## 🏗️ Project Structure

```
rag_assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
└── knowledge-base/
    ├── employees/
    │   ├── avery_lancaster.md
    │   └── ...
    └── products/
        ├── claimllm.md
        └── ...
```

---

## ⚙️ Features

* 🔍 Keyword-based document retrieval
* 📂 Multiple knowledge sources (employees + products)
* 🧾 Markdown (`.md`) support
* 🧠 Context-aware LLM responses
* 💬 Interactive UI using Gradio
* ❌ Safe fallback when answer is unknown

---

## 🧪 Example Queries

* "Who is Avery Lancaster?"
* "What does Claimllm do?"


---

## 🛠️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/insurellm-rag.git
cd insurellm-rag
```

---

### 2. Create virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Add OpenAI API Key

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

### 5. Run the application

```
python app.py
```

App will open in browser automatically.

---

## 📚 Knowledge Base Format

### Employees Example (`employees/alex_lancaster.md`)

```
# Avery Lancaster
Avery Lancaster co-founded Insurellm in 2015 and has since guided the company to its current position as a leading Insurance Tech provider.
```

---

### Products Example (`products/claimgenius.md`)

```
# Claimllm
Claimllm is Insurellm's revolutionary claims processing platform that transforms the claims experience for insurers, adjusters, and policyholders.
```

---

## 🧠 How It Works

### 1. Document Loading

* Reads `.md` files
* Stores metadata (title, source, content)

### 2. Retrieval

* Tokenizes user query
* Matches against document content + title
* Scores relevance
* Selects top-k documents

### 3. Prompt Construction

* Injects retrieved documents into system prompt
* Adds structured context

### 4. LLM Response

* Uses OpenAI model (`gpt-4.1-nano`)
* Returns concise, factual answers

---

## ⚠️ Limitations (Current Version)

* No embeddings (keyword-based retrieval only)
* No vector database
* Limited semantic understanding
* No chunking for large documents

---

## 🚀 Future Improvements

* 🔹 Add embeddings (OpenAI / HuggingFace)
* 🔹 Use vector DB (FAISS / Chroma / pgvector)
* 🔹 Implement document chunking
* 🔹 Add reranking
* 🔹 Add citations in responses
* 🔹 Add conversation-aware retrieval

---

## 💡 Why This Project Matters

This project demonstrates:

* Core understanding of **RAG architecture**
* Prompt engineering with context injection
* Handling structured knowledge bases
* Building AI-powered apps with UI

---

## 🧠 Tech Stack

* Python
* OpenAI API
* Gradio
* dotenv

---

## 🧑‍💻 Author

Disha Verma
BTech 
Web Developer | AI Engineer

---

## ⭐ If you found this useful

Give this repo a ⭐ and feel free to contribute!

---
