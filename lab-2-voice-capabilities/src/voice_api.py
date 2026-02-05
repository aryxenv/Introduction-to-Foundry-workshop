"""
Voice-enabled API for the RAG chatbot
Extends the basic chatbot API with voice capabilities
"""
import os
import logging
from typing import Optional
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import asyncio

from voice_handler import VoiceHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Voice-Enabled RAG Chatbot API",
    description="API for interacting with the RAG chatbot using voice",
    version="1.0.0"
)

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize voice handler
voice_handler: Optional[VoiceHandler] = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global voice_handler
    
    # Load configuration
    speech_key = os.getenv("AZURE_SPEECH_KEY", "")
    speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
    
    if speech_key:
        voice_handler = VoiceHandler(
            speech_key=speech_key,
            speech_region=speech_region,
            stt_language=os.getenv("STT_LANGUAGE", "en-US"),
            tts_voice=os.getenv("TTS_VOICE_NAME", "en-US-JennyNeural")
        )
        logger.info("Voice handler initialized")
    else:
        logger.warning("AZURE_SPEECH_KEY not configured - voice features disabled")


class TextRequest(BaseModel):
    """Request model for text input"""
    text: str


class VoiceInfo(BaseModel):
    """Information about available voices"""
    name: str
    language: str
    gender: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Voice-Enabled RAG Chatbot API",
        "voice_enabled": voice_handler is not None,
        "endpoints": {
            "health": "/health",
            "transcribe": "/api/voice/transcribe",
            "synthesize": "/api/voice/synthesize",
            "chat": "/api/voice/chat",
            "voices": "/api/voice/voices"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "voice_enabled": voice_handler is not None
    }


@app.post("/api/voice/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio to text
    
    Args:
        audio: Audio file (WAV, MP3, etc.)
        
    Returns:
        Transcribed text
    """
    if not voice_handler:
        raise HTTPException(status_code=503, detail="Voice services not configured")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio.filename).suffix) as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Transcribe audio
            text = await voice_handler.transcribe_audio(temp_path)
            
            return {
                "text": text,
                "status": "success"
            }
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice/synthesize")
async def synthesize_speech(request: TextRequest):
    """
    Convert text to speech
    
    Args:
        request: Text to convert
        
    Returns:
        Audio file
    """
    if not voice_handler:
        raise HTTPException(status_code=503, detail="Voice services not configured")
    
    try:
        # Create temporary file for audio output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_path = temp_file.name
        
        # Synthesize speech
        audio_data = await voice_handler.synthesize_speech(
            text=request.text,
            output_file=temp_path
        )
        
        # Return audio file
        return FileResponse(
            temp_path,
            media_type="audio/wav",
            filename="speech.wav"
        )
    
    except Exception as e:
        logger.error(f"Error synthesizing speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice/chat")
async def voice_chat(audio: UploadFile = File(...)):
    """
    Complete voice interaction: audio input -> text -> chatbot response -> audio output
    
    Args:
        audio: Audio file with user's question
        
    Returns:
        Audio file with chatbot's response
    """
    if not voice_handler:
        raise HTTPException(status_code=503, detail="Voice services not configured")
    
    try:
        # Step 1: Transcribe audio to text
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio.filename).suffix) as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_input_path = temp_file.name
        
        try:
            text = await voice_handler.transcribe_audio(temp_input_path)
            logger.info(f"Transcribed: {text}")
        finally:
            if os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
        
        if not text:
            raise HTTPException(status_code=400, detail="No speech detected in audio")
        
        # Step 2: Get chatbot response
        # In a real implementation, integrate with RAG chatbot from Lab 1
        # from rag_agent import RAGChatbot
        # response = await chatbot.chat(text)
        # response_text = response.response
        
        # Placeholder response
        response_text = f"You asked: {text}. This is a placeholder response. In a full implementation, this would come from the RAG chatbot."
        
        logger.info(f"Response: {response_text[:100]}...")
        
        # Step 3: Convert response to speech
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_output_path = temp_file.name
        
        audio_data = await voice_handler.synthesize_speech(
            text=response_text,
            output_file=temp_output_path
        )
        
        # Return audio response
        return FileResponse(
            temp_output_path,
            media_type="audio/wav",
            filename="response.wav"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in voice chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voice/voices")
async def list_voices():
    """
    List available voices
    
    Returns:
        List of available voice options
    """
    # Common Azure neural voices
    voices = [
        VoiceInfo(name="en-US-JennyNeural", language="en-US", gender="Female"),
        VoiceInfo(name="en-US-GuyNeural", language="en-US", gender="Male"),
        VoiceInfo(name="en-US-AriaNeural", language="en-US", gender="Female"),
        VoiceInfo(name="en-GB-SoniaNeural", language="en-GB", gender="Female"),
        VoiceInfo(name="en-GB-RyanNeural", language="en-GB", gender="Male"),
        VoiceInfo(name="es-ES-ElviraNeural", language="es-ES", gender="Female"),
        VoiceInfo(name="fr-FR-DeniseNeural", language="fr-FR", gender="Female"),
        VoiceInfo(name="de-DE-KatjaNeural", language="de-DE", gender="Female"),
        VoiceInfo(name="ja-JP-NanamiNeural", language="ja-JP", gender="Female"),
    ]
    
    return {
        "voices": [v.dict() for v in voices],
        "current_voice": os.getenv("TTS_VOICE_NAME", "en-US-JennyNeural")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
