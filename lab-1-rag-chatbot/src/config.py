"""
Configuration management for RAG Chatbot
Loads environment variables and validates configuration
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_CHAT_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4")
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    # Azure AI Search Configuration
    AZURE_SEARCH_ENDPOINT: str = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    AZURE_SEARCH_API_KEY: str = os.getenv("AZURE_SEARCH_API_KEY", "")
    AZURE_SEARCH_INDEX_NAME: str = os.getenv("AZURE_SEARCH_INDEX_NAME", "chatbot-knowledge-base")
    
    # Application Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "3"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    @classmethod
    def validate(cls) -> None:
        """Validate that all required configuration is present"""
        required_fields = [
            ("AZURE_OPENAI_ENDPOINT", cls.AZURE_OPENAI_ENDPOINT),
            ("AZURE_OPENAI_API_KEY", cls.AZURE_OPENAI_API_KEY),
            ("AZURE_SEARCH_ENDPOINT", cls.AZURE_SEARCH_ENDPOINT),
            ("AZURE_SEARCH_API_KEY", cls.AZURE_SEARCH_API_KEY),
        ]
        
        missing_fields = [name for name, value in required_fields if not value]
        
        if missing_fields:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing_fields)}. "
                f"Please set these in your .env file."
            )
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if configuration is complete"""
        try:
            cls.validate()
            return True
        except ValueError:
            return False


# Validate configuration on import
if __name__ != "__main__":
    try:
        Config.validate()
    except ValueError as e:
        print(f"⚠️  Configuration Warning: {e}")
