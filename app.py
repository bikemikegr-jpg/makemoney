import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import get_answer
from ingest import ingest_directory

load_dotenv()

app = FastAPI(title="Personal AI (prototype)")

class IngestRequest(BaseModel):
    path: str

class ChatRequest(BaseModel):
    query: str
    k: int = 4

@app.post("/ingest")
def ingest(req: IngestRequest):
    path = req.path
    if not os.path.exists(path):
        raise HTTPException(status_code=400, detail="Path not found")
    ingest_directory(path)
    return {"status": "ingested", "path": path}

@app.post("/chat")
def chat(req: ChatRequest):
    resp = get_answer(req.query, k=req.k)
    return {"answer": resp}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
