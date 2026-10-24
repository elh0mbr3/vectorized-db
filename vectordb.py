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
  
  # Adds a key-value element of vectors list
  def ingest(self, vector: Vector):
    self.vectors[vector.name] = vector
  
  # Returns a vector without removing it from the list
  def get(self, name:str) -> Vector:
    return self.vectors.get(name)
  
  # Removes and returns a vector
  def pop(self, name: str) -> Vector:
    return self.vectors.pop(name)
  
  # Returns a dictionary of sorted key-value elements depending how similar they are to an input query
  def search(self, vector: Vector) -> dict:
    sorted: dict = {}
    temp: list = []
    for v in self.vectors.values():
      cosine: float = v.cosine_similarity(vector)
      temp.append(tuple((v, cosine)))
    for i in range(0, len(temp) - 1):
      for j in range(i+1, len(temp)):
        if temp[i][1] < temp[j][1]:
          swap = temp[i]
          temp[i] = temp[j]
          temp[j] = swap
    for v in temp:
      sorted[v[0]] = v[1]
    return sorted