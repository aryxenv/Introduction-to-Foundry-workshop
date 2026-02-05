# Lab 2: Adding Voice Capabilities to Your Chatbot

## 🎯 Lab Overview

In this lab, you'll enhance your RAG chatbot from Lab 1 by adding voice capabilities using Azure Speech Services. By the end of this lab, users will be able to interact with your chatbot using voice input and receive audio responses, all deployed on Azure AI Foundry.

**Estimated Time**: 1-2 hours

**Prerequisites**: Completion of Lab 1

## 📖 What You'll Learn

- **Azure Speech Services**: Speech-to-Text (STT) and Text-to-Speech (TTS)
- **Audio Processing**: Handling audio streams and formats
- **Real-time Communication**: WebSockets for streaming audio
- **Voice UI Design**: Best practices for voice interfaces
- **Integration**: Connecting voice capabilities with existing RAG chatbot

## 🏗️ Architecture Overview

### Voice-Enabled Architecture

```
User Voice Input → Azure Speech (STT) → Text Query
                                            ↓
                                       RAG Chatbot
                                            ↓
Text Response → Azure Speech (TTS) → Audio Response
```

**New Components:**
- **Azure Speech Service**: Handles STT and TTS
- **Audio Handler**: Manages audio input/output
- **WebSocket Server**: Enables real-time audio streaming
- **Voice UI**: Frontend for voice interaction

### How It Works

1. User speaks into microphone
2. Audio captured and sent to Azure Speech STT
3. Speech converted to text
4. Text sent to RAG chatbot (from Lab 1)
5. Chatbot generates text response
6. Text converted to speech using Azure TTS
7. Audio response played to user

## 📋 Prerequisites

Before starting, ensure you have:

- [ ] Completed Lab 1 successfully
- [ ] Working RAG chatbot from Lab 1
- [ ] Azure subscription (same as Lab 1)
- [ ] Microphone and speakers/headphones
- [ ] Modern web browser with microphone access

## 🛠️ Step-by-Step Instructions

### Step 1: Azure Speech Service Setup (15 minutes)

#### 1.1 Create Azure Speech Service

**Using Azure Portal:**

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Search for "Speech Service"
3. Click "Create"
4. Fill in details:
   - Resource group: `rg-foundry-chatbot-workshop` (same as Lab 1)
   - Region: Choose closest to you
   - Name: `speech-chatbot-workshop`
   - Pricing tier: Free F0 (sufficient for workshop)
5. Click "Review + Create"
6. After creation, go to "Keys and Endpoint":
   - Note **Key 1**
   - Note **Region**

**Using Azure CLI:**

```bash
# Create Speech Service
az cognitiveservices account create \
  --name speech-chatbot-workshop \
  --resource-group rg-foundry-chatbot-workshop \
  --kind SpeechServices \
  --sku F0 \
  --location eastus

# Get keys
az cognitiveservices account keys list \
  --name speech-chatbot-workshop \
  --resource-group rg-foundry-chatbot-workshop
```

#### 1.2 Update Environment Configuration

Add to your `.env` file:

```properties
# Azure Speech Service Configuration
AZURE_SPEECH_KEY=your-speech-service-key
AZURE_SPEECH_REGION=eastus

# Voice Configuration
STT_LANGUAGE=en-US
TTS_VOICE_NAME=en-US-JennyNeural
TTS_VOICE_STYLE=friendly
AUDIO_FORMAT=riff-24khz-16bit-mono-pcm
```

**Voice Options:**
- `en-US-JennyNeural`: Natural female voice
- `en-US-GuyNeural`: Natural male voice
- `en-US-AriaNeural`: Expressive female voice
- `en-GB-SoniaNeural`: British female voice

See [full list of voices](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)

### Step 2: Understanding Speech Services (20 minutes)

#### 2.1 Speech-to-Text (STT)

**How it works:**
1. Capture audio from microphone
2. Stream audio to Azure Speech Service
3. Receive transcribed text in real-time
4. Handle recognition events (started, recognized, canceled)

**Key Concepts:**

- **Continuous Recognition**: Keeps listening until stopped
- **Single Shot Recognition**: Recognizes one utterance
- **Language Models**: Optimized for different scenarios (general, conversation, dictation)
- **Custom Models**: Train on your own data (advanced)

**Code Example:**
```python
import azure.cognitiveservices.speech as speechsdk

# Configure speech recognizer
speech_config = speechsdk.SpeechConfig(
    subscription=AZURE_SPEECH_KEY,
    region=AZURE_SPEECH_REGION
)
speech_config.speech_recognition_language = "en-US"

# Create recognizer
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config
)

# Start recognition
result = recognizer.recognize_once()
print(f"Recognized: {result.text}")
```

#### 2.2 Text-to-Speech (TTS)

**How it works:**
1. Send text to Azure Speech Service
2. Specify voice and language
3. Receive audio stream
4. Play audio to user

**Key Concepts:**

- **Neural Voices**: High-quality, natural-sounding voices
- **Voice Styles**: Emotional and speaking styles
- **SSML**: Speech Synthesis Markup Language for fine control
- **Audio Formats**: Various formats for different use cases

**Code Example:**
```python
# Configure speech synthesizer
speech_config = speechsdk.SpeechConfig(
    subscription=AZURE_SPEECH_KEY,
    region=AZURE_SPEECH_REGION
)
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

# Create synthesizer
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

# Synthesize speech
result = synthesizer.speak_text("Hello! How can I help you today?")
```

### Step 3: Implement Voice Handler (30 minutes)

#### 3.1 Review Voice Handler Implementation

Navigate to `lab-2-voice-capabilities` and examine `src/voice_handler.py`:

```python
class VoiceHandler:
    """
    Handles speech-to-text and text-to-speech operations
    
    Key methods:
    - transcribe_audio(): Convert speech to text
    - synthesize_speech(): Convert text to speech
    - start_continuous_recognition(): Real-time STT
    """
```

**Key Features:**

1. **Async Support**: Non-blocking operations
2. **Error Handling**: Graceful failures
3. **Events**: Callbacks for recognition events
4. **Streaming**: Real-time audio processing

#### 3.2 Test Voice Handler

Run the interactive voice test:

```bash
cd lab-2-voice-capabilities

# Install dependencies
pip install -r requirements.txt

# Test speech recognition
python scripts/test_speech_recognition.py

# Test speech synthesis
python scripts/test_speech_synthesis.py
```

**Speech Recognition Test:**
```
🎤 Speech Recognition Test
Speak now... (say 'stop' to quit)

> You said: "Hello, how are you?"
> You said: "What products does TechCorp offer?"
> You said: "stop"

Test complete!
```

**Speech Synthesis Test:**
```
🔊 Speech Synthesis Test
Enter text to speak (or 'quit' to exit):

> Hello world
🔊 Playing: "Hello world"
✅ Speech synthesis complete

> quit
```

### Step 4: Integrate Voice with RAG Chatbot (30 minutes)

#### 4.1 Review Integration Architecture

The integrated system combines:
- Voice Handler (new)
- RAG Chatbot (from Lab 1)
- API with voice endpoints (extended)

**New Workflow:**
```
Voice Input → STT → Text → RAG → Response Text → TTS → Voice Output
```

#### 4.2 Review Enhanced API

Open `src/voice_api.py` to see new endpoints:

**New Endpoints:**
- `POST /api/voice/chat` - Voice-to-voice chat
- `POST /api/voice/transcribe` - Audio to text
- `POST /api/voice/synthesize` - Text to audio
- `GET /api/voice/voices` - List available voices

**Example Voice Chat Endpoint:**
```python
@app.post("/api/voice/chat")
async def voice_chat(audio_file: UploadFile):
    """
    Complete voice interaction:
    1. Transcribe audio to text
    2. Get chatbot response
    3. Synthesize response to audio
    4. Return audio file
    """
    # Transcribe
    text = await voice_handler.transcribe(audio_file)
    
    # Get response
    response = await chatbot.chat(text)
    
    # Synthesize
    audio = await voice_handler.synthesize(response.response)
    
    return audio
```

#### 4.3 Test Enhanced API

Start the server with voice capabilities:

```bash
uvicorn src.voice_api:app --reload --port 8000
```

Test using the interactive docs: `http://localhost:8000/docs`

**Try the endpoints:**

1. **Test Transcription:**
   - Go to `/api/voice/transcribe`
   - Upload an audio file (WAV, MP3)
   - See the transcribed text

2. **Test Synthesis:**
   - Go to `/api/voice/synthesize`
   - Enter text: "Hello, this is a test"
   - Download and play the audio file

3. **Test Voice Chat:**
   - Go to `/api/voice/chat`
   - Upload audio with a question
   - Receive audio response

### Step 5: Build Voice-Enabled Web Interface (30 minutes)

#### 5.1 Understanding the Web Interface

The web interface provides:
- Microphone access
- Real-time audio visualization
- Voice activation detection (VAD)
- Audio playback
- Text display

**Technology Stack:**
- HTML5 Audio APIs
- JavaScript MediaRecorder
- WebSocket for streaming (optional)
- Bootstrap for styling

#### 5.2 Review Web Interface Code

Open `web/index.html`:

**Key Components:**

1. **Microphone Access:**
```javascript
// Request microphone permission
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

// Create recorder
const mediaRecorder = new MediaRecorder(stream);

// Handle recorded data
mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
};
```

2. **Audio Visualization:**
```javascript
// Create audio context
const audioContext = new AudioContext();
const analyser = audioContext.createAnalyser();

// Visualize audio levels
function visualize() {
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(dataArray);
    // Draw visualization
}
```

3. **Sending Audio to API:**
```javascript
async function sendAudioToAPI(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    
    const response = await fetch('/api/voice/chat', {
        method: 'POST',
        body: formData
    });
    
    const audioResponse = await response.blob();
    playAudio(audioResponse);
}
```

#### 5.3 Run the Web Interface

Serve the web interface:

```bash
# Simple Python server
cd web
python -m http.server 8080

# Or use the provided server script
python scripts/serve_web.py
```

Open in browser: `http://localhost:8080`

**Try it out:**

1. Click "Allow" when prompted for microphone access
2. Click the microphone button to start recording
3. Ask a question: "What are your office hours?"
4. Release the button
5. See transcribed text
6. Hear the audio response
7. Read the text response

### Step 6: Advanced Features (20 minutes)

#### 6.1 Voice Activity Detection (VAD)

Automatically detect when user starts/stops speaking:

```python
# In voice_handler.py
def detect_speech_end(self, audio_level, threshold=30, silence_duration=1.5):
    """
    Detect when user has stopped speaking
    - Monitor audio levels
    - Track silence duration
    - Trigger end of speech event
    """
    if audio_level < threshold:
        self.silence_start = time.time()
    else:
        self.silence_start = None
    
    if self.silence_start:
        silence_time = time.time() - self.silence_start
        if silence_time > silence_duration:
            return True
    
    return False
```

#### 6.2 SSML for Enhanced TTS

Use SSML for more control over speech synthesis:

```python
# Example SSML
ssml = f"""
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <prosody rate="medium" pitch="medium">
            {response_text}
        </prosody>
    </voice>
</speak>
"""

result = synthesizer.speak_ssml(ssml)
```

**SSML Features:**
- Adjust speaking rate
- Change pitch
- Add pauses: `<break time="500ms"/>`
- Emphasize words: `<emphasis level="strong">important</emphasis>`
- Control pronunciation

#### 6.3 Custom Wake Word

Implement wake word detection (e.g., "Hey TechBot"):

```python
# Using pattern matching on transcribed text
def check_wake_word(text, wake_word="hey techbot"):
    text_lower = text.lower()
    if wake_word in text_lower:
        # Extract command after wake word
        command = text_lower.split(wake_word, 1)[1].strip()
        return True, command
    return False, None
```

#### 6.4 Multi-Language Support

Support multiple languages:

```python
# Language detection
from langdetect import detect

def get_voice_for_language(language):
    voices = {
        'en': 'en-US-JennyNeural',
        'es': 'es-ES-ElviraNeural',
        'fr': 'fr-FR-DeniseNeural',
        'de': 'de-DE-KatjaNeural',
        'ja': 'ja-JP-NanamiNeural'
    }
    return voices.get(language, 'en-US-JennyNeural')

# Auto-detect and use appropriate voice
detected_lang = detect(response_text)
voice = get_voice_for_language(detected_lang)
```

### Step 7: Deploy Voice-Enabled Chatbot (30 minutes)

#### 7.1 Update Docker Configuration

Review updated `Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Install system dependencies for audio
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY web/ ./web/

# Expose ports
EXPOSE 8000

CMD ["uvicorn", "src.voice_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 7.2 Test Docker Container

Build and test locally:

```bash
# Build image
docker build -t rag-chatbot-voice:latest .

# Run container
docker run -p 8000:8000 --env-file .env rag-chatbot-voice:latest

# Test in browser
open http://localhost:8000
```

#### 7.3 Deploy to Azure AI Foundry

Update your Azure AI Foundry project to include voice capabilities:

**Option A: Update Existing Deployment**

1. **Add Speech Service Connection**
   - In Azure AI Foundry, go to your project
   - Navigate to "Settings" → "Connections"
   - Add Azure Speech Service connection:
     - Name: `speech-connection`
     - Select your Speech Service resource
     - Authenticate

2. **Update Prompt Flow or Deployment**
   - If using Prompt Flow: Add audio input/output nodes
   - If using direct deployment: Update your endpoint configuration

**Option B: Deploy Updated Web App**

```bash
# Update environment variables
az webapp config appsettings set \
  --name rag-chatbot-webapp-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --settings \
    AZURE_SPEECH_KEY="$AZURE_SPEECH_KEY" \
    AZURE_SPEECH_REGION="$AZURE_SPEECH_REGION"

# Deploy updated code
az webapp up \
  --name rag-chatbot-webapp-[yourname] \
  --resource-group rg-foundry-chatbot-workshop
```

**Option C: Update Azure AI Foundry Endpoint**

```bash
# Update online deployment with new environment variables
az ml online-deployment update \
  --name rag-chatbot-deployment \
  --endpoint rag-chatbot-endpoint \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot \
  --set \
    environment_variables.AZURE_SPEECH_KEY="$AZURE_SPEECH_KEY" \
    environment_variables.AZURE_SPEECH_REGION="$AZURE_SPEECH_REGION"
```

#### 7.4 Test Production Deployment

```bash
# Get endpoint URL (if using Azure AI Foundry endpoint)
ENDPOINT_URL=$(az ml online-endpoint show \
  --name rag-chatbot-endpoint \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot \
  --query scoring_uri -o tsv)

# Test voice endpoint
curl -X POST $ENDPOINT_URL/api/voice/transcribe \
  -H "Authorization: Bearer $API_KEY" \
  -F "audio=@test_audio.wav"

# Or if using Web App
WEBAPP_URL="https://rag-chatbot-webapp-[yourname].azurewebsites.net"
curl -X POST $WEBAPP_URL/api/voice/transcribe \
  -F "audio=@test_audio.wav"
```

### Step 8: Best Practices for Voice Interfaces (15 minutes)

#### 8.1 Voice UI Design Principles

**1. Provide Clear Feedback:**
- Visual indicator when listening
- Confirmation of what was heard
- Progress indicator during processing

**2. Handle Errors Gracefully:**
```python
# Example error messages
ERROR_MESSAGES = {
    'no_speech': "I didn't hear anything. Please try again.",
    'unclear': "I didn't catch that. Could you repeat?",
    'no_match': "I'm not sure about that. Can you rephrase?",
    'service_error': "I'm having trouble hearing right now. Please try again."
}
```

**3. Set Expectations:**
- Tell users what they can say
- Provide example phrases
- Guide users when confused

**4. Keep Responses Concise:**
```python
def make_voice_friendly(text):
    """
    Adapt text response for voice output
    - Remove markdown
    - Shorten long responses
    - Make more conversational
    """
    # Remove markdown
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    
    # Limit length
    if len(text) > 500:
        text = text[:500] + "..."
    
    return text
```

#### 8.2 Privacy and Security

**Best Practices:**

1. **Inform Users:**
   - Display recording indicator
   - Explain data usage
   - Provide opt-out option

2. **Minimize Data Retention:**
   ```python
   # Don't store audio files
   # Process and delete immediately
   async def process_audio(audio_data):
       text = await transcribe(audio_data)
       # Delete audio_data
       del audio_data
       return text
   ```

3. **Secure Transmission:**
   - Use HTTPS for all API calls
   - Encrypt audio data in transit
   - Don't log sensitive content

#### 8.3 Performance Optimization

**Tips for Low Latency:**

1. **Stream Audio:**
   ```python
   # Use streaming recognition for real-time
   async def streaming_recognition():
       stream = await audio_stream()
       async for result in recognizer.recognize_continuous(stream):
           yield result.text
   ```

2. **Pre-generate Common Responses:**
   ```python
   # Cache TTS for frequent responses
   CACHED_AUDIO = {
       'hello': pregenerate_tts("Hello! How can I help?"),
       'thinking': pregenerate_tts("Let me think about that..."),
       'error': pregenerate_tts("Sorry, I encountered an error.")
   }
   ```

3. **Parallel Processing:**
   ```python
   # Process STT and prepare TTS simultaneously
   async def fast_voice_chat(audio):
       text_task = asyncio.create_task(transcribe(audio))
       
       text = await text_task
       response = await get_response(text)
       
       audio_task = asyncio.create_task(synthesize(response))
       return await audio_task
   ```

#### 8.4 Accessibility

Make voice interface accessible:

1. **Provide Alternative Inputs:**
   - Text input alongside voice
   - Keyboard shortcuts
   - Screen reader support

2. **Customize Voice Settings:**
   - Voice selection
   - Speaking rate adjustment
   - Volume control

3. **Visual Feedback:**
   - Captions for audio responses
   - Text transcript of conversation
   - Visual indicators for all states

### Step 9: Testing and Validation (15 minutes)

#### 9.1 Test Scenarios

Test various use cases:

- [ ] Clear speech in quiet environment
- [ ] Speech with background noise
- [ ] Accented speech
- [ ] Fast speech
- [ ] Slow speech
- [ ] Long questions
- [ ] Short questions
- [ ] Follow-up questions
- [ ] Interruptions
- [ ] Multiple speakers

#### 9.2 Quality Metrics

Monitor these metrics:

1. **Accuracy:**
   - Word Error Rate (WER)
   - Intent recognition accuracy
   - Response relevance

2. **Latency:**
   - STT latency: < 500ms
   - RAG processing: < 2s
   - TTS latency: < 1s
   - Total response time: < 4s

3. **User Experience:**
   - Successful interactions
   - User satisfaction
   - Error rate

#### 9.3 Run Test Suite

```bash
# Run unit tests
pytest tests/test_voice_handler.py -v

# Run integration tests
pytest tests/test_voice_integration.py -v

# Run performance tests
python scripts/test_voice_performance.py
```

### Step 10: Monitoring and Analytics (10 minutes)

#### 10.1 Log Important Events

```python
import logging

logger.info("Voice interaction started", extra={
    'session_id': session_id,
    'timestamp': datetime.now(),
    'user_agent': request.headers.get('user-agent')
})

logger.info("Speech recognized", extra={
    'text': transcribed_text,
    'confidence': result.confidence,
    'duration': audio_duration
})

logger.info("Response synthesized", extra={
    'response_length': len(response_text),
    'voice': voice_name,
    'audio_duration': audio_duration
})
```

#### 10.2 Track Metrics in Foundry

Configure monitoring dashboard:

**Key Metrics:**
- Voice interactions per day
- Average STT latency
- Average TTS latency
- Error rate by type
- Most common queries
- Language distribution

**Alerts:**
- STT latency > 2s
- TTS latency > 3s
- Error rate > 10%
- Service unavailable

## 🎓 Key Takeaways

Congratulations! You've learned:

- ✅ How to integrate Azure Speech Services
- ✅ Implementing speech-to-text and text-to-speech
- ✅ Building voice-enabled interfaces
- ✅ Best practices for voice UI design
- ✅ Deploying voice-enabled applications

## 🔍 Troubleshooting

### Common Issues

**Issue**: "Microphone permission denied"

**Solution**:
- Check browser settings
- Use HTTPS (required for microphone access)
- Try different browser
- Check system permissions

---

**Issue**: "Speech recognition fails"

**Solution**:
- Verify Azure Speech Service key and region
- Check audio format compatibility
- Ensure stable internet connection
- Test with different audio input

---

**Issue**: "Audio playback not working"

**Solution**:
- Check browser audio permissions
- Verify audio format is supported
- Test with different browser
- Check volume settings

---

**Issue**: "High latency in voice responses"

**Solution**:
- Use streaming recognition
- Optimize RAG retrieval
- Cache common responses
- Use faster voice models
- Check network latency

## 📚 Additional Resources

- [Azure Speech Service Documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [Voice User Interface Design](https://www.nngroup.com/articles/voice-first/)
- [SSML Reference](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup)

## ✅ Lab Completion Checklist

Before finishing, ensure you have:

- [ ] Azure Speech Service configured
- [ ] STT and TTS tested successfully
- [ ] Voice handler integrated with RAG chatbot
- [ ] Web interface working with voice
- [ ] Deployed voice-enabled chatbot to Foundry
- [ ] Tested end-to-end voice interactions
- [ ] Understand voice UI best practices

## 🎉 Congratulations!

You've successfully completed the workshop! You now have a fully functional, voice-enabled RAG chatbot deployed on Microsoft Azure AI Foundry.

**What's Next?**
- Experiment with different voices and languages
- Add custom wake word detection
- Implement conversation memory
- Add support for multi-turn dialogues
- Explore custom speech models
- Build mobile app with voice capabilities

## 🌟 Share Your Success

We'd love to hear about your experience! Share your project and what you learned.

---

**Questions or Feedback?** Check the [resources](../resources/README.md) folder or contact your instructor.
