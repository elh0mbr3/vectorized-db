![](vectorized_db/static/Vectorized-DB.png)

# VectorizedDB
A lightweight, custom-built vector database written in Python. This side project stores mathematical representations of text (vectors) to power similarity search and keyword comparison.

## Getting started

Requires Python 3.10 or newer.

```bash
git clone https://github.com/elh0mbr3/vectorized-db.git
cd vectorized-db
pip install .
vectordb-ui
```

Then open http://127.0.0.1:8000 in your browser.

On the first run, a few sample documents are loaded so you can try searching right away.
Your data is saved in a `.vectorized_db` folder in your home directory.

## How it works
1. **Text processing.** Each document is lowercased, punctuation is removed, and common stop words ("the", "and", "is", etc.) are filtered out.
2. **Vocabulary.** Every unique word across all documents becomes one dimension in a shared vocabulary.
3. **Vectors.** Each document becomes a list of numbers: how many times each vocabulary word appears in it. This is called a *bag-of-words* model.
4. **Search.** The query is turned into a vector the same way, then compared with every document using **cosine similarity**, the cosine of the angle between two vectors. A score of 1 means the same direction (very similar), and 0 means no shared words.

The vector math (dot product, magnitude, cosine similarity) is implemented from scratch in `vectorized_db/vector.py`, without any advanced math or ML libraries.