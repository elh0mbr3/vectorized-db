# that's main.py

# Imports
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from vectorized_db.vectordb import VectorDB
from vectorized_db.file_handler import load_vectors, store_vectors, db_path
import uvicorn
import os

# Checks before loading since load_vectors() creates an empty database when no file exists
is_first_run: bool = not os.path.exists(db_path)

vector_db: VectorDB = load_vectors()
print(f"Total documents loaded: {len(vector_db.vectors)}")

# Auto-loads startup files for fresh installs
if is_first_run:
  current_dir = os.path.dirname(os.path.abspath(__file__))
  samples_dir = os.path.join(current_dir, "sample_docs")
  
  # Safely creates the folder if it doesn't exist
  os.makedirs(samples_dir, exist_ok=True)
  
  for filename in os.listdir(samples_dir):
    if filename.endswith((".txt", ".md")):
      file_path = os.path.join(samples_dir, filename)
      with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        vector_db.ingest(os.path.splitext(filename)[0], content)
        print(f"Auto-loaded test file: {filename}")
  
  store_vectors(vector_db)

app: FastAPI = FastAPI()

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

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
  content = await file.read()
  text_input = content.decode("utf-8")
  # Strips extension based on file type:
  if file.filename.endswith(".txt"):
    doc_name = file.filename.replace(".txt", "")
  else:
    doc_name = file.filename.replace(".md", "")
  vector_db.ingest(doc_name, text_input)
  store_vectors(vector_db)
  return {"message": "Success"}

@app.delete("/api/delete")
async def delete_document(doc_name: str):
  # Checks if document exists
  if doc_name not in vector_db.vectors:
    raise HTTPException(status_code=404, detail="Document not found")
  
  # Removes the document vector
  del vector_db.vectors[doc_name]
  
  # Saves the updated state to disk to ensure the deletion persists across reboots
  store_vectors(vector_db)
  
  return {"message": f"Successfully deleted {doc_name}"}

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
  
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

def start_server():
  uvicorn.run("vectorized_db.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
  start_server()