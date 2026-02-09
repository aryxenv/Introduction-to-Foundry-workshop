# Sub-Lab 2.2: Add Voice to Your Agent

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md)

---

**⏱️ Estimated Time**: 15-20 minutes

## Overview

In this sub-lab, you'll add real-time voice capabilities to the Foundry Agent Web App you deployed in Sub-Lab 1.5. Users will be able to speak directly to your RAG chatbot and receive spoken responses.

> **Note**: This sub-lab is **Code only** and builds on the Foundry Agent Web App from Sub-Lab 1.5.

---

## 🎓 Key Concepts

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

## 📝 Prerequisites

- ✅ Completed [Sub-Lab 1.5](../lab-1-rag-chatbot/sub-lab-1.5-host-agent-webapp.md) - Foundry Agent Web App deployed
- ✅ Completed [Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) - GPT Realtime model deployed
- ✅ Your Foundry Agent Web App running locally or deployed to Azure

---

## 💻 Code Instructions

### Step 1: Navigate to Your Web App

```powershell
# Navigate to your Foundry Agent Web App from Sub-Lab 1.5
cd c:\Users\lverghote\source\repos\foundry-agent-webapp
```

---

### Step 2: Add Realtime Voice Dependencies

Add the required npm packages to the frontend:

```powershell
cd frontend
npm install @anthropic-ai/sdk@latest --legacy-peer-deps
```

> **Note**: The Foundry Agent Web App uses React 19, which requires `--legacy-peer-deps` for some packages.

---

### Step 3: Create Voice Chat Component

Create a new file `frontend/src/components/VoiceChat.tsx`:

```typescript
import { useState, useRef, useCallback, useEffect } from 'react';
import { Button } from '@fluentui/react-components';
import { Mic24Regular, MicOff24Regular } from '@fluentui/react-icons';
import { useAuth } from '../hooks/useAuth';

interface VoiceChatProps {
  onTranscript: (text: string) => void;
  onResponse: (text: string) => void;
}

export const VoiceChat: React.FC<VoiceChatProps> = ({ onTranscript, onResponse }) => {
  const [isListening, setIsListening] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const { getAccessToken } = useAuth();

  const connectToRealtime = useCallback(async () => {
    try {
      const token = await getAccessToken();
      const apiUrl = import.meta.env.VITE_API_URL || '/api';
      
      // Connect to backend WebSocket endpoint for Realtime API
      const wsUrl = apiUrl.replace('http', 'ws') + '/voice/stream';
      const ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        console.log('Connected to voice service');
        setIsConnected(true);
        
        // Send session configuration
        ws.send(JSON.stringify({
          type: 'session.update',
          session: {
            voice: 'alloy',
            turn_detection: {
              type: 'server_vad',
              threshold: 0.5,
              prefix_padding_ms: 300,
              silence_duration_ms: 200
            }
          }
        }));
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'response.audio_transcript.delta') {
          onResponse(data.delta);
        } else if (data.type === 'conversation.item.input_audio_transcription.completed') {
          onTranscript(data.transcript);
        }
      };

      ws.onclose = () => {
        console.log('Disconnected from voice service');
        setIsConnected(false);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  }, [getAccessToken, onTranscript, onResponse]);

  const startListening = useCallback(async () => {
    if (!isConnected) {
      await connectToRealtime();
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
          // Convert to base64 and send
          const reader = new FileReader();
          reader.onloadend = () => {
            const base64 = (reader.result as string).split(',')[1];
            wsRef.current?.send(JSON.stringify({
              type: 'input_audio_buffer.append',
              audio: base64
            }));
          };
          reader.readAsDataURL(event.data);
        }
      };

      mediaRecorder.start(100); // Send chunks every 100ms
      mediaRecorderRef.current = mediaRecorder;
      setIsListening(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  }, [isConnected, connectToRealtime]);

  const stopListening = useCallback(() => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      mediaRecorderRef.current = null;
    }
    setIsListening(false);
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopListening();
      wsRef.current?.close();
    };
  }, [stopListening]);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      <Button
        icon={isListening ? <MicOff24Regular /> : <Mic24Regular />}
        appearance={isListening ? 'primary' : 'secondary'}
        onClick={isListening ? stopListening : startListening}
        title={isListening ? 'Stop listening' : 'Start voice input'}
      >
        {isListening ? 'Stop' : 'Voice'}
      </Button>
      {isListening && (
        <span style={{ color: 'red', fontSize: '12px' }}>● Recording...</span>
      )}
    </div>
  );
};
```

---

### Step 4: Add Backend Voice Endpoint

Create a new file `backend/WebApp.Api/Endpoints/VoiceEndpoints.cs`:

```csharp
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using Azure.Identity;

namespace WebApp.Api.Endpoints;

public static class VoiceEndpoints
{
    public static void MapVoiceEndpoints(this WebApplication app)
    {
        app.Map("/api/voice/stream", async (HttpContext context) =>
        {
            if (!context.WebSockets.IsWebSocketRequest)
            {
                context.Response.StatusCode = 400;
                return;
            }

            var webSocket = await context.WebSockets.AcceptWebSocketAsync();
            await HandleVoiceSession(webSocket, context.RequestAborted);
        });
    }

    private static async Task HandleVoiceSession(
        WebSocket clientSocket, 
        CancellationToken cancellationToken)
    {
        var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
            ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT not configured");
        
        var deployment = "gpt-4o-realtime-preview";
        
        // Get token for Azure OpenAI
        var credential = new DefaultAzureCredential();
        var token = await credential.GetTokenAsync(
            new Azure.Core.TokenRequestContext(
                new[] { "https://cognitiveservices.azure.com/.default" }),
            cancellationToken);

        // Connect to Azure OpenAI Realtime API
        var realtimeUrl = $"{endpoint.Replace("https", "wss")}/openai/realtime" +
            $"?api-version=2024-10-01-preview&deployment={deployment}";
        
        using var realtimeSocket = new ClientWebSocket();
        realtimeSocket.Options.SetRequestHeader("Authorization", $"Bearer {token.Token}");
        
        await realtimeSocket.ConnectAsync(new Uri(realtimeUrl), cancellationToken);

        // Relay messages between client and Realtime API
        var clientToRealtime = RelayMessages(clientSocket, realtimeSocket, cancellationToken);
        var realtimeToClient = RelayMessages(realtimeSocket, clientSocket, cancellationToken);

        await Task.WhenAny(clientToRealtime, realtimeToClient);
    }

    private static async Task RelayMessages(
        WebSocket source, 
        WebSocket destination, 
        CancellationToken cancellationToken)
    {
        var buffer = new byte[8192];
        
        while (source.State == WebSocketState.Open && !cancellationToken.IsCancellationRequested)
        {
            var result = await source.ReceiveAsync(buffer, cancellationToken);
            
            if (result.MessageType == WebSocketMessageType.Close)
            {
                await destination.CloseAsync(
                    WebSocketCloseStatus.NormalClosure, 
                    "Closed", 
                    cancellationToken);
                break;
            }

            await destination.SendAsync(
                new ArraySegment<byte>(buffer, 0, result.Count),
                result.MessageType,
                result.EndOfMessage,
                cancellationToken);
        }
    }
}
```

---

### Step 5: Register Voice Endpoints

Update `backend/WebApp.Api/Program.cs` to register the voice endpoints:

```csharp
// Add after existing endpoint mappings
app.UseWebSockets();
app.MapVoiceEndpoints();
```

---

### Step 6: Add Environment Variable

Add the Azure OpenAI endpoint to your configuration:

```powershell
# Add to your .env file in backend/WebApp.Api/
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
```

Or set via azd:

```powershell
azd env set AZURE_OPENAI_ENDPOINT "https://your-resource.openai.azure.com"
```

---

### Step 7: Test Locally

1. Start the development servers:

```powershell
.\deployment\scripts\start-local-dev.ps1
```

2. Open http://localhost:5173 in your browser

3. Click the **Voice** button to start speaking

4. Ask questions about your knowledge base:
   - "What products does TechCorp offer?"
   - "What is the return policy?"
   - "How can I contact support?"

5. The agent should respond with audio!

---

### Step 8: Deploy to Azure

Deploy your updated app with voice capabilities:

```powershell
azd deploy
```

---

## ✅ Validation Checklist

| Check | Status |
|-------|--------|
| VoiceChat component created | ⬜ |
| Backend voice endpoint added | ⬜ |
| Environment variables configured | ⬜ |
| Local testing works | ⬜ |
| Can speak and be understood | ⬜ |
| Agent responds with voice | ⬜ |
| RAG retrieval works via voice | ⬜ |

---

## 🎉 Congratulations!

You've successfully added voice capabilities to your RAG chatbot! Your agent can now:

- 🎤 Understand natural speech input
- 🔍 Query your knowledge base based on voice questions  
- 🗣️ Respond with natural, synthesized speech
- 📚 Cite sources from your documents

---

## 🔗 What You Built

```
┌─────────────────────────────────────────────────────────────────┐
│                  Foundry Agent Web App                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  React Frontend                                            │  │
│  │  ┌─────────────┐    ┌─────────────────────────────────┐   │  │
│  │  │ VoiceChat   │ ──▶│  WebSocket → Backend → Realtime │   │  │
│  │  │ Component   │    │       API Relay                 │   │  │
│  │  └─────────────┘    └─────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GPT Realtime API                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Speech Input → Processing → Speech Output                   ││
│  │       ↓              ↓              ↑                        ││
│  │  Transcription  →  RAG Agent  →  Voice Synthesis             ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Troubleshooting

### Common Issues

**Issue**: "Microphone permission denied"

**Solution**:
- Check browser settings for microphone access
- Use HTTPS (required for microphone in browsers)
- Try a different browser

---

**Issue**: "WebSocket connection failed"

**Solution**:
- Verify `AZURE_OPENAI_ENDPOINT` is set correctly
- Check that GPT Realtime model is deployed (Sub-Lab 2.1)
- Ensure WebSocket support is enabled in backend

---

**Issue**: "No audio output"

**Solution**:
- Check browser audio permissions
- Verify volume is not muted
- Check browser console for errors

---

## ➡️ Next Steps

- **Customize voices**: Try different voices for different use cases
- **Add interruption handling**: Allow users to interrupt the agent mid-response
- **Implement push-to-talk**: Add a toggle for manual voice control
- **Add visual feedback**: Show audio waveforms during recording

---

## 📚 Additional Resources

- [GPT Realtime Documentation](https://learn.microsoft.com/azure/ai-services/openai/realtime-audio)
- [Foundry Agent Web App Repository](https://github.com/microsoft-foundry/foundry-agent-webapp)
- [WebRTC Integration Guide](https://learn.microsoft.com/azure/ai-services/openai/realtime-audio-webrtc)

---

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) | [Back to Lab 1 →](../lab-1-rag-chatbot/README.md)
