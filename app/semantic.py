# app/semantic.py
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_model():
    return SentenceTransformer(MODEL_NAME)

def embed_texts(texts, model):
    """Create embeddings for a list of texts"""
    if not texts:
        raise ValueError("No texts provided for embedding")
    try:
        embeddings = model.encode(texts, convert_to_numpy=True)
        if embeddings.ndim != 2:
            raise ValueError(f"Unexpected embedding shape: {embeddings.shape}")
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Error creating embeddings: {str(e)}")

def build_faiss_index(embeddings):
    """Build FAISS index from embeddings"""
    if embeddings is None or len(embeddings) == 0:
        raise ValueError("No embeddings provided to build index")
        
    try:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index
    except Exception as e:
        raise RuntimeError(f"Error building FAISS index: {str(e)}")

def save_index(index, path):
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        faiss.write_index(index, path)
    except Exception as e:
        raise RuntimeError(f"Failed to save index to {path}: {str(e)}")

def load_index(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Index file not found at {path}")
    try:
        return faiss.read_index(path)
    except RuntimeError as e:
        raise RuntimeError(f"Failed to read the index file. Error: {str(e)}")
