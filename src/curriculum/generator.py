"""
Main curriculum generator orchestrator.
Combines RAG retrieval + LLM generation.
"""
import json
from typing import Optional
from src.curriculum.models import CurriculumRequest, Curriculum
from src.rag.vector_store import CurriculumVectorStore
from src.rag.retriever import CurriculumRetriever
from src.llm.client import GeminiClient
from src.llm.prompts import get_curriculum_generation_prompt


class CurriculumGenerator:
    """Main curriculum generation orchestrator."""
    
    def __init__(
        self,
        vector_store: CurriculumVectorStore,
        llm_client: GeminiClient
    ):
        """
        Initialize curriculum generator.
        
        Args:
            vector_store: ChromaDB vector store
            llm_client: Gemini LLM client
        """
        self.vector_store = vector_store
        self.llm_client = llm_client
        self.retriever = CurriculumRetriever(vector_store)
    
    def generate(
        self,
        request: CurriculumRequest,
        use_rag: bool = True
    ) -> Curriculum:
        """
        Generate curriculum using RAG + LLM.
        
        Args:
            request: Curriculum generation request
            use_rag: Whether to use RAG context (default: True)
            
        Returns:
            Generated curriculum
        """
        print(f"\n🎓 Generating {request.level} curriculum for {request.skill}...")
        
        # Step 1: RAG retrieval (if enabled)
        context = ""
        if use_rag and self.vector_store.get_count() > 0:
            print("📚 Retrieving similar curriculum examples...")
            similar_curricula = self.retriever.retrieve_similar_curricula(
                skill=request.skill,
                level=request.level,
                k=3
            )
            context = self.retriever.format_context_for_llm(similar_curricula)
            print(f"✓ Retrieved {len(similar_curricula)} similar examples")
        
        # Step 2: Generate prompt
        prompt = get_curriculum_generation_prompt(
            skill=request.skill,
            level=request.level,
            duration_semesters=request.duration_semesters,
            specialization=request.specialization,
            focus_areas=request.focus_areas,
            context=context
        )
        
        # Step 3: Generate with LLM
        print("🤖 Generating curriculum with Gemini...")
        response = self.llm_client.generate_with_retry(
            prompt=prompt,
            temperature=0.7
        )
        
        # Step 4: Parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_str = response.strip()
            if json_str.startswith("```json"):
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif json_str.startswith("```"):
                json_str = json_str.split("```")[1].split("```")[0].strip()
            
            curriculum_data = json.loads(json_str)
            curriculum = Curriculum(**curriculum_data)
            
            print(f"✓ Successfully generated curriculum with {len(curriculum.semesters)} semesters")
            return curriculum
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse curriculum JSON: {str(e)}\nResponse: {response[:500]}")
        except Exception as e:
            raise ValueError(f"Failed to create curriculum object: {str(e)}")
    
    def generate_from_dict(self, request_dict: dict) -> Curriculum:
        """
        Generate curriculum from dictionary input.
        
        Args:
            request_dict: Request parameters as dictionary
            
        Returns:
            Generated curriculum
        """
        request = CurriculumRequest(**request_dict)
        return self.generate(request)
