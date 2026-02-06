"""
Sentence Transformers embedding service for RAG.
Uses free, local embeddings - no API calls required.
"""
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:
    """Generate embeddings using Sentence Transformers (free, local)."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model.
        
        Args:
            model_name: Sentence Transformers model (default: all-MiniLM-L6-v2)
                       - 384 dimensions
                       - Fast inference
                       - Good quality for RAG
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"✓ Model loaded successfully (dimension: {self.model.get_sentence_embedding_dimension()})")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient).
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings.tolist()
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.model.get_sentence_embedding_dimension()
