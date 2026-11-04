import re
import os
from vectorized_db.vector import Vector

# Gets the path to the folder where embedder.py is
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "stopwords.txt")

# Phase 0 - stop words
with open(file_path, "r", encoding="utf-8") as file:
  raw_stopwords = file.read()
STOPWORDS_SET = set(raw_stopwords.replace(",", "").split())

# Returns a list of split words from a given string input
def process_words(words: str) -> list:
  
  # Phase 1 - lowercasing
  lowercased: str = words.lower()
    
  # Phase 2 - punctuation removal (using regex)
  new_lowercased: str = re.sub(r"[!,.;:?_*#>\'\"\(\)\[\]]+", "", lowercased)
    
  # Phase 3 - splitting and filtering
  raw_words = new_lowercased.split()
  new_words = [word for word in raw_words if word not in STOPWORDS_SET]
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
  return Vector("x", numbers)