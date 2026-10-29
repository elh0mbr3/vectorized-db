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
  
  # Returns a string of vectors
  def __str__(self):
    return f"{self.master_vocabulary} <> {self.vectors}"
  
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
  def search(self, search_input: str) -> dict:
    processed_query: list = process_words(search_input)
    query_vector: Vector = build_vector(self.master_vocabulary, processed_query, name="search_query")
    
    sorted_dict: dict = {}
    temp: list = []
    
    for doc_name, data in self.vectors.items():
      cosine: float = data["vector"].cosine_similarity(query_vector)
      temp.append((doc_name, cosine))
      
    temp = sorted(temp, key=lambda x: x[1], reverse=True)
    
    for v in temp:
      sorted_dict[v[0]] = v[1]
    return sorted_dict