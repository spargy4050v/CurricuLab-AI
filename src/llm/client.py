"""
Google Gemini client for curriculum generation.
Uses free tier: 60 requests/min, 1500 requests/day.
"""
import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv


class GeminiClient:
    """Google Gemini LLM client wrapper."""
    
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        """
        Initialize Gemini client.
        
        Args:
            model_name: Gemini model to use (default: gemini-1.5-pro)
        """
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment variables. "
                "Please create a .env file with your API key. "
                "Get your key from: https://makersuite.google.com/app/apikey"
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        
        print(f"✓ Gemini client initialized: {model_name}")
        print(f"  Free tier: 60 requests/min, 1500 requests/day")
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using Gemini.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        generation_config = {
            "temperature": temperature,
        }
        
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        
        except Exception as e:
            raise Exception(f"Gemini generation failed: {str(e)}")
    
    def generate_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """
        Generate with automatic retry on failure.
        
        Args:
            prompt: Input prompt
            max_retries: Maximum retry attempts
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
        """
        import time
        
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, **kwargs)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⚠ Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e
