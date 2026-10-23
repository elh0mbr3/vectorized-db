# Imports
from vector import Vector

# A vector database class
class VectorDB:
  vectors: dict
  
  # Initialises a vector database object
  def __init__(self, vectors):
    self.vectors = vectors
  
  # Returns a string of vectors
  def __str__(self):
    return f"{self.vectors}"
  
  # Adds a key-value element of vectors dictionary
  def ingest(self, name: str, vector):
    self.vectors[name] = vector
  
  # Returns a vector without removing it from the dictionary
  def get(self, name) -> Vector:
    return self.vectors[name]
  
  # Removes and returns a vector
  def pop(self, name) -> Vector:
    return self.vectors.pop(name)