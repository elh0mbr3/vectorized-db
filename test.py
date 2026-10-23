# that's test.py

# Import
from vector import Vector

vector1 = Vector([1, 3, 1])
vector2 = Vector([2, 4, 3])
print(vector1.dot_product(vector2))
vector3 = vector1.add(vector2)
print(vector3)
vector3.multiply_by(3)
print(vector3)
print(vector1.magnitude)
print(vector1.unit_vector())