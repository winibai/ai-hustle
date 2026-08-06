#!/usr/bin/env python3
"""
Simple ingestion script:
- Reads .md files from a docs directory
- Splits text into chunks
- Calls OpenAI embeddings API
- Stores vectors into local Chroma DB (./chroma_db)

Usage:
  export OPENAI_API_KEY="..."
  python kb-starter/ingest.py --docs_dir kb-starter/docs

Note: for large production ingestion use more robust chunking and batching.
"""

import os
import argparse
import glob
import json
import time

try:
    import openai
except Exception as e:
    print("Missing dependency 'openai'. Install with: pip install openai")
    raise

try:
    import chromadb
    from chromadb.config import Settings
except Exception as e:
    print("Missing dependency 'chromadb'. Install with: pip install chromadb")
    raise

# Simple splitter by paragraph with max token/char approx limits
def chunk_text(text, max_chars=1000):
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    cur = ""
    for p in paragraphs:
        if len(cur) + len(p) + 2 <= max_chars:
            cur = (cur + "\n\n" + p).strip()
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    return chunks


def embed_texts(texts, model):
    # openai.Embedding.create supports batch input as list
    resp = openai.Embedding.create(input=texts, model=model)
    vectors = [r['embedding'] for r in resp['data']]
    return vectors


def main(docs_dir, embedding_model):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set. Export it before running.")
        return
    openai.api_key = api_key

    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
    col_name = "kb_collection"
    try:
        collection = client.get_collection(col_name)
        print(f"Found existing collection '{col_name}'")
    except Exception:
        collection = client.create_collection(name=col_name)
        print(f"Created collection '{col_name}'")

    files = glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True)
    print(f"Found {len(files)} markdown files in {docs_dir}")

    ids = []
    metadatas = []
    documents = []
    vectors = []

    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            text = f.read()
        chunks = chunk_text(text)
        for i, c in enumerate(chunks):
            doc_id = f"{os.path.basename(fp)}::chunk-{i}"
            ids.append(doc_id)
            metadatas.append({"source": fp, "chunk_index": i})
            documents.append(c)

    # Batch embedding in smaller chunks to avoid very large requests
    batch_size = 16
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        print(f"Embedding batch {i}..{i+len(batch)-1}")
        vecs = embed_texts(batch, embedding_model)
        vectors.extend(vecs)
        time.sleep(0.2)

    # Upsert into chroma
    print(f"Upserting {len(ids)} vectors into Chroma collection '{col_name}'")
    collection.add(ids=ids, embeddings=vectors, metadatas=metadatas, documents=documents)
    client.persist()
    print("Done. Chroma DB persisted at ./chroma_db")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--docs_dir', default='kb-starter/docs')
    parser.add_argument('--embedding_model', default=os.environ.get('EMBEDDING_MODEL', 'text-embedding-3-small'))
    args = parser.parse_args()
    main(args.docs_dir, args.embedding_model)
