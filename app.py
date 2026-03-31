

import os
import glob
from pathlib import Path

import gradio as gr
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. Setup


load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"OpenAI API Key exists and begins with: {api_key[:8]}")
else:
    raise ValueError("OPENAI_API_KEY not found in .env")

MODEL = "gpt-4.1-nano"
DB_NAME = "chroma_db"

client = OpenAI()


# 2. Inspect raw knowledge base


knowledge_base_path = "knowledge-base/**/*.md"
files = glob.glob(knowledge_base_path, recursive=True)
print(f"Found {len(files)} files in the knowledge base")

entire_knowledge_base = ""

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        entire_knowledge_base += f.read()
        entire_knowledge_base += "\n\n"

print(f"Total characters in knowledge base: {len(entire_knowledge_base):,}")

encoding = tiktoken.encoding_for_model(MODEL)
tokens = encoding.encode(entire_knowledge_base)
token_count = len(tokens)
print(f"Total tokens for {MODEL}: {token_count:,}")


# 3. Load documents using LangChain


folders = glob.glob("knowledge-base/*")
documents = []

for folder in folders:
    doc_type = os.path.basename(folder)

    loader = DirectoryLoader(
        folder,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    folder_docs = loader.load()

    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type
        doc.metadata["source_file"] = Path(doc.metadata.get("source", "")).name
        documents.append(doc)

print(f"Loaded {len(documents)} documents")


# 4. Split into chunks


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"Divided into {len(chunks)} chunks")
if chunks:
    print("Sample chunk metadata:", chunks[0].metadata)
    print("Sample chunk preview:", chunks[0].page_content[:300])


# 5. Create embeddings


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# Alternative:
# from langchain_openai import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


# 6. Create / rebuild Chroma vector store


if os.path.exists(DB_NAME):
    try:
        Chroma(
            persist_directory=DB_NAME,
            embedding_function=embeddings
        ).delete_collection()
        print("Existing Chroma collection deleted")
    except Exception as e:
        print("No previous collection deleted:", e)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_NAME
)

print(f"Vectorstore created with {vectorstore._collection.count()} chunks")


# 7. Inspect embedding dimensions


collection = vectorstore._collection
count = collection.count()

sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
dimensions = len(sample_embedding)

print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")


# 8. Retrieval function


def retrieve_relevant_chunks(query, top_k=3):
    results = vectorstore.similarity_search(query, k=top_k)
    return results


# 9. Build context from retrieved chunks


def build_context(query, top_k=3):
    relevant_chunks = retrieve_relevant_chunks(query, top_k=top_k)

    if not relevant_chunks:
        return "No relevant context was found in the knowledge base."

    context_parts = []

    for i, chunk in enumerate(relevant_chunks, start=1):
        context_parts.append(
            f"[Chunk {i}]\n"
            f"Source Type: {chunk.metadata.get('doc_type', 'unknown')}\n"
            f"Source File: {chunk.metadata.get('source_file', 'unknown')}\n"
            f"Content:\n{chunk.page_content}"
        )

    return "\n\n".join(context_parts)


# 10. Prompt


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


# 11. Chat function


def chat(message, history):
    context = build_context(message, top_k=3)

    messages = [
        {
            "role": "system",
            "content": f"{SYSTEM_PROMPT}\n\nRelevant context:\n{context}"
        }
    ]

    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content


# 12. Launch Gradio app


demo = gr.ChatInterface(
    fn=chat,
    title="Insurellm RAG Assistant",
    description="Ask questions about employees and products from the knowledge base."
)

demo.launch(inbrowser=True)