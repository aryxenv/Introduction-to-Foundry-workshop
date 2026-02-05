"""
FastAPI application for RAG Chatbot
Provides REST API endpoints for the chatbot
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation Chatbot using Microsoft Agent Framework",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation history")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Chatbot's response")
    sources: List[str] = Field(..., description="Sources used to generate response")
    session_id: str = Field(..., description="Session identifier")
    timestamp: str = Field(..., description="Response timestamp")


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: str
    version: str


class StatsResponse(BaseModel):
    """Response model for statistics"""
    total_requests: int
    uptime_seconds: float
    status: str


# Global state (in production, use proper state management)
request_count = 0
start_time = datetime.now()


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    logger.info("🚀 Starting RAG Chatbot API...")
    
    # In a real implementation:
    # 1. Initialize RAG chatbot
    # 2. Connect to vector store
    # 3. Verify Azure OpenAI connectivity
    
    logger.info("✅ RAG Chatbot API ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    logger.info("👋 Shutting down RAG Chatbot API...")


@app.get("/", tags=["General"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "RAG Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "stats": "/api/stats",
            "docs": "/docs"
        }
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Monitoring"])
async def health_check():
    """
    Health check endpoint
    
    Returns service health status
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/api/stats", response_model=StatsResponse, tags=["Monitoring"])
async def get_stats():
    """
    Get API statistics
    
    Returns usage statistics
    """
    uptime = (datetime.now() - start_time).total_seconds()
    
    return StatsResponse(
        total_requests=request_count,
        uptime_seconds=uptime,
        status="operational"
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Chat endpoint
    
    Send a message to the chatbot and receive a response.
    
    Args:
        request: ChatRequest with user message and optional session_id
        
    Returns:
        ChatResponse with bot's answer, sources, and session info
        
    Raises:
        HTTPException: If processing fails
    """
    global request_count
    request_count += 1
    
    try:
        logger.info(f"📨 Received message: {request.message[:50]}...")
        
        # Generate or use existing session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # In real implementation:
        # 1. Retrieve conversation history for session
        # 2. Call RAG chatbot with message
        # 3. Get response with sources
        # 4. Update conversation history
        
        # Placeholder response (replace with actual RAG chatbot call)
        bot_response = (
            "This is a placeholder response. In a real implementation, "
            "the RAG chatbot would retrieve relevant context from the "
            "knowledge base and generate a contextual response using "
            "Azure OpenAI."
        )
        sources = ["placeholder.txt"]
        
        # Real implementation would look like:
        # rag_response = await chatbot.chat(request.message, session_id)
        # bot_response = rag_response.response
        # sources = rag_response.sources
        
        response = ChatResponse(
            response=bot_response,
            sources=sources,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"✅ Response generated for session {session_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error processing chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )


@app.delete("/api/chat/{session_id}", tags=["Chat"])
async def clear_session(session_id: str):
    """
    Clear conversation history for a session
    
    Args:
        session_id: Session identifier to clear
        
    Returns:
        Success message
    """
    try:
        # In real implementation:
        # chatbot.clear_history(session_id)
        
        logger.info(f"🗑️  Cleared session: {session_id}")
        
        return {
            "message": f"Session {session_id} cleared successfully",
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"❌ Error clearing session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing session: {str(e)}"
        )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return {
        "error": "Not Found",
        "message": f"The endpoint {request.url.path} does not exist",
        "status_code": 404
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {exc}")
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
