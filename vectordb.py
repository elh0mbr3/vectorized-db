# Imports
from vector import Vector
from embedder import unique_set, build_vector, process_words

# A vector database class
class VectorDB:
  vectors: dict[str, dict]
  master_vocabulary: set[str]
  
  # Initialises a vector database object
  def __init__(self, vectors=None):
    if vectors == None:
      self.vectors = {}
    else:
      self.vectors = vectors
    self.master_vocabulary = set()
  
  # Returns a string Sof vectors
  def __str__(self):
    return f"{self.vectors}"
  
  # Adds a string to process it and adds it to a master_vocabulary
  def ingest(self, name: str, text_input: str):
    processed_text: list = process_words(text_input)
    words: set = unique_set(processed_text)
    self.master_vocabulary.update(words)
    self.vectors[name] = {"text": processed_text, "vector": None}
    for i, j in self.vectors.items():
      vector: Vector = build_vector(self.master_vocabulary, j["text"], name=i)
      self.vectors[i] = {"text": j["text"], "vector": vector}
  
  # Returns a vector without removing it from the list
  def get(self, name:str) -> Vector:
    return self.vectors.get(name).get("vector")
  
  # Removes and returns a vector
  def pop(self, name: str) -> Vector:
    return self.vectors.pop(name).pop("vector")
  
  # Returns a dictionary of sorted key-value elements depending how similar they are to an input query
  def search(self, vector: Vector) -> dict:
    sorted: dict = {}
    temp: list = []
    for v in self.vectors.values():
      cosine: float = v["vector"].cosine_similarity(vector)
      temp.append(tuple((v["vector"], cosine)))
    for i in range(0, len(temp) - 1):
      for j in range(i+1, len(temp)):
        if temp[i][1] < temp[j][1]:
          swap = temp[i]
          temp[i] = temp[j]
          temp[j] = swap
    for v in temp:
      sorted[v[0]] = v[1]
    return sorted