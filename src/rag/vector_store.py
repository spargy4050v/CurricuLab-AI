"""
ChromaDB vector store for curriculum knowledge base.
Persistent, local, free vector database.
"""
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
import os


class CurriculumVectorStore:
    """ChromaDB-based vector store for curriculum examples."""
    
    def __init__(self, persist_directory: str = "./data/vector_db"):
        """
        Initialize ChromaDB vector store.
        
        Args:
            persist_directory: Directory for persistent storage
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="curriculum_knowledge_base",
            metadata={"description": "Educational curriculum examples and templates"}
        )
        
        print(f"✓ ChromaDB initialized at: {persist_directory}")
        print(f"  Collection: {self.collection.name}")
        print(f"  Documents: {self.collection.count()}")
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ):
        """
        Add curriculum documents to vector store.
        
        Args:
            documents: List of curriculum text documents
            metadatas: Optional metadata for each document
            ids: Optional custom IDs (auto-generated if not provided)
        """
        if ids is None:
            # Auto-generate IDs
            existing_count = self.collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{}] * len(documents)
        
        # ChromaDB automatically generates embeddings
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✓ Added {len(documents)} documents to vector store")
    
    def similarity_search(
        self,
        query: str,
        k: int = 3,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar curriculum documents.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of matching documents with metadata and scores
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None,
                    'id': results['ids'][0][i] if results['ids'] else None
                })
        
        return formatted_results
    
    def get_count(self) -> int:
        """Get total number of documents in vector store."""
        return self.collection.count()
    
    def clear(self):
        """Clear all documents from vector store."""
        self.client.delete_collection(name="curriculum_knowledge_base")
        self.collection = self.client.create_collection(
            name="curriculum_knowledge_base",
            metadata={"description": "Educational curriculum examples and templates"}
        )
        print("✓ Vector store cleared")
