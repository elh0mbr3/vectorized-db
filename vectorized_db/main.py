# that's main.py

# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from vectorized_db.vectordb import VectorDB
from vectorized_db.file_handler import load_vectors
import uvicorn
import os

vector_db: VectorDB = load_vectors()
print(f"Total documents loaded: {len(vector_db.vectors)}")

app: FastAPI = FastAPI()
app.add_middleware(CORSMiddleware, allow_methods=["*"], allow_credentials=True, allow_origins=["*"], allow_headers=["*"])


@app.get("/api/status")
def return_status():
  return {"status": "online"}

@app.get(path="/api/vectors")
def load_dictionary():
  export_data: dict = {"master_vocabulary": list(vector_db.master_vocabulary)}
  document_vectors: dict = {}
  for doc_name, data in vector_db.vectors.items():
    document_vectors[doc_name] = data["vector"].entries
  export_data["vector"] = document_vectors
  return export_data

@app.get(path="/api/search")
def search(search_input: str):
  return vector_db.search(search_input)

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
  
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

def start_server():
  uvicorn.run("vectorized_db.main:app", host="localhost", port=8000, reload=False)

if __name__ == "__main__":
  start_server()