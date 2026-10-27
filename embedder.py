import re

def process_words(input: str) -> list:
  # Phase 1 - lowercasing
  lowercased: str = input.lower()
    
  # Phase 2 - punctuation removal (using regex)
  new_lowercased: str = re.sub(r"[!,.;?]+", "", lowercased)
    
  # Phase 3 - splitting
  new_words = new_lowercased.split()
  print(new_words) # for debugging
  return new_words