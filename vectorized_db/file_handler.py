from vectorized_db.vectordb import VectorDB
from vectorized_db.vector import Vector
import os
import json

# Stores the database in the user's home folder
db_dir = os.path.join(os.path.expanduser("~"), ".vectorized_db")
db_path = os.path.join(db_dir, "vectors.json")

# Stores VectordDB.vectors in a json file
def store_vectors(vector_db: VectorDB):
  # Safely created the database directory if it was deleted or never existed
  os.makedirs(db_dir, exist_ok=True)
  
  # Redefines Python dictionaries as JSON object
  export_data: dict = {}
  export_data["master_vocabulary"] = sorted(vector_db.master_vocabulary)
  safe_vectors: dict = {}
  for name, vectors in vector_db.vectors.items():
    safe_vectors[name] = {"text": vectors["text"], "numbers": vectors["vector"].entries}
  export_data["documents"] = safe_vectors
  
  # Saves to the absolute path
  with open(file=db_path, mode="w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=1)

# Converts content from .txt file into a Python string
def convert_text(file_path: str = "") -> str:
  if file_path == "":
    raise FileNotFoundError
  with open(file=file_path, mode="r", encoding="utf-8") as f:
    return f.read()
  
# Loads vectors into a program
def load_vectors() -> VectorDB:
  try:
    # Uses the absolute path instead of a hardcoded string
    with open(file=db_path, mode="r", encoding="utf-8") as f:
      vector_db = VectorDB()
      dictionary = dict(json.load(f))
      master_vocabulary: set = set(dictionary["master_vocabulary"])
      vector_db.master_vocabulary = master_vocabulary
      for doc_name, data in dictionary["documents"].items():
        processed_text = data["text"]
        raw_numbers = data["numbers"]
        integer_numbers: list[int] = []
        for number in raw_numbers:
          integer_numbers.append(int(number))
        vector: Vector = Vector(entries=integer_numbers)
        vector_db.vectors[doc_name] = {"text": processed_text, "vector": vector}
      return vector_db
  except FileNotFoundError:
    print("No existing database found. Initialising a new database")
    return VectorDB()
  
    