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

### Voice Input Modes (Turn Detection)

| Mode | Description | Use Case |
|------|-------------|----------|
| **server_vad** | Server detects speech end based on silence | Natural conversations |
| **semantic_vad** | Server detects speech end based on words spoken | More natural turn-taking |
| **none** | Manual control (push-to-talk) | Noisy environments, external VAD |

### Available Voices

| Voice | Description |
|-------|-------------|
| **alloy** | Neutral, balanced |
| **ash** | Warm tone |
| **ballad** | Expressive |
| **coral** | Conversational |
| **echo** | Clear, direct |
| **sage** | Calm, thoughtful |
| **shimmer** | Soft, gentle |
| **verse** | Versatile |

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

> ⚠️ **Note**: The Foundry portal UI is evolving. The exact steps may differ from what's shown here. Check the latest [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/) for current instructions.

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
| **Model** | `gpt-4o-realtime-preview` | Your deployed model |
| **Voice** | `alloy` | Or any available voice |
| **Turn detection** | `server_vad` | Automatic speech detection |

---

### Step 3: Configure Voice Settings

1. Set voice parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| **threshold** | `0.5` | Speech detection sensitivity (0.0-1.0) |
| **prefix_padding_ms** | `300` | Audio to include before speech starts |
| **silence_duration_ms** | `200` | Silence duration to detect speech end |

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
<summary><strong>Option 2: Code (Using Realtime API)</strong></summary>

> ⚠️ **Note**: This example shows the conceptual approach. For the latest SDK and code samples, see the [GPT Realtime API documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/realtime-audio).

### Step 1: Install Dependencies

```bash
pip install openai
pip install azure-identity
pip install websockets
```

---

### Step 2: Connect to GPT Realtime API

Create a new file `realtime_voice.py`:

```python
import os
import json
import asyncio
import websockets
from azure.identity import DefaultAzureCredential

# Your Azure OpenAI endpoint and deployment
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = "gpt-4o-realtime-preview"

async def connect_to_realtime():
    """Connect to the GPT Realtime API via WebSocket."""
    
    # Get access token
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    
    # Construct WebSocket URL
    ws_url = f"{AZURE_OPENAI_ENDPOINT.replace('https', 'wss')}/openai/realtime"
    ws_url += f"?api-version=2024-10-01-preview&deployment={DEPLOYMENT_NAME}"
    
    headers = {
        "Authorization": f"Bearer {token.token}"
    }
    
    async with websockets.connect(ws_url, extra_headers=headers) as ws:
        # Configure session with VAD settings
        session_config = {
            "type": "session.update",
            "session": {
                "voice": "alloy",
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 200
                },
                "tools": [
                    {
                        "type": "function",
                        "name": "search_knowledge_base",
                        "description": "Search the company knowledge base",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"}
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        }
        
        await ws.send(json.dumps(session_config))
        print("Connected to GPT Realtime API!")
        print("Session configured with voice and RAG tool.")
        
        return ws
```

---

### Step 3: Handle Function Calls (RAG Integration)

When the model needs to search your knowledge base, it will emit a function call:

```python
async def handle_realtime_events(ws):
    """Handle events from the Realtime API."""
    
    async for message in ws:
        event = json.loads(message)
        
        if event["type"] == "response.function_call_arguments.done":
            # Model wants to call our RAG function
            if event["name"] == "search_knowledge_base":
                args = json.loads(event["arguments"])
                
                # Search your knowledge base from Lab 1
                results = await search_knowledge_base(args["query"])
                
                # Send function result back to the model
                await ws.send(json.dumps({
                    "type": "conversation.item.create",
                    "item": {
                        "type": "function_call_output",
                        "call_id": event["call_id"],
                        "output": results
                    }
                }))
                
                # Trigger response generation
                await ws.send(json.dumps({"type": "response.create"}))
        
        elif event["type"] == "response.audio.delta":
            # Handle audio output (play through speakers)
            audio_data = event["delta"]
            # Process audio...
        
        elif event["type"] == "response.audio_transcript.delta":
            # Text transcript of what the model is saying
            print(event["delta"], end="", flush=True)
```

---

### Step 4: Implement Knowledge Base Search

Connect to your AI Search index from Lab 1:

```python
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

async def search_knowledge_base(query: str) -> str:
    """Search the knowledge base created in Lab 1."""
    
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
    
    return context if context else "No relevant information found."
```

---

### Step 5: Run and Test

1. Set your environment variables:

```bash
# Windows PowerShell
$env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
$env:SEARCH_ENDPOINT = "https://your-search.search.windows.net"
```

2. Run the script:

```bash
python realtime_voice.py
```

3. Test with voice queries:
   - "What are the company's remote work policies?"
   - "Tell me about the vacation policy"
   - "Who can I contact for HR questions?"

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
