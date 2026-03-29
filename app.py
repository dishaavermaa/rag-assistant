import os
import re
import glob
from pathlib import Path
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI


# 1. Setup


load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"OpenAI API Key exists and begins with: {api_key[:8]}")
else:
    raise ValueError("OPENAI_API_KEY not found in .env")

MODEL = "gpt-4.1-nano"
client = OpenAI()


# 2. Load knowledge bases


knowledge_base = []

def load_documents(folder_path, source_type):
    files = glob.glob(f"{folder_path}/*.md")
    docs = []

    for filepath in files:
        filename = Path(filepath).stem
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        docs.append({
            "id": filename.lower(),
            "title": filename,
            "source": source_type,   # employees or products
            "content": content
        })

    return docs

employee_docs = load_documents("knowledge-base/employees", "employees")
product_docs = load_documents("knowledge-base/products", "products")

knowledge_base.extend(employee_docs)
knowledge_base.extend(product_docs)

print(f"Loaded {len(employee_docs)} employee docs")
print(f"Loaded {len(product_docs)} product docs")
print(f"Total docs loaded: {len(knowledge_base)}")


# 3. Utility functions


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text):
    return set(normalize_text(text).split())


# 4. Retrieval


def score_document(query, doc):
    query_tokens = tokenize(query)
    content_tokens = tokenize(doc["content"])
    title_tokens = tokenize(doc["title"])

    # Score based on token overlap
    content_overlap = len(query_tokens.intersection(content_tokens))
    title_overlap = len(query_tokens.intersection(title_tokens))

    # Give more importance to title matches
    score = content_overlap + (2 * title_overlap)
    return score

def retrieve_relevant_docs(query, top_k=3):
    scored_docs = []

    for doc in knowledge_base:
        score = score_document(query, doc)
        if score > 0:
            scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [doc for score, doc in scored_docs[:top_k]]


# 5. Build additional context


def build_context(query, top_k=3):
    relevant_docs = retrieve_relevant_docs(query, top_k=top_k)

    if not relevant_docs:
        return "No relevant context was found in the knowledge base."

    context_parts = []
    for i, doc in enumerate(relevant_docs, start=1):
        context_parts.append(
            f"[Document {i}]\n"
            f"Source: {doc['source']}\n"
            f"Title: {doc['title']}\n"
            f"Content:\n{doc['content']}"
        )

    return "\n\n".join(context_parts)


# 6. Prompt

SYSTEM_PROMPT = """
You are Insurellm, the Insurance Tech company assistant.

You answer questions about:
1. company employees
2. company products

Rules:
- Use the provided context if it is relevant.
- If the answer is not clearly present in the context, say you do not know.
- Do not invent employee details or product details.
- Keep answers brief, clear, and accurate.
"""


# 7. Chat function


def chat(message, history):
    context = build_context(message, top_k=3)

    messages = [
        {
            "role": "system",
            "content": f"{SYSTEM_PROMPT}\n\nRelevant context:\n{context}"
        }
    ]

    # Gradio ChatInterface with type="messages" gives history as structured messages
    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content


# 8. Launch UI


demo = gr.ChatInterface(
    fn=chat,
    # type="messages",
    title="Insurellm Mini RAG",
    description="Ask about employees and products from the local knowledge base."
)

demo.launch(inbrowser=True)