import faiss
import numpy as np
import pickle
from .config import INDEX_PATH, CHUNKS_PATH

class VectorStore:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = None
        self.chunks = []

    def add(self, embeddings, chunks):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings))
        self.chunks = chunks

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(CHUNKS_PATH, "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            self.chunks = pickle.load(f)

    def search(self, query_embedding, k=3):
        if self.index is None:
            return []
        D, I = self.index.search(np.array(query_embedding), k)
        return [self.chunks[i] for i in I[0]]
