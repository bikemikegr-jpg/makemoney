import os
from argparse import ArgumentParser
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

def ingest_directory(path: str):
    docs = []
    for root, _, files in os.walk(path):
        for fname in files:
            if fname.lower().endswith((".txt", ".md")):
                full = os.path.join(root, fname)
                loader = TextLoader(full, encoding="utf-8")
                dd = loader.load()
                for d in dd:
                    d.metadata["source"] = full
                docs.extend(dd)

    if not docs:
        print("No text or markdown files found to ingest.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)
    vectordb.persist()
    print(f"Ingested {len(chunks)} chunks into {PERSIST_DIR}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path", required=True, help="Path to directory with text/markdown files")
    args = parser.parse_args()
    ingest_directory(args.path)
