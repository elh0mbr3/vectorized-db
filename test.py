# that's test.py - will be later rewritten to apply TDD (Test-Driven Development) standards

# Import
from vector import Vector
from vectordb import VectorDB
from embedder import process_words, unique_set, build_vector

# Testing vector methods and attributes:
# vector1 = Vector([1.5, 3.4, 1.7])
# vector2 = Vector([2.1, 4.7, 3.8])
# print(vector1.dot_product(vector2))
# vector3 = vector1.add(vector2)
# print(vector3)
# vector3.multiply_by(3)
# print(vector3)
# print(vector1.magnitude)
# print(vector1.unit_vector())
# Passes all cases

# will throw DifferentDimensionsError:
# vector4 = Vector([5, 4, 3, 1])
# vector5 = Vector([3, 2])
# print(vector4.add(vector5))

# Testing cosine_similarity():
# vector10, vector11 = Vector([0.0, 0.0]), Vector([1.0, 2.0])
# print(vector10.cosine_similarity(vector11))
# Passes all cases

# Case 1: Empty initialisation
vectordb1 = VectorDB({})
print(vectordb1)

# Case 2: Pre-loaded initialisation
vectordb2 = VectorDB({
  "test": [1.5, 1.7, 5.2]
})
print(vectordb2)

# Case 3: Ingest representation
vectordb3 = VectorDB({})
vectordb3.ingest(Vector("x", [5.6, 4.2, 7.9]))
print(vectordb3)

vectordb4 = VectorDB({
  "test1": Vector("x", [6.7, 4.4, 3.2]),
  "test2": Vector("y", [8.9, 2.2, 1.6]),
  "test3": Vector("z", [5.6, 2.3, 4.3])
})

print(vectordb4.search(Vector("u", [3.5, 6.6, 1.2])))

string: str = "Python is fast, but C is faster!"

process_words(string)
vector1: Vector = build_vector(unique_set(process_words(string)), process_words(string))
print(Vector)