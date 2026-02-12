# Sub-Lab 2.2: Add Voice to Your Agent

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) | [Next: Sub-Lab 2.3 →](./sub-lab-2.3-cleanup.md)

---

**⏱️ Estimated Time**: 30-40 minutes

## Overview

In this sub-lab, you'll add real-time voice capabilities to the Foundry Agent Web App you deployed in Sub-Lab 1.5. Users will be able to speak directly to your chatbot and receive spoken responses using the GPT Realtime model.

> **Note**: This sub-lab is **Code only** and builds on the Foundry Agent Web App from Sub-Lab 1.5.

---

## 🎓 Key Concepts

### Voice-Enabled Architecture

The Foundry Agent Web App uses a **text-based architecture** (HTTP + Server-Sent Events). To add voice, we'll integrate the **GPT Realtime API** which uses WebSockets for bidirectional audio streaming:

```
┌────────────────────────────────────────────────────────────────────┐
│                     Foundry Agent Web App                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  React Frontend                                               │  │
│  │  ┌───────────────────┐      ┌────────────────────────────┐   │  │
│  │  │  VoicePanel.tsx   │ ──▶  │  WebSocket Connection      │   │  │
│  │  │  - Mic capture    │      │  → Backend relay           │   │  │
│  │  │  - Audio playback │ ◀──  │  → Azure OpenAI Realtime   │   │  │
│  │  └───────────────────┘      └────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ASP.NET Core Backend                                         │  │
│  │  ┌────────────────────────────────────────────────────────┐   │  │
│  │  │  VoiceEndpoints.cs - WebSocket proxy to Realtime API   │   │  │
│  │  └────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                   Azure OpenAI GPT Realtime API                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Speech-to-Speech Model (gpt-realtime)                        │  │
│  │  - Voice Activity Detection (VAD)                             │  │
│  │  - Natural voice synthesis                                    │  │
│  │  - Function calling for RAG integration                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

### GPT Realtime vs Traditional Voice Pipeline

| Traditional Approach | GPT Realtime |
|---------------------|--------------|
| STT → LLM → TTS (3 services) | Single model handles everything |
| Higher latency (cumulative) | Low latency (~200-500ms) |
| No interruption handling | Natural interruptions supported |
| Separate voice config | Integrated voice selection |

### Voice Input Modes (Turn Detection)

| Mode | Description | Use Case |
|------|-------------|----------|
| **server_vad** | Server detects speech end based on silence | Natural conversations (recommended) |
| **semantic_vad** | Server detects speech end based on meaning | More natural turn-taking |
| **none** | Manual control (push-to-talk) | Noisy environments |

> 💡 **Important**: When using `server_vad` or `semantic_vad`, the server automatically detects when you stop speaking and triggers a response. You don't need to manually commit the audio buffer - the server handles this for you.

### Available Voices

| Voice | Description |
|-------|-------------|
| **alloy** | Neutral, balanced |
| **ash** | Warm tone |
| **coral** | Conversational |
| **echo** | Clear, direct |
| **sage** | Calm, thoughtful |
| **shimmer** | Soft, gentle (recommended) |

---

## 📋 Prerequisites

> 📝 **First time using the Code option?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.

- ✅ Completed [Sub-Lab 1.5](../lab-1-rag-chatbot/sub-lab-1.5-host-agent-webapp.md) - Foundry Agent Web App deployed
- ✅ Completed [Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) - GPT Realtime model deployed
- ✅ Your webapp folder from Sub-Lab 1.5

---

## 💻 Code Instructions

### Step 1: Navigate to Your Web App

Navigate to the webapp folder you created in Sub-Lab 1.5:

```powershell
cd lab-1-rag-chatbot/webapp
```

---

### Step 2: Configure Realtime Model Settings

Set the environment variables for the GPT Realtime model:

```powershell
# Set the Azure OpenAI endpoint (your AI Foundry services endpoint)
# Get this from your AI Foundry resource - it's the services URL without the project path
azd env set AZURE_OPENAI_ENDPOINT "https://<your-ai-foundry-resource>.services.ai.azure.com"

# Set the realtime model deployment name (from Sub-Lab 2.1)
azd env set AZURE_OPENAI_REALTIME_DEPLOYMENT "gpt-realtime"

# Set the voice (optional - defaults to shimmer)
azd env set AZURE_OPENAI_REALTIME_VOICE "shimmer"
```

> 💡 **Tip**: Your `AZURE_OPENAI_ENDPOINT` is your AI Foundry services URL without the `/api/projects/...` path. For example, if your `AI_AGENT_ENDPOINT` is `https://my-foundry.services.ai.azure.com/api/projects/my-project`, then your `AZURE_OPENAI_ENDPOINT` is `https://my-foundry.services.ai.azure.com`.

---

### Step 3: Add Backend Voice Endpoint

Create a new folder and file in the `lab-1-rag-chatbot/webapp/backendWebApp.Api` folder 
Create a folder named `Endpoints`and a file `VoiceEndpoints.cs` inside that folder:

```csharp
using System.Net.WebSockets;
using Azure.Identity;

namespace WebApp.Api.Endpoints;

public static class VoiceEndpoints
{
    public static void MapVoiceEndpoints(this WebApplication app)
    {
        app.Map("/api/voice/realtime", async (HttpContext context) =>
        {
            if (!context.WebSockets.IsWebSocketRequest)
            {
                context.Response.StatusCode = StatusCodes.Status400BadRequest;
                await context.Response.WriteAsync("WebSocket connection required");
                return;
            }

            using var clientSocket = await context.WebSockets.AcceptWebSocketAsync();
            await ProxyToRealtimeApi(clientSocket, context.RequestAborted);
        });
    }

    private static async Task ProxyToRealtimeApi(
        WebSocket clientSocket,
        CancellationToken cancellationToken)
    {
        // Get configuration
        var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
            ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT not configured");
        
        var deployment = Environment.GetEnvironmentVariable("AZURE_OPENAI_REALTIME_DEPLOYMENT")
            ?? "gpt-realtime";  // Default matches Portal deployment name
        
        var apiVersion = "2025-04-01-preview";

        // Get access token using managed identity
        var credential = new DefaultAzureCredential();
        var tokenResult = await credential.GetTokenAsync(
            new Azure.Core.TokenRequestContext(
                ["https://cognitiveservices.azure.com/.default"]),
            cancellationToken);

        // Build WebSocket URL for Azure OpenAI Realtime API
        var wsEndpoint = endpoint.Replace("https://", "wss://");
        var realtimeUrl = $"{wsEndpoint}/openai/realtime?api-version={apiVersion}&deployment={deployment}";

        // Connect to Azure OpenAI Realtime API
        using var realtimeSocket = new ClientWebSocket();
        realtimeSocket.Options.SetRequestHeader("Authorization", $"Bearer {tokenResult.Token}");
        
        try
        {
            await realtimeSocket.ConnectAsync(new Uri(realtimeUrl), cancellationToken);
            Console.WriteLine("Connected to Azure OpenAI Realtime API");

            // Relay messages bidirectionally
            var clientToRealtime = RelayMessagesAsync(
                clientSocket, realtimeSocket, "Client→Realtime", cancellationToken);
            var realtimeToClient = RelayMessagesAsync(
                realtimeSocket, clientSocket, "Realtime→Client", cancellationToken);

            // Wait for either direction to complete (usually means disconnect)
            await Task.WhenAny(clientToRealtime, realtimeToClient);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Realtime connection error: {ex.Message}");
            throw;
        }
    }

    private static async Task RelayMessagesAsync(
        WebSocket source,
        WebSocket destination,
        string direction,
        CancellationToken cancellationToken)
    {
        var buffer = new byte[16384];

        try
        {
            while (source.State == WebSocketState.Open && 
                   destination.State == WebSocketState.Open &&
                   !cancellationToken.IsCancellationRequested)
            {
                var result = await source.ReceiveAsync(buffer, cancellationToken);

                if (result.MessageType == WebSocketMessageType.Close)
                {
                    Console.WriteLine($"{direction}: Received close message");
                    if (destination.State == WebSocketState.Open)
                    {
                        await destination.CloseAsync(
                            WebSocketCloseStatus.NormalClosure,
                            "Closing",
                            cancellationToken);
                    }
                    break;
                }

                if (destination.State == WebSocketState.Open)
                {
                    await destination.SendAsync(
                        new ArraySegment<byte>(buffer, 0, result.Count),
                        result.MessageType,
                        result.EndOfMessage,
                        cancellationToken);
                }
            }
        }
        catch (WebSocketException ex) when (ex.WebSocketErrorCode == WebSocketError.ConnectionClosedPrematurely)
        {
            Console.WriteLine($"{direction}: Connection closed");
        }
    }
}
```

---

### Step 4: Register Voice Endpoints and WebSockets

Update the existing file `backend/WebApp.Api/Program.cs` to enable WebSockets and register the voice endpoints.

**First, add the using statement at the top of the file (with the other using statements):**

```csharp
using WebApp.Api.Endpoints;
```

**Then, after `app.UseAuthorization()` add:**

```csharp
// Enable WebSockets for voice
app.UseWebSockets(new WebSocketOptions
{
    KeepAliveInterval = TimeSpan.FromSeconds(30)
});

// Map voice endpoints
app.MapVoiceEndpoints();
```
   <img src="images/websocket.png" width="400"/>
---

### Step 5: Create Frontend Audio Utilities

Create a new file `frontend/src/utils/audioUtils.ts` to handle PCM16 audio conversion:

```typescript
/**
 * Audio utilities for GPT Realtime API integration
 * The Realtime API expects PCM16 audio at 24kHz sample rate
 */

const SAMPLE_RATE = 24000;

/**
 * Creates an AudioContext configured for the Realtime API
 */
export function createAudioContext(): AudioContext {
  return new AudioContext({ sampleRate: SAMPLE_RATE });
}

/**
 * Converts a Float32Array to base64-encoded PCM16
 */
export function floatTo16BitPCM(float32Array: Float32Array): ArrayBuffer {
  const buffer = new ArrayBuffer(float32Array.length * 2);
  const view = new DataView(buffer);
  
  for (let i = 0; i < float32Array.length; i++) {
    const s = Math.max(-1, Math.min(1, float32Array[i]));
    view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }
  
  return buffer;
}

/**
 * Converts base64-encoded PCM16 to Float32Array for playback
 */
export function base64ToFloat32Array(base64: string): Float32Array {
  const binaryString = atob(base64);
  const bytes = new Uint8Array(binaryString.length);
  
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  
  const int16Array = new Int16Array(bytes.buffer);
  const float32Array = new Float32Array(int16Array.length);
  
  for (let i = 0; i < int16Array.length; i++) {
    float32Array[i] = int16Array[i] / 0x8000;
  }
  
  return float32Array;
}

/**
 * Converts an ArrayBuffer to base64 string
 */
export function arrayBufferToBase64(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

/**
 * Audio player that queues and plays PCM16 audio chunks
 */
export class AudioPlayer {
  private audioContext: AudioContext;
  private scheduledTime: number = 0;

  constructor() {
    this.audioContext = createAudioContext();
  }

  async play(base64Audio: string): Promise<void> {
    if (this.audioContext.state === 'suspended') {
      await this.audioContext.resume();
    }

    const floatData = base64ToFloat32Array(base64Audio);
    const audioBuffer = this.audioContext.createBuffer(1, floatData.length, SAMPLE_RATE);
    audioBuffer.getChannelData(0).set(floatData);

    const source = this.audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(this.audioContext.destination);

    // Schedule playback
    const startTime = Math.max(this.audioContext.currentTime, this.scheduledTime);
    source.start(startTime);
    this.scheduledTime = startTime + audioBuffer.duration;
  }

  stop(): void {
    this.scheduledTime = 0;
  }

  async close(): Promise<void> {
    await this.audioContext.close();
  }
}

/**
 * Audio recorder that captures microphone input and converts to PCM16
 */
export class AudioRecorder {
  private audioContext: AudioContext | null = null;
  private mediaStream: MediaStream | null = null;
  private processor: ScriptProcessorNode | null = null;
  private onAudioData: ((base64: string) => void) | null = null;

  async start(onAudioData: (base64: string) => void): Promise<void> {
    this.onAudioData = onAudioData;

    // Get microphone access
    this.mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: SAMPLE_RATE,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true,
      }
    });

    this.audioContext = createAudioContext();
    const source = this.audioContext.createMediaStreamSource(this.mediaStream);

    // Create processor for capturing audio data
    // Note: ScriptProcessorNode is deprecated but widely supported
    // For production, consider AudioWorklet
    this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
    
    this.processor.onaudioprocess = (event) => {
      const inputData = event.inputBuffer.getChannelData(0);
      const pcm16 = floatTo16BitPCM(inputData);
      const base64 = arrayBufferToBase64(pcm16);
      this.onAudioData?.(base64);
    };

    source.connect(this.processor);
    this.processor.connect(this.audioContext.destination);
  }

  stop(): void {
    this.processor?.disconnect();
    this.mediaStream?.getTracks().forEach(track => track.stop());
    this.audioContext?.close();
    
    this.processor = null;
    this.mediaStream = null;
    this.audioContext = null;
    this.onAudioData = null;
  }
}
```

---

### Step 6: Create Voice Panel Component

Create a new file `frontend/src/components/VoicePanel.tsx`:

```tsx
import { useState, useRef, useCallback, useEffect } from 'react';
import {
  Button,
  Card,
  CardHeader,
  Text,
  Spinner,
  makeStyles,
  tokens,
} from '@fluentui/react-components';
import {
  Mic24Regular,
  Mic24Filled,
  Call24Regular,
  CallEnd24Regular,
  Dismiss24Regular,
} from '@fluentui/react-icons';
import { AudioPlayer, AudioRecorder } from '../utils/audioUtils';

const useStyles = makeStyles({
  // Collapsed state - just a floating button
  collapsedButton: {
    position: 'fixed',
    bottom: '100px',
    right: '20px',
    zIndex: 1000,
    borderRadius: '50%',
    width: '56px',
    height: '56px',
    boxShadow: tokens.shadow16,
  },
  // Expanded panel
  container: {
    position: 'fixed',
    bottom: '100px',
    right: '20px',
    width: '320px',
    zIndex: 1000,
    display: 'flex',
    flexDirection: 'column',
    gap: tokens.spacingVerticalS,
    padding: tokens.spacingHorizontalM,
    boxShadow: tokens.shadow16,
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  controls: {
    display: 'flex',
    gap: tokens.spacingHorizontalS,
    alignItems: 'center',
    justifyContent: 'center',
  },
  status: {
    display: 'flex',
    alignItems: 'center',
    gap: tokens.spacingHorizontalXS,
  },
  recording: {
    color: tokens.colorPaletteRedForeground1,
  },
  connected: {
    color: tokens.colorPaletteGreenForeground1,
  },
  transcript: {
    maxHeight: '150px',
    overflowY: 'auto',
    padding: tokens.spacingHorizontalS,
    backgroundColor: tokens.colorNeutralBackground2,
    borderRadius: tokens.borderRadiusMedium,
    fontSize: tokens.fontSizeBase200,
  },
  closeButton: {
    position: 'absolute',
    top: tokens.spacingVerticalS,
    right: tokens.spacingHorizontalS,
  },
});

// Realtime API message types
interface RealtimeMessage {
  type: string;
  [key: string]: unknown;
}

interface SessionConfig {
  modalities: string[];
  voice: string;
  input_audio_format: string;
  output_audio_format: string;
  input_audio_transcription: {
    model: string;
  };
  turn_detection: {
    type: string;
    threshold: number;
    prefix_padding_ms: number;
    silence_duration_ms: number;
  };
}

export const VoicePanel: React.FC = () => {
  const styles = useStyles();
  
  const [isExpanded, setIsExpanded] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const audioPlayerRef = useRef<AudioPlayer | null>(null);
  const audioRecorderRef = useRef<AudioRecorder | null>(null);
  const audioSentRef = useRef<boolean>(false);

  // Connect to the voice endpoint
  const connect = useCallback(async () => {
    setIsConnecting(true);
    setError(null);

    try {
      // Determine WebSocket URL
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/api/voice/realtime`;

      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setIsConnecting(false);

        // Initialize audio player
        audioPlayerRef.current = new AudioPlayer();

        // Send session configuration
        const sessionConfig: SessionConfig = {
          modalities: ['text', 'audio'],
          voice: 'shimmer',
          input_audio_format: 'pcm16',
          output_audio_format: 'pcm16',
          input_audio_transcription: {
            model: 'whisper-1',
          },
          turn_detection: {
            type: 'server_vad',
            threshold: 0.5,
            prefix_padding_ms: 300,
            silence_duration_ms: 800,
          },
        };

        ws.send(JSON.stringify({
          type: 'session.update',
          session: sessionConfig,
        }));
      };

      ws.onmessage = (event) => {
        const message: RealtimeMessage = JSON.parse(event.data);
        handleRealtimeMessage(message);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        setIsRecording(false);
        cleanup();
      };

      ws.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError('Connection failed. Please try again.');
        setIsConnecting(false);
      };

    } catch (err) {
      console.error('Failed to connect:', err);
      setError('Failed to connect to voice service');
      setIsConnecting(false);
    }
  }, []);

  // Handle messages from Realtime API
  const handleRealtimeMessage = useCallback((message: RealtimeMessage) => {
    switch (message.type) {
      case 'session.created':
        console.log('Session created');
        break;

      case 'session.updated':
        console.log('Session updated');
        break;

      case 'conversation.item.input_audio_transcription.completed':
        // User's speech was transcribed
        const userText = message.transcript as string;
        if (userText) {
          setTranscript(prev => [...prev, `You: ${userText}`]);
        }
        break;

      case 'response.audio_transcript.delta':
        // Streaming assistant text (for display)
        break;

      case 'response.audio_transcript.done':
        // Final assistant transcript
        const assistantText = message.transcript as string;
        if (assistantText) {
          setTranscript(prev => [...prev, `Assistant: ${assistantText}`]);
        }
        break;

      case 'response.audio.delta':
        // Audio chunk from assistant - play it
        const audioData = message.delta as string;
        if (audioData && audioPlayerRef.current) {
          audioPlayerRef.current.play(audioData);
        }
        break;

      case 'response.audio.done':
        console.log('Audio response complete');
        break;

      case 'error':
        console.error('Realtime API error:', message);
        const errorMsg = (message.error as { message?: string })?.message || 'An error occurred';
        // Don't show buffer errors to user - server_vad handles these automatically
        if (!errorMsg.includes('buffer')) {
          setError(errorMsg);
        }
        break;

      default:
        // Log other message types for debugging
        if (message.type.startsWith('error')) {
          console.error('Error message:', message);
        }
    }
  }, []);

  // Start recording
  const startRecording = useCallback(async () => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      setError('Not connected');
      return;
    }

    try {
      audioRecorderRef.current = new AudioRecorder();
      audioSentRef.current = false;
      
      await audioRecorderRef.current.start((base64Audio) => {
        // Send audio to Realtime API
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({
            type: 'input_audio_buffer.append',
            audio: base64Audio,
          }));
          audioSentRef.current = true;
        }
      });

      setIsRecording(true);
      setError(null);
    } catch (err) {
      console.error('Failed to start recording:', err);
      setError('Failed to access microphone. Please check permissions.');
    }
  }, []);

  // Stop recording
  const stopRecording = useCallback(() => {
    audioRecorderRef.current?.stop();
    audioRecorderRef.current = null;
    setIsRecording(false);
    // Note: With server_vad enabled, the server automatically detects speech end
    // and triggers a response. No manual commit needed.
    audioSentRef.current = false;
  }, []);

  // Disconnect
  const disconnect = useCallback(() => {
    cleanup();
    wsRef.current?.close();
    wsRef.current = null;
    setIsConnected(false);
    setIsRecording(false);
  }, []);

  // Cleanup resources
  const cleanup = useCallback(() => {
    audioRecorderRef.current?.stop();
    audioRecorderRef.current = null;
    audioPlayerRef.current?.stop();
    audioPlayerRef.current?.close();
    audioPlayerRef.current = null;
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanup();
      wsRef.current?.close();
    };
  }, [cleanup]);

  // Collapsed state - just a floating mic button
  if (!isExpanded) {
    return (
      <Button
        className={styles.collapsedButton}
        appearance="primary"
        icon={<Mic24Regular />}
        onClick={() => setIsExpanded(true)}
        title="Open Voice Chat"
      />
    );
  }

  // Expanded state - full panel
  return (
    <Card className={styles.container}>
      <Button
        className={styles.closeButton}
        appearance="subtle"
        icon={<Dismiss24Regular />}
        size="small"
        onClick={() => {
          if (!isRecording) {
            setIsExpanded(false);
          }
        }}
        title="Minimize"
      />
      
      <CardHeader
        header={<Text weight="semibold">🎤 Voice Chat</Text>}
        description={
          <div className={styles.status}>
            {isConnected ? (
              <Text size={200} className={styles.connected}>● Connected</Text>
            ) : isConnecting ? (
              <Text size={200}>Connecting...</Text>
            ) : (
              <Text size={200}>Click to start</Text>
            )}
            {isRecording && (
              <Text size={200} className={styles.recording}> ● Recording</Text>
            )}
          </div>
        }
      />

      <div className={styles.controls}>
        {!isConnected ? (
          <Button
            appearance="primary"
            icon={isConnecting ? <Spinner size="tiny" /> : <Call24Regular />}
            onClick={connect}
            disabled={isConnecting}
          >
            {isConnecting ? 'Connecting...' : 'Start'}
          </Button>
        ) : (
          <>
            <Button
              appearance={isRecording ? 'primary' : 'secondary'}
              icon={isRecording ? <Mic24Filled /> : <Mic24Regular />}
              onClick={isRecording ? stopRecording : startRecording}
            >
              {isRecording ? 'Stop' : 'Talk'}
            </Button>
            <Button
              appearance="subtle"
              icon={<CallEnd24Regular />}
              onClick={disconnect}
            >
              End
            </Button>
          </>
        )}
      </div>

      {error && (
        <Text size={200} style={{ color: tokens.colorPaletteRedForeground1 }}>
          {error}
        </Text>
      )}

      {transcript.length > 0 && (
        <div className={styles.transcript}>
          {transcript.slice(-3).map((line, i) => (
            <Text key={i} block size={200} style={{ marginBottom: '4px' }}>
              {line}
            </Text>
          ))}
        </div>
      )}
    </Card>
  );
};
```

> **Note**: The VoicePanel displays as a collapsible floating button in the bottom-right corner. Click the mic button to expand it, then click "Start" to connect. Once connected, click "Talk" and speak - the server will automatically detect when you're done and respond with audio. The panel shows only the last 3 transcript lines for a cleaner UI.

---

### Step 7: Add Voice Panel to the App

Update `frontend/src/App.tsx` to include the VoicePanel. Find the main layout section and add the VoicePanel component.

First, add the import at the top:

```tsx
import { VoicePanel } from './components/VoicePanel';
```

Then add the component to your layout. The exact location depends on your UI preference, but a common approach is to add it alongside or below the chat interface. (E.g. on line 96 just after the agent preview)

```tsx
{/* Add Voice Panel */}
<VoicePanel />
```
   <img src="images/voicepanel.png" width="400"/>

---

### Step 8: Update Infrastructure for Voice Environment Variables

The voice endpoint needs the `AZURE_OPENAI_ENDPOINT` environment variable to connect to the Realtime API. Update your Bicep files to pass this value.

**8a. Update `infra/main.bicep`**

Add the new parameter near the existing parameters (around line 20-30):

```bicep
@description('Azure OpenAI endpoint for Realtime API')
param azureOpenAiEndpoint string = ''
```

Then, in the module call to `main-app.bicep` (around line 90), add the parameter:

```bicep
module app 'main-app.bicep' = {
  name: 'app'
  params: {
    // ... existing params ...
    azureOpenAiEndpoint: azureOpenAiEndpoint
  }
}
```

**8b. Update `infra/main-app.bicep`**

Add the parameter at the top:

```bicep
@description('Azure OpenAI endpoint for Realtime API')
param azureOpenAiEndpoint string = ''
```

Then in the `appEnv` variable (where environment variables are defined), add:

```bicep
var appEnv = [
  // ... existing env vars ...
  {
    name: 'AZURE_OPENAI_ENDPOINT'
    value: azureOpenAiEndpoint
  }
  {
    name: 'AZURE_OPENAI_REALTIME_DEPLOYMENT'
    value: 'gpt-realtime'
  }
  {
    name: 'AZURE_OPENAI_REALTIME_VOICE'
    value: 'shimmer'
  }
]
```

> 💡 **Tip**: If you're using `azd`, the environment variables you set in Step 2 will be automatically picked up during deployment.

---

### Step 9: Verify WebSocket Configuration

Azure Container Apps supports WebSockets by default. Verify your configuration is correct:

1. Open `container-app.bicep` in the `webapp/infra/core/host` folder
2. Find the ingress configuration (around line 27) and confirm it looks like this:

```bicep
ingress: enableIngress ? {
  external: external
  targetPort: targetPort
  transport: 'auto'  // 'auto' or 'http' both support WebSockets
  allowInsecure: false
} : null
```

> 💡 **Note**: The default template already has `transport: 'auto'` which supports WebSockets. If your configuration matches the above, no changes are needed.

---

### Step 10: Deploy to Azure

Deploy your updated app with voice capabilities:

```powershell
azd deploy
```

**Get your deployed URL:**

If your browser didn't open automatically, you can get the URL with:

```powershell
azd env get-values | Select-String "WEB_ENDPOINT"
```

**Test voice chat:**

1. Open the URL in your browser
2. Sign in with your Microsoft account
3. Click **"Start Voice Chat"** to connect
4. Click **"Talk"** and ask a question about your knowledge base
5. Release to let the server detect end of speech
6. Listen to the spoken response!

**Try these questions:**
- "What products does TechCorp offer?"
- "What is the return policy?"
- "How do I contact support?"

---

## 🔧 Troubleshooting

### "WebSocket connection failed"

1. Check that WebSockets are enabled on your Container App
2. Verify the `AZURE_OPENAI_ENDPOINT` is set correctly (it should be the base URL like `https://your-resource.services.ai.azure.com`, not the project URL)
3. Check that the managed identity has access to Azure OpenAI

### "Buffer too small" errors in console

This error can be safely ignored when using `server_vad` mode. The server automatically handles turn detection and may occasionally report this when you pause briefly. The code already filters these errors from the UI.

### "Failed to access microphone"

1. Ensure your site is served over HTTPS (required for microphone access)
2. Check browser permissions for microphone access
3. Try a different browser if issues persist

### No audio playback

1. Check browser console for errors
2. Ensure the AudioContext is not suspended (requires user interaction)
3. Verify the `output_audio_format` matches what the player expects

### High latency

1. Consider using `semantic_vad` for more natural turn detection
2. Reduce `silence_duration_ms` in the session config
3. Check network latency to your Azure region

---

## ✅ Validation Checklist

| Check | Status |
|-------|--------|
| VoiceEndpoints.cs created | ⬜ |
| WebSockets enabled in Program.cs | ⬜ |
| audioUtils.ts created | ⬜ |
| VoicePanel.tsx created | ⬜ |
| VoicePanel added to App | ⬜ |
| Infrastructure bicep updated | ⬜ |
| Environment variables configured | ⬜ |
| Can speak and be understood | ⬜ |
| Receives spoken responses | ⬜ |
| Deployed to Azure successfully | ⬜ |

---

## 🎉 Congratulations!

You've successfully added voice capabilities to your chatbot! Your agent can now:

- 🎤 Listen to natural speech input
- 🧠 Process questions using the GPT Realtime model
- 🗣️ Respond with natural, synthesized speech
- 📝 Show transcripts of the conversation

---

## ➡️ Next Steps

- **Try different voices**: Change `voice` in VoicePanel.tsx to `alloy`, `ash`, `coral`, `echo`, or `sage`
- **Add push-to-talk mode**: Set `turn_detection.type` to `"none"` for manual control
- **Integrate with RAG**: Add function calling to query your knowledge base
- **Add visual feedback**: Show audio waveforms during recording
- **Adjust sensitivity**: Modify `silence_duration_ms` (lower = faster response, higher = more natural pauses)

---

## 📚 Additional Resources

- [Azure OpenAI Realtime Audio Documentation](https://learn.microsoft.com/azure/ai-services/openai/realtime-audio)
- [Azure OpenAI Realtime API Reference](https://learn.microsoft.com/azure/ai-services/openai/realtime-audio-reference)
- [Foundry Agent Web App Repository](https://github.com/microsoft-foundry/foundry-agent-webapp)
- [Azure Samples - Realtime Audio SDK](https://github.com/Azure-Samples/aoai-realtime-audio-sdk)

---

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) | [Next: Sub-Lab 2.3 →](./sub-lab-2.3-cleanup.md)
