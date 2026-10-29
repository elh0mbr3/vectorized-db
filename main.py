# that's main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vectordb import VectorDB
from file_handler import load_vectors
import uvicorn

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
  
if __name__ == "__main__":
  uvicorn.run(app=app, host="localhost", port=8000)