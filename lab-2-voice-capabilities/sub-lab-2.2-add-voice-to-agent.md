# Sub-Lab 2.2: Add Voice to Your Agent

## 🎯 Objective

Add real-time voice capabilities to the RAG chatbot agent you created in Lab 1, enabling natural speech-to-speech conversations with your knowledge base.

---

## 📚 Key Concepts

### Voice-Enabled Agents

A **voice-enabled agent** combines:
- **Speech recognition**: Converting user speech to text
- **Agent processing**: Understanding intent and retrieving relevant information
- **Speech synthesis**: Converting the agent's response back to natural speech

### GPT Realtime Integration

The GPT Realtime model provides **native speech-to-speech** capabilities:
- No separate STT → LLM → TTS pipeline needed
- Single model handles the entire voice conversation
- Preserves context across the conversation
- Supports function calling (your RAG retrieval becomes a tool)

### Voice Input Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Server VAD** | Server detects when user stops speaking | Natural conversations |
| **Push-to-talk** | User presses button to speak | Noisy environments |
| **Continuous** | Always listening | Hands-free scenarios |

### Available Voices (GA Features)

| Voice | Style | Best For |
|-------|-------|----------|
| **Marin** | Warm, welcoming | Customer service |
| **Cedar** | Clear, professional | Business applications |
| **Alloy** | Neutral, balanced | General purpose |
| **Echo** | Conversational | Casual interactions |
| **Fable** | Expressive | Storytelling |
| **Onyx** | Deep, authoritative | Formal announcements |
| **Nova** | Friendly, upbeat | Engaging content |
| **Shimmer** | Soft, gentle | Calm interactions |

---

## ⏱️ Estimated Time: 15-20 minutes

---

## 📝 Prerequisites

- ✅ Completed [Lab 1: RAG Chatbot](../lab-1-rag-chatbot/README.md) - You need an existing agent
- ✅ Completed [Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) - GPT Realtime model deployed

---

## Choose Your Path

<details>
<summary><strong>Option 1: Console (Microsoft Foundry Portal)</strong></summary>

### Step 1: Navigate to Your Agent

1. Go to [Microsoft Foundry Portal](https://ai.azure.com)
2. Select your project
3. Navigate to **Agents** in the left menu
4. Click on your RAG chatbot agent from Lab 1

---

### Step 2: Enable Voice Input

1. In the agent configuration, click **Settings** or **Edit**
2. Look for **Voice & Audio** settings
3. Enable **Voice input**
4. Configure the following:

| Setting | Value | Notes |
|---------|-------|-------|
| **Model** | `gpt-realtime` | Your deployed model |
| **Voice** | `marin` | Or your preferred voice |
| **Input mode** | `Server VAD` | Automatic speech detection |

---

### Step 3: Configure Voice Settings

1. Set voice parameters:

| Parameter | Recommended | Description |
|-----------|-------------|-------------|
| **Threshold** | `0.5` | Speech detection sensitivity |
| **Prefix padding** | `300ms` | Time before speech starts |
| **Silence duration** | `500ms` | Time to wait after speech ends |

2. Click **Save** to apply settings

---

### Step 4: Test Voice Interaction

1. Click **Test** or **Chat** to open the agent interface
2. Look for the **microphone icon** 🎤
3. Click the microphone or say your wake word
4. Ask a question about your knowledge base:
   > "What are the company's remote work policies?"
5. The agent should:
   - Recognize your speech
   - Query the RAG knowledge base
   - Respond with synthesized speech

---

### Step 5: Verify RAG Integration

Test that voice queries retrieve from your knowledge base:

| Test Query (speak) | Expected Behavior |
|--------------------|-------------------|
| "Tell me about the company" | Retrieves from `company_info.txt` |
| "What are the PTO policies?" | Retrieves from `policies.txt` |
| "Who founded the company?" | Uses knowledge base context |

> ✅ **Success**: Your agent responds verbally with information from your knowledge base

---

</details>

<details>
<summary><strong>Option 2: Code (Microsoft Agent Framework)</strong></summary>

### Step 1: Install Voice Dependencies

```bash
pip install agent-framework[voice]
pip install azure-ai-projects
pip install pyaudio
```

> ⚠️ **Note**: PyAudio requires additional system dependencies:
> - **Windows**: Usually works out of the box
> - **macOS**: `brew install portaudio`
> - **Linux**: `sudo apt-get install portaudio19-dev`

---

### Step 2: Create Voice-Enabled Agent

Create a new file `voice_agent.py`:

```python
import os
from agent_framework import Agent, VoiceConfig
from agent_framework.tools import Tool
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Your project connection string from Lab 1
PROJECT_CONNECTION_STRING = os.environ.get("PROJECT_CONNECTION_STRING")

# Initialize project client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=PROJECT_CONNECTION_STRING
)

# Get your RAG agent from Lab 1
agent = project_client.agents.get_agent(
    agent_id=os.environ.get("RAG_AGENT_ID")
)

# Configure voice settings
voice_config = VoiceConfig(
    model="gpt-realtime",
    voice="marin",  # New GA voice
    input_mode="server_vad",
    vad_settings={
        "threshold": 0.5,
        "prefix_padding_ms": 300,
        "silence_duration_ms": 500
    }
)

# Enable voice on the agent
agent.enable_voice(voice_config)

print("Voice-enabled agent ready!")
print("Speak into your microphone to interact with your knowledge base.")
```

---

### Step 3: Create Voice Conversation Handler

Add conversation handling to your script:

```python
from agent_framework.voice import VoiceSession

async def run_voice_conversation():
    """Run an interactive voice conversation with the agent."""
    
    # Create a voice session
    async with VoiceSession(agent) as session:
        print("\n🎤 Voice session started. Say 'quit' to exit.\n")
        
        while True:
            # Listen for user speech
            user_input = await session.listen()
            
            if user_input.lower() in ["quit", "exit", "stop"]:
                print("Ending voice session...")
                break
            
            print(f"You said: {user_input}")
            
            # Agent processes and responds with voice
            response = await session.respond()
            
            print(f"Agent said: {response.text}")
            print(f"Sources: {response.citations}")

# Run the conversation
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_voice_conversation())
```

---

### Step 4: Add RAG Tool for Voice

If your agent doesn't have the RAG tool configured, add it:

```python
from agent_framework.tools import FunctionTool

# Define the RAG retrieval as a tool
@FunctionTool
async def search_knowledge_base(query: str) -> str:
    """
    Search the company knowledge base for relevant information.
    
    Args:
        query: The user's question or search terms
    
    Returns:
        Relevant information from the knowledge base
    """
    # Use your existing vector store from Lab 1
    from azure.search.documents import SearchClient
    from azure.identity import DefaultAzureCredential
    
    search_client = SearchClient(
        endpoint=os.environ.get("SEARCH_ENDPOINT"),
        index_name="rag-index",
        credential=DefaultAzureCredential()
    )
    
    results = search_client.search(
        search_text=query,
        top=3,
        select=["content", "source"]
    )
    
    context = "\n\n".join([
        f"From {r['source']}:\n{r['content']}" 
        for r in results
    ])
    
    return context

# Register the tool with your voice agent
agent.register_tool(search_knowledge_base)
```

---

### Step 5: Run and Test

1. Set your environment variables:

```bash
# Windows PowerShell
$env:PROJECT_CONNECTION_STRING = "your-connection-string"
$env:RAG_AGENT_ID = "your-agent-id"
$env:SEARCH_ENDPOINT = "https://your-search.search.windows.net"
```

2. Run the voice agent:

```bash
python voice_agent.py
```

3. Test with voice queries:
   - "What are the company's remote work policies?"
   - "Tell me about the vacation policy"
   - "Who can I contact for HR questions?"

---

### Step 6: (Optional) Build a Web Interface

Create a simple web interface for browser-based voice interaction:

```python
# web_voice_app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import asyncio

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('voice_chat.html')

@socketio.on('audio_stream')
def handle_audio(data):
    """Handle incoming audio from browser."""
    # Process audio through your voice agent
    # Emit response back to client
    pass

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
```

> 💡 **Tip**: For production apps, use WebRTC for lower latency

---

</details>

---

## ✅ Validation Checklist

| Check | Status |
|-------|--------|
| Agent has voice input enabled | ⬜ |
| GPT Realtime model connected | ⬜ |
| Can speak and be understood | ⬜ |
| Agent responds with voice | ⬜ |
| RAG retrieval works via voice | ⬜ |
| Citations are maintained | ⬜ |

---

## 🎉 Congratulations!

You've successfully added voice capabilities to your RAG chatbot agent! Your agent can now:

- 🎤 Understand natural speech input
- 🔍 Query your knowledge base based on voice questions  
- 🗣️ Respond with natural, synthesized speech
- 📚 Cite sources from your documents

---

## 🔗 What You Built

```
┌─────────────────────────────────────────────────────────────┐
│                    Voice-Enabled RAG Agent                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User Speech ──► GPT Realtime ──► Agent Processing           │
│       │              │                   │                   │
│       │              │                   ▼                   │
│       │              │         ┌─────────────────┐           │
│       │              │         │  RAG Retrieval  │           │
│       │              │         │  (AI Search)    │           │
│       │              │         └────────┬────────┘           │
│       │              │                  │                    │
│       │              ▼                  ▼                    │
│       │         Response + Context + Citations               │
│       │              │                                       │
│       ▼              ▼                                       │
│  Voice Response ◄── Speech Synthesis                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ➡️ Next Steps

- **Customize voices**: Try different voices for different use cases
- **Add interruption handling**: Allow users to interrupt the agent mid-response
- **Implement multi-turn memory**: Maintain conversation context across turns
- **Deploy to production**: Host your voice agent as a web service

---

## 📚 Additional Resources

- [GPT Realtime Documentation](https://learn.microsoft.com/azure/ai-services/openai/realtime-audio)
- [Microsoft Agent Framework Voice Guide](https://learn.microsoft.com/azure/ai-services/agents)
- [WebRTC Integration Guide](https://learn.microsoft.com/azure/ai-services/openai/realtime-audio-webrtc)

---

[← Back to Lab 2 Overview](./README.md) | [Back to Lab 1 →](../lab-1-rag-chatbot/README.md)
