import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

def _get_vectordb():
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return vectordb

def get_answer(query: str, k: int = 4) -> str:
    vectordb = _get_vectordb()
    retriever = vectordb.as_retriever(search_kwargs={"k": k})

    llm = ChatOpenAI(model_name=LLM_MODEL, temperature=0.2)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    result = qa({"query": query})
    answer = result.get("result") or result.get("answer") or ""
    return answer
