"""
Unit tests for RAG Agent
Tests the core functionality of the RAG chatbot
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.rag_agent import RAGChatbot, ChatMessage, RAGResponse


class MockVectorStore:
    """Mock vector store for testing"""
    
    async def search(self, query: str, top_k: int):
        """Return mock search results"""
        return [
            {
                'content': 'TechCorp offers SmartAssist, DataVision, and CloudSync products.',
                'metadata': {
                    'source': 'company_info.txt',
                    'chunk_index': 0
                }
            },
            {
                'content': 'Office hours are Monday-Friday, 9 AM - 5 PM EST.',
                'metadata': {
                    'source': 'company_info.txt',
                    'chunk_index': 1
                }
            }
        ]


@pytest.fixture
def chatbot():
    """Create a test chatbot instance"""
    vector_store = MockVectorStore()
    return RAGChatbot(
        azure_openai_endpoint="https://test.openai.azure.com/",
        azure_openai_api_key="test-key",
        chat_deployment="gpt-4-test",
        embedding_deployment="embedding-test",
        vector_store=vector_store,
        top_k=3,
        temperature=0.7,
        max_tokens=1000
    )


@pytest.mark.asyncio
async def test_chatbot_initialization(chatbot):
    """Test chatbot initializes correctly"""
    assert chatbot is not None
    assert chatbot.endpoint == "https://test.openai.azure.com/"
    assert chatbot.chat_deployment == "gpt-4-test"
    assert chatbot.top_k == 3
    assert len(chatbot.conversation_history) == 0


@pytest.mark.asyncio
async def test_retrieve_context(chatbot):
    """Test context retrieval from vector store"""
    results = await chatbot._retrieve_context("What products do you offer?")
    
    assert len(results) == 2
    assert 'content' in results[0]
    assert 'metadata' in results[0]


@pytest.mark.asyncio
async def test_build_prompt(chatbot):
    """Test prompt building with context"""
    context_chunks = [
        {
            'content': 'TechCorp offers SmartAssist and DataVision.',
            'metadata': {'source': 'products.txt'}
        }
    ]
    
    prompt = chatbot._build_prompt("What products do you offer?", context_chunks)
    
    assert "What products do you offer?" in prompt
    assert "TechCorp offers SmartAssist" in prompt
    assert "Context:" in prompt


@pytest.mark.asyncio
async def test_chat_response(chatbot):
    """Test chat method returns proper response"""
    response = await chatbot.chat("What products do you offer?")
    
    assert isinstance(response, RAGResponse)
    assert response.response is not None
    assert isinstance(response.sources, list)
    assert len(response.retrieved_chunks) > 0


@pytest.mark.asyncio
async def test_conversation_history(chatbot):
    """Test conversation history is maintained"""
    # Clear history
    chatbot.clear_history()
    assert len(chatbot.conversation_history) == 0
    
    # Send a message
    await chatbot.chat("Hello")
    
    # Check history updated
    history = chatbot.get_history()
    assert len(history) == 2  # User message + assistant response
    assert history[0].role == "user"
    assert history[1].role == "assistant"


@pytest.mark.asyncio
async def test_clear_history(chatbot):
    """Test clearing conversation history"""
    # Add some messages
    await chatbot.chat("Hello")
    assert len(chatbot.conversation_history) > 0
    
    # Clear history
    chatbot.clear_history()
    assert len(chatbot.conversation_history) == 0


def test_chat_message():
    """Test ChatMessage dataclass"""
    message = ChatMessage(role="user", content="Hello")
    
    assert message.role == "user"
    assert message.content == "Hello"


def test_rag_response():
    """Test RAGResponse dataclass"""
    response = RAGResponse(
        response="Test response",
        sources=["test.txt"],
        retrieved_chunks=[{"content": "test"}]
    )
    
    assert response.response == "Test response"
    assert response.sources == ["test.txt"]
    assert len(response.retrieved_chunks) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
