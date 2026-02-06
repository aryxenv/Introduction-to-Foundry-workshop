# Sub-Lab 2.3: Build Voice Web App

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.2](./sub-lab-2.2-audio-playground.md)

---

**⏱️ Estimated Time**: 15-20 minutes

## Overview

In this sub-lab, you'll build a web application that enables voice conversations using the GPT Realtime API with WebRTC. This gives you a custom voice interface that can be integrated into your own applications.

---

## 🎓 Key Concepts

### WebRTC vs WebSockets

| Protocol | Best For | Latency |
|----------|----------|---------|
| **WebRTC** | Client-side apps (browsers, mobile) | Very low (~100-200ms) |
| **WebSockets** | Server-to-server communication | Low (~200-500ms) |

> 💡 **Recommendation**: Use WebRTC for web applications. It's designed for real-time audio and provides the best user experience.

### Realtime API Flow

```
┌─────────────┐     WebRTC      ┌─────────────────┐
│   Browser   │ ←─────────────→ │  GPT Realtime   │
│  (audio)    │                 │    Endpoint     │
└─────────────┘                 └─────────────────┘
      │                                │
      │ 1. Send audio chunks           │
      │ ──────────────────────────────→│
      │                                │
      │ 2. Receive audio response      │
      │←────────────────────────────── │
      │                                │
```

### Session Configuration

When creating a realtime session, you configure:
- **Model**: Which realtime model to use
- **Voice**: Response voice (alloy, coral, etc.)
- **Instructions**: System prompt for the model
- **Tools**: Functions the model can call (for RAG integration)

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

### 1. Install Dependencies

```bash
cd lab-2-voice-capabilities

# Install Python dependencies
pip install aiohttp python-dotenv
```

### 2. Create Realtime Voice Client

Create `src/realtime_client.py`:

```python
"""
GPT Realtime API client for voice conversations
Uses WebRTC for low-latency audio streaming
"""
import os
import json
import asyncio
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

load_dotenv()

# Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
REALTIME_DEPLOYMENT = os.getenv("AZURE_OPENAI_REALTIME_DEPLOYMENT", "gpt-realtime")
VOICE = os.getenv("AZURE_OPENAI_REALTIME_VOICE", "alloy")


def get_realtime_endpoint():
    """Get the WebRTC endpoint for realtime audio"""
    # Remove trailing slash if present
    base_url = AZURE_OPENAI_ENDPOINT.rstrip('/')
    # Construct realtime endpoint
    return f"{base_url}/openai/realtime"


def get_session_config(instructions: str = None):
    """
    Create session configuration for realtime API
    """
    default_instructions = """
    You are a helpful customer service assistant for TechCorp.
    Keep responses concise and conversational.
    If you don't know something, say so honestly.
    """
    
    return {
        "model": REALTIME_DEPLOYMENT,
        "voice": VOICE,
        "instructions": instructions or default_instructions,
        "input_audio_format": "pcm16",
        "output_audio_format": "pcm16",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 500
        }
    }


async def create_realtime_session():
    """
    Create a new realtime session
    Returns session details including the ephemeral token for WebRTC
    """
    import aiohttp
    
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    
    endpoint = get_realtime_endpoint()
    session_url = f"{endpoint}/sessions"
    
    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json"
    }
    
    session_config = get_session_config()
    
    async with aiohttp.ClientSession() as session:
        async with session.post(session_url, headers=headers, json=session_config) as response:
            if response.status == 200:
                session_data = await response.json()
                print(f"✅ Created realtime session: {session_data.get('id')}")
                return session_data
            else:
                error = await response.text()
                raise Exception(f"Failed to create session: {error}")


if __name__ == "__main__":
    # Test session creation
    asyncio.run(create_realtime_session())
```

### 3. Create Voice Web Interface

Create `web/voice-app.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechCorp Voice Assistant</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        
        .mic-button {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 48px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 20px 0;
        }
        
        .mic-button:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .mic-button.listening {
            background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(245, 87, 108, 0.4); }
            70% { box-shadow: 0 0 0 20px rgba(245, 87, 108, 0); }
            100% { box-shadow: 0 0 0 0 rgba(245, 87, 108, 0); }
        }
        
        .status {
            font-size: 18px;
            color: #666;
            margin: 20px 0;
            min-height: 24px;
        }
        
        .status.listening {
            color: #f5576c;
            font-weight: bold;
        }
        
        .transcript {
            background: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            min-height: 100px;
            text-align: left;
        }
        
        .transcript h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .transcript-content {
            color: #555;
            line-height: 1.6;
        }
        
        .transcript-content .user {
            color: #667eea;
            font-weight: bold;
        }
        
        .transcript-content .assistant {
            color: #764ba2;
        }
        
        .settings {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
        
        .settings label {
            display: block;
            margin-bottom: 5px;
            color: #666;
            font-size: 14px;
        }
        
        .settings select {
            padding: 8px 12px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ TechCorp Voice Assistant</h1>
        <p class="subtitle">Powered by GPT Realtime</p>
        
        <button id="micButton" class="mic-button" onclick="toggleListening()">
            🎤
        </button>
        
        <p id="status" class="status">Click to start speaking</p>
        
        <div class="transcript">
            <h3>Conversation</h3>
            <div id="transcriptContent" class="transcript-content">
                <em>Your conversation will appear here...</em>
            </div>
        </div>
        
        <div class="settings">
            <label for="voiceSelect">Voice:</label>
            <select id="voiceSelect">
                <option value="alloy">Alloy (Neutral)</option>
                <option value="coral">Coral (Friendly)</option>
                <option value="echo">Echo (Calm)</option>
                <option value="shimmer">Shimmer (Clear)</option>
            </select>
        </div>
    </div>

    <script>
        let isListening = false;
        let peerConnection = null;
        let audioContext = null;
        let mediaStream = null;
        
        const micButton = document.getElementById('micButton');
        const status = document.getElementById('status');
        const transcriptContent = document.getElementById('transcriptContent');
        
        async function toggleListening() {
            if (isListening) {
                stopListening();
            } else {
                await startListening();
            }
        }
        
        async function startListening() {
            try {
                // Request microphone access
                mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                
                // Update UI
                isListening = true;
                micButton.classList.add('listening');
                status.textContent = 'Listening...';
                status.classList.add('listening');
                
                // Initialize WebRTC connection
                await initializeRealtimeConnection();
                
            } catch (error) {
                console.error('Error starting voice:', error);
                status.textContent = 'Error: ' + error.message;
            }
        }
        
        function stopListening() {
            isListening = false;
            micButton.classList.remove('listening');
            status.textContent = 'Click to start speaking';
            status.classList.remove('listening');
            
            // Cleanup
            if (mediaStream) {
                mediaStream.getTracks().forEach(track => track.stop());
            }
            if (peerConnection) {
                peerConnection.close();
            }
        }
        
        async function initializeRealtimeConnection() {
            // Note: In production, get session token from your backend
            // This is a simplified example
            
            const voice = document.getElementById('voiceSelect').value;
            
            // For demo: Show connection status
            addToTranscript('system', 'Connecting to GPT Realtime...');
            
            // In production, you would:
            // 1. Call your backend to get an ephemeral token
            // 2. Use that token to establish WebRTC connection
            // 3. Stream audio through the connection
            
            // Simulated response for demo
            setTimeout(() => {
                addToTranscript('assistant', 'Hello! I\'m your TechCorp voice assistant. How can I help you today?');
            }, 1000);
        }
        
        function addToTranscript(role, text) {
            const roleClass = role === 'user' ? 'user' : 'assistant';
            const roleLabel = role === 'user' ? 'You' : 'Assistant';
            
            if (transcriptContent.querySelector('em')) {
                transcriptContent.innerHTML = '';
            }
            
            const message = document.createElement('p');
            message.innerHTML = `<span class="${roleClass}">${roleLabel}:</span> ${text}`;
            transcriptContent.appendChild(message);
            transcriptContent.scrollTop = transcriptContent.scrollHeight;
        }
    </script>
</body>
</html>
```

### 4. Create Backend Server

Create `src/voice_server.py`:

```python
"""
FastAPI server for GPT Realtime voice application
Handles session creation and token management
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
import aiohttp

load_dotenv()

app = FastAPI(title="TechCorp Voice Assistant API")

# Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
REALTIME_DEPLOYMENT = os.getenv("AZURE_OPENAI_REALTIME_DEPLOYMENT", "gpt-realtime")


class SessionRequest(BaseModel):
    voice: str = "alloy"
    instructions: str = None


class SessionResponse(BaseModel):
    session_id: str
    token: str
    endpoint: str


@app.post("/api/realtime/session", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    """
    Create a realtime session and return ephemeral token
    The client uses this token to establish WebRTC connection
    """
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        
        endpoint = f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/realtime"
        session_url = f"{endpoint}/sessions"
        
        default_instructions = """
        You are a helpful customer service assistant for TechCorp.
        You have knowledge about TechCorp's products: SmartAssist, DataVision, and CloudSync.
        Keep responses concise since this is a voice interface.
        Be friendly and professional.
        """
        
        session_config = {
            "model": REALTIME_DEPLOYMENT,
            "voice": request.voice,
            "instructions": request.instructions or default_instructions,
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16"
        }
        
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(session_url, headers=headers, json=session_config) as response:
                if response.status == 200:
                    data = await response.json()
                    return SessionResponse(
                        session_id=data.get("id"),
                        token=data.get("client_secret", {}).get("token", ""),
                        endpoint=endpoint
                    )
                else:
                    error = await response.text()
                    raise HTTPException(status_code=response.status, detail=error)
                    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "voice-assistant"}


# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static")


@app.get("/")
async def serve_app():
    """Serve the voice app HTML"""
    return FileResponse("web/voice-app.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 5. Run the Voice Application

```bash
# Start the server
cd lab-2-voice-capabilities
uvicorn src.voice_server:app --reload --port 8000
```

Open your browser: `http://localhost:8000`

### 6. Test the Voice App

1. Click the microphone button
2. Allow microphone access when prompted
3. Speak naturally: "What products do you offer?"
4. Listen to the voice response
5. Try follow-up questions

### ✅ Code Checkpoint

You should now have:
- [ ] Realtime client library created
- [ ] Voice web interface working
- [ ] Backend server handling sessions
- [ ] Voice conversations working in browser

</details>

---

## 🎉 Congratulations!

You've completed Lab 2! You now have:

- ✅ GPT Realtime model deployed in Foundry
- ✅ Tested voice conversations in Audio Playground
- ✅ (Code path) Built a custom voice web application

### What You Built

```
┌─────────────────────────────────────────────────────────────────┐
│                   Voice-Enabled Chatbot                         │
│                                                                  │
│   🎤 Voice Input → GPT Realtime → 🔊 Voice Output               │
│                         ↓                                        │
│               Knowledge from Lab 1                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Next Steps

- **Customize the voice**: Try different voices and speaking styles
- **Add more context**: Connect your RAG knowledge base from Lab 1
- **Build mobile app**: Use WebRTC SDK for iOS/Android
- **Add visual feedback**: Display audio waveforms and transcripts
- **Implement wake word**: "Hey TechBot" activation

---

## 📚 Additional Resources

- [GPT Realtime API Reference](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/realtime-audio-reference)
- [WebRTC Integration Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/realtime-audio-webrtc)
- [Voice Live SDK](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live) (alternative approach)

---

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.2](./sub-lab-2.2-audio-playground.md)
