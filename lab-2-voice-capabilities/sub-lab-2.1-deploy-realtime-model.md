# Sub-Lab 2.1: Deploy GPT Realtime Model

[← Back to Lab 2 Overview](./README.md) | [Next: Sub-Lab 2.2 →](./sub-lab-2.2-add-voice-to-agent.md)

---

**⏱️ Estimated Time**: 10-15 minutes

## Overview

In this sub-lab, you'll deploy the GPT Realtime model in Microsoft Foundry. This model enables real-time voice conversations with low latency - users speak directly to the model and receive audio responses.

---

## 🎓 Key Concepts

### What is GPT Realtime?

GPT Realtime is a speech-to-speech (S2S) model that went **Generally Available in August 2025**. Unlike traditional voice assistants that chain separate Speech-to-Text, LLM, and Text-to-Speech services together, GPT Realtime handles everything in a single model.

| Traditional Approach | GPT Realtime |
|---------------------|--------------|
| STT → LLM → TTS (3 separate steps) | Single model handles everything |
| Higher latency (cumulative delays) | Low latency (~200-500ms) |
| No interruption handling | Natural interruptions supported |
| Separate voice configuration | Integrated voice selection |

### Key Features

- **Natural Voices**: Multiple voice options including Alloy, Ash, Coral, Echo, Sage, and Shimmer
- **Instruction Following**: Ability to follow tone, pacing, and language instructions in the system prompt
- **High Audio Quality**: Clear, glitch-free output with accurate alphanumeric reproduction
- **Image Input Support**: Add images to context and discuss them via voice
- **Function Calling**: Call custom code during conversations, with async function calling support
- **Natural Turn-Taking**: Real-world conversation flow with automatic voice activity detection (VAD)

### Model Variants

| Model | Best For | Notes |
|-------|----------|-------|
| `gpt-realtime` | Production voice applications | Full-featured GA model |
| `gpt-mini-realtime` | Cost-effective, faster responses | Feature parity with full model |
| `gpt-realtime-preview` | Testing preview features | Use GA models for production |

### Pricing

GPT Realtime is priced based on tokens per million:
- Text input/output tokens
- Audio input/output tokens (audio is tokenized)

> 💡 For this workshop, usage will be minimal and well within free tier or trial credits.

---

## 🖥️ Option: Portal

<details>
<summary><strong>Click to expand Portal instructions</strong></summary>

### 1. Navigate to Foundry Portal

1. Go to [Microsoft Foundry](https://ai.azure.com)
2. Select your project (`my-first-chatbot`)

### 2. Deploy GPT Realtime Model

1. In the top menu go to "Discover"
2. Click "Models" on the left
3. Search for `gpt-realtime` and click on it

   <img src="images/foundry-models-1.png" width="800"/>

4. Click Deploy -> Custom settings
    - Deployment name: `gpt-realtime`
    - Deployment type: Global Standard
    - Tokens per Minute Rate Limit: choose the minimum (=10 000)
5. Pick your project. Click "Deploy"


### 3. Verify Deployment

1. Wait for deployment to complete (1-2 minutes)
2. Once deployed, you'll see it in your model deployments list under Build -> Models
3. Note the deployment name - you'll need it for the Audio Playground

   <img src="images/foundry-models-2.png" width="800"/>

### ✅ Portal Checkpoint

You should now have:
- [ ] GPT Realtime model deployed in your Foundry project
- [ ] Deployment name noted for next steps

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

> 📝 **First time using the Code option?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.

### 1. Verify Prerequisites

Ensure you're logged into Azure and have the Foundry resource from Lab 1.

> ✏️ **Replace `[yourname]`** with your actual name (same as Lab 1.1) in all commands below.

```powershell
# Check Azure CLI is installed
az --version

# Login to Azure (if not already)
az login

# Verify your Foundry resource exists
az cognitiveservices account show `
  --name foundry-workshop-[yourname] `
  --resource-group rg-foundry-workshop-[yourname] `
  --query "name" -o tsv
```

**Expected Output:**
```
foundry-workshop-[yourname]
```

If you see an error like "ResourceNotFound", double-check your resource name from Lab 1.1.

### 2. Deploy GPT Realtime Model

> ✏️ **Replace `[yourname]`** with your actual name (same as Lab 1.1).

```powershell
# Deploy GPT Realtime model
az cognitiveservices account deployment create `
  --name foundry-workshop-[yourname] `
  --resource-group rg-foundry-workshop-[yourname] `
  --deployment-name gpt-realtime `
  --model-name gpt-realtime `
  --model-version "2025-08-28" `
  --model-format OpenAI `
  --sku-capacity 1 `
  --sku-name GlobalStandard
```

> 💡 **Note**: The GPT Realtime model uses `GlobalStandard` SKU which provides global availability. Capacity of 1 is sufficient for workshop purposes.

### 3. Verify Deployment

> ✏️ **Replace `[yourname]`** with your actual name (same as Lab 1.1).

```powershell
# Verify the deployment was created
az cognitiveservices account deployment show `
  --name foundry-workshop-[yourname] `
  --resource-group rg-foundry-workshop-[yourname] `
  --deployment-name gpt-realtime `
  --query "{Name:name, Model:properties.model.name, Status:properties.provisioningState}" `
  -o table
```

**Expected Output:**
```
Name          Model            Status
------------  ---------------  -----------
gpt-realtime  gpt-realtime     Succeeded
```

You can also list all deployments to see the complete picture:

> ✏️ **Replace `[yourname]`** with your actual name (same as Lab 1.1).

```powershell
# List all deployments
az cognitiveservices account deployment list `
  --name foundry-workshop-[yourname] `
  --resource-group rg-foundry-workshop-[yourname] `
  --query "[].{Name:name, Model:properties.model.name, Status:properties.provisioningState}" `
  -o table
```

**Expected Output:**
```
Name                     Model                   Status
-----------------------  ----------------------  -----------
gpt-4.1-mini             gpt-4.1-mini            Succeeded
text-embedding-3-small   text-embedding-3-small  Succeeded
gpt-realtime             gpt-realtime            Succeeded
```

### 4. Note the Deployment Name

Your deployment name is `gpt-realtime`. You'll use this in the Audio Playground to test your deployment.

### ✅ Code Checkpoint

You should now have:
- [ ] GPT Realtime model deployed via CLI
- [ ] Deployment verified with `Succeeded` status
- [ ] Deployment name noted for next steps

</details>

---

[← Back to Lab 2 Overview](./README.md) | [Next: Sub-Lab 2.2 →](./sub-lab-2.2-add-voice-to-agent.md)
