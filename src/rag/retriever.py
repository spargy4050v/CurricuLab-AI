"""
RAG retriever for curriculum generation.
Combines vector search with context formatting.
"""
from typing import List, Dict
from src.rag.vector_store import CurriculumVectorStore


class CurriculumRetriever:
    """RAG retrieval logic for curriculum examples."""
    
    def __init__(self, vector_store: CurriculumVectorStore):
        """
        Initialize retriever.
        
        Args:
            vector_store: ChromaDB vector store instance
        """
        self.vector_store = vector_store
    
    def retrieve_similar_curricula(
        self,
        skill: str,
        level: str,
        k: int = 3
    ) -> List[Dict]:
        """
        Retrieve similar curriculum examples.
        
        Args:
            skill: Subject/skill area
            level: Education level
            k: Number of examples to retrieve
            
        Returns:
            List of relevant curriculum examples
        """
        # Construct search query
        query = f"Create a {level} curriculum for {skill}"
        
        # Try to filter by level if possible
        try:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter_metadata={"level": level}
            )
            
            # If no results with filter, search without filter
            if not results:
                results = self.vector_store.similarity_search(query=query, k=k)
        except:
            # Fallback to unfiltered search
            results = self.vector_store.similarity_search(query=query, k=k)
        
        return results
    
    def format_context_for_llm(self, retrieved_docs: List[Dict]) -> str:
        """
        Format retrieved documents as context for LLM.
        
        Args:
            retrieved_docs: Retrieved curriculum examples
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return "No similar curriculum examples found."
        
        context_parts = ["Here are some similar curriculum examples for reference:\n"]
        
        for i, doc in enumerate(retrieved_docs, 1):
            metadata = doc.get('metadata', {})
            content = doc.get('content', '')
            
            context_parts.append(f"\n--- Example {i} ---")
            if metadata:
                context_parts.append(f"Level: {metadata.get('level', 'N/A')}")
                context_parts.append(f"Subject: {metadata.get('subject', 'N/A')}")
            context_parts.append(f"\n{content}\n")
        
        return "\n".join(context_parts)
