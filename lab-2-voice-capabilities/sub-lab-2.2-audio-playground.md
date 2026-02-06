# Sub-Lab 2.2: Test in Audio Playground

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) | [Next: Sub-Lab 2.3 →](./sub-lab-2.3-voice-web-app.md)

---

**⏱️ Estimated Time**: 10-15 minutes

## Overview

In this sub-lab, you'll test your GPT Realtime model using the Audio Playground in Microsoft Foundry. This is the fastest way to experience voice conversations without writing any code.

---

## 🎓 Key Concepts

### What is the Audio Playground?

The Audio Playground is a built-in tool in Foundry that lets you:
- **Test voice interactions** with your deployed realtime model
- **Configure voice settings** like voice selection and speaking style
- **Adjust audio parameters** like silence detection and response threshold
- **Provide instructions** to customize the model's behavior

### Audio Settings

| Setting | Description |
|---------|-------------|
| **Voice** | The voice used for responses (alloy, echo, shimmer, etc.) |
| **Threshold** | Audio level to trigger speech detection |
| **Prefix padding** | Silence before speech starts |
| **Silence duration** | How long to wait before ending input |

---

## 🖥️ Option: Console

<details>
<summary><strong>Click to expand Console instructions</strong></summary>

### 1. Navigate to Audio Playground

1. Go to [Microsoft Foundry](https://ai.azure.com)
2. Select your project (`my-first-chatbot`)
3. In the left menu, click **Playgrounds**
4. Select **Audio playground** → **Try the Audio playground**

   <img src="images/audio-playground-1.png" width="800"/>

> ⚠️ **Note**: The Chat playground doesn't support `gpt-realtime`. You must use the Audio playground.

### 2. Select Your Model

1. In the **Deployment** dropdown, select your `gpt-realtime` deployment
2. If you don't see it, verify the model is deployed (Sub-Lab 2.1)

   <img src="images/audio-playground-2.png" width="600"/>

### 3. Configure Instructions

1. In the **Give the model instructions and context** text box, enter:

   ```
   You are a helpful customer service assistant for TechCorp.
   
   You have access to knowledge about TechCorp's products, policies, and services.
   
   Key information:
   - TechCorp offers SmartAssist, DataVision, and CloudSync products
   - Return policy: 30 days for unopened items
   - Standard shipping is free, express is $9.99
   - Support hours: Monday-Friday 9 AM - 6 PM
   
   Keep responses concise and conversational since this is a voice interface.
   If you don't know something, say so honestly.
   ```

   <img src="images/audio-playground-3.png" width="600"/>

### 4. Configure Voice Settings

1. Expand **Voice configuration** (if available)
2. Select a voice: **alloy** (neutral) or **coral** (friendly)
3. Adjust settings if needed:
   - **Threshold**: 30 (default)
   - **Prefix padding**: 200ms
   - **Silence duration**: 500ms

### 5. Start Voice Conversation

1. Click **Start listening**
2. When prompted, **Allow** microphone access in your browser
3. The playground will show "Listening..." when ready

   <img src="images/audio-playground-4.png" width="800"/>

### 6. Test Voice Interactions

Try these questions by speaking naturally:

**Test 1: Product Information**
> "What products does TechCorp offer?"

**Test 2: Policy Question**
> "What's your return policy?"

**Test 3: Follow-up Question**
> "And what about shipping costs?"

**Test 4: Interruption Test**
> Start asking a question, then interrupt mid-response to test natural conversation flow

### 7. Observe the Behavior

Notice how the model:
- ✅ Responds with natural-sounding voice
- ✅ Allows you to interrupt mid-response
- ✅ Maintains context across the conversation
- ✅ Keeps responses concise for voice

### 8. Stop the Session

Click **Stop listening** to end the voice session.

### ✅ Console Checkpoint

You should now have:
- [ ] Successfully started Audio Playground
- [ ] Model responding to voice input
- [ ] Tested multiple voice interactions
- [ ] Experienced natural conversation flow

</details>

---

## 💡 Tips for Voice Interactions

### Keep Instructions Voice-Friendly

❌ **Bad for voice:**
> "Here's a detailed breakdown of our product lineup: 1. SmartAssist - This is our flagship AI customer service platform that provides..."

✅ **Good for voice:**
> "We have three main products: SmartAssist for customer service, DataVision for analytics, and CloudSync for cloud management. Want details on any of these?"

### Handle Silence Gracefully

If the model seems to cut off early or wait too long, adjust:
- **Silence duration**: Increase if it stops listening too quickly
- **Threshold**: Lower if it's not detecting quiet speech

### Test Different Voices

Each voice has a different personality:
- **alloy** - Professional, neutral
- **coral** - Warm, friendly
- **echo** - Calm, soothing
- **shimmer** - Clear, articulate

---

## 🔗 Connect to Your RAG Agent (Advanced)

To use your knowledge base from Lab 1 with voice:

1. In the instructions, reference your Foundry IQ knowledge base
2. Or use the Agent playground and enable voice (if available)
3. For full integration, proceed to Sub-Lab 2.3 (Code path)

---

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.1](./sub-lab-2.1-deploy-realtime-model.md) | [Next: Sub-Lab 2.3 →](./sub-lab-2.3-voice-web-app.md)
