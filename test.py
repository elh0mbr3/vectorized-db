# that's test.py - will be later rewritten to apply TDD (Test-Driven Development) standards

# Import
from vector import Vector

vector1 = Vector([1.5, 3.4, 1.7])
vector2 = Vector([2.1, 4.7, 3.8])
print(vector1.dot_product(vector2))
vector3 = vector1.add(vector2)
print(vector3)
vector3.multiply_by(3)
print(vector3)
print(vector1.magnitude)
print(vector1.unit_vector())

# will throw DifferentDimensionsError:
# vector4 = Vector([5, 4, 3, 1])
# vector5 = Vector([3, 2])
# print(vector4.add(vector5))

# Testing cosine_similarity():
# vector10, vector11 = Vector([0.0, 0.0]), Vector([1.0, 2.0])
# print(vector10.cosine_similarity(vector11))
# Passes all cases