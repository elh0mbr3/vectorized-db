# Imports
# from math import cos <- can be used for later
# from math import sin <- can be used for later
from math import sqrt
from math import pow

class DifferentDimensionsError(Exception):
  pass

# A vector class
class Vector:
  entries: list
  magnitude: float
  
  # Initialises a vector object
  def __init__(self, entries: list):
    self.entries = entries
    self.magnitude = self.calculate_magnitude()
  
  # Overrides __str__ method to return a string of vector entries without using .entries attribute
  def __str__(self):
    return f"{self.entries}"   
  
  # Returns the number of vector entries (should be int)
  def get_size(self) -> int:
    return len(self.entries)
  
  # Calculates a dot product (scalar value)
  def dot_product(self, vector) -> float:
    if self.get_size() != vector.get_size():
      raise DifferentDimensionsError("Vectors appear to have different number of dimensions.")
    sum: float = 0.0
    for i in range(0, self.get_size()):
      sum += self.entries[i] * vector.entries[i]
    return sum 
  
  # Adds two vectors and returns a new vector
  def add(self, vector):
    if self.get_size() != vector.get_size():
      raise DifferentDimensionsError("Vectors appear to have different number of dimensions.")
    temp: list = []
    for i in range(0, self.get_size()):
      temp.append(self.entries[i] + vector.entries[i])
    return Vector(temp)
  
  # Multiplies vector entries by a scalar number
  def multiply_by(self, scalar: float):
    temp: list = []
    for entry in self.entries:
      entry *= scalar
      temp.append(entry)
    return Vector(temp)
    
  # Returns a magnitude value
  def calculate_magnitude(self) -> float:
    temp: list = []
    sum: float = 0.0
    for entry in self.entries:
      sum += pow(entry, 2)
    return sqrt(sum)
  
  # Returns a unit vector
  def unit_vector(self):
    temp: list = []
    for entry in self.entries:
      temp.append(entry / self.magnitude)
    return Vector(temp)
  
  # Returns the angle between two vectors
  def cosine_similarity(self, vector) -> float:
    if self.get_size() != vector.get_size():
      raise DifferentDimensionsError("Vectors appear to have different number of dimensions.")
    dot_product: float = self.dot_product(vector)
    combined_magnitude: float = self.magnitude * vector.magnitude
    if combined_magnitude == 0:
      return 0.0
    return dot_product / combined_magnitude