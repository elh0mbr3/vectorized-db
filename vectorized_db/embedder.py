import re
from vectorized_db.vector import Vector

# Returns a list of split words from a given string input
def process_words(words: str) -> list:
  # Phase 1 - lowercasing
  lowercased: str = words.lower()
    
  # Phase 2 - punctuation removal (using regex)
  new_lowercased: str = re.sub(r"[!,.;?]+", "", lowercased)
    
  # Phase 3 - splitting
  new_words = new_lowercased.split()
  return new_words

# Returns a set of unique words removing duplicates
def unique_set(word_list: list) -> set:
  return set(word_list)

# Returns a vector built of counters of unique words appearing in a list of words
def build_vector(word_set: set, word_list: list, name: str = "") -> Vector:
  numbers: list[int] = []
  sorted_set = sorted(word_set)
  for word in sorted_set:
    numbers.append(word_list.count(word))
  print(numbers)
  return Vector("x", numbers)