from vectordb import VectorDB
from vector import Vector
import json

# Stores VectordDB.vectors in a json file
def store_vectors(vector_db: VectorDB):
  export_data: dict = {}
  export_data["master_vocabulary"] = list(vector_db.master_vocabulary)
  safe_vectors: dict = {}
  for name, vectors in vector_db.vectors.items():
    safe_vectors[name] = {"text": vectors["text"], "numbers": vectors["vector"].entries}
  export_data["documents"] = safe_vectors
  with open(file="database/vectors.json", mode="w") as f:
    f.write(json.dumps(obj=export_data, indent=1))

# Converts content from .txt file into a Python string
def convert_text(file_path: str = "") -> str:
  if file_path == "":
    raise FileNotFoundError
  with open (file=file_path, mode="r") as f:
    return f.read()
  
# Loads vectors into a program
def load_vectors() -> VectorDB:
  with open(file="database/vectors.json", mode="r") as f:
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
      vector: Vector = Vector(name=doc_name, entries=integer_numbers)
      vector_db.vectors[doc_name] = {"text": processed_text, "vector": vector}
    return vector_db
  
    