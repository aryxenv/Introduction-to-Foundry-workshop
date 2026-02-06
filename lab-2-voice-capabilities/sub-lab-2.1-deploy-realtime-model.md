# Sub-Lab 2.1: Deploy GPT Realtime Model

[← Back to Lab 2 Overview](./README.md) | [Next: Sub-Lab 2.2 →](./sub-lab-2.2-audio-playground.md)

---

**⏱️ Estimated Time**: 10-15 minutes

## Overview

In this sub-lab, you'll deploy the GPT Realtime model in Microsoft Foundry. This model enables real-time voice conversations with low latency - users speak directly to the model and receive audio responses.

---

## 🎓 Key Concepts

### What is GPT Realtime?

GPT Realtime is different from traditional voice assistants:

| Traditional Approach | GPT Realtime |
|---------------------|--------------|
| STT → LLM → TTS (3 separate steps) | Single model handles everything |
| Higher latency (cumulative delays) | Low latency (~200-500ms) |
| No interruption handling | Natural interruptions supported |
| Separate voice configuration | Integrated voice selection |

### Model Variants

| Model | Best For |
|-------|----------|
| `gpt-realtime` | Production voice applications |
| `gpt-realtime-mini` | Cost-effective, faster responses |
| `gpt-4o-realtime-preview` | Testing latest preview features |

---

## 🖥️ Option: Console

<details>
<summary><strong>Click to expand Console instructions</strong></summary>

### 1. Navigate to Foundry Portal

1. Go to [Microsoft Foundry](https://ai.azure.com)
2. Select your project (`my-first-chatbot`)

### 2. Deploy GPT Realtime Model

1. In the left menu:
   - For **Foundry resource**: Select **Models + endpoints** under "My assets"
   - For **Azure OpenAI resource**: Select **Deployments** under "Shared resources"

2. Click **+ Deploy model** → **Deploy base model**

   <img src="images/deploy-realtime-1.png" width="800"/>

3. Search for `gpt-realtime` in the model catalog

4. Select the model and click **Confirm**

   <img src="images/deploy-realtime-2.png" width="600"/>

5. Review deployment details:
   - **Deployment name**: `gpt-realtime` (or keep default)
   - **Deployment type**: Global Standard
   
6. Click **Deploy**

### 3. Verify Deployment

1. Wait for deployment to complete (1-2 minutes)
2. Once deployed, you'll see it in your model deployments list
3. Note the deployment name - you'll need it for the Audio Playground

   <img src="images/deploy-realtime-3.png" width="800"/>

### ✅ Console Checkpoint

You should now have:
- [ ] GPT Realtime model deployed in your Foundry project
- [ ] Deployment name noted for next steps

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

### 1. Deploy via Azure CLI

```bash
# Login to Azure (if not already)
az login

# Deploy GPT Realtime model
az cognitiveservices account deployment create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --deployment-name gpt-realtime \
  --model-name gpt-realtime \
  --model-version "2025-08-28" \
  --model-format OpenAI \
  --sku-capacity 1 \
  --sku-name GlobalStandard
```

### 2. Verify Deployment

```bash
# List deployments
az cognitiveservices account deployment list \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --output table
```

**Expected Output:**
```
Name          Model              Version      ProvisioningState
------------  -----------------  -----------  ------------------
gpt-4o        gpt-4o             2024-05-13   Succeeded
gpt-realtime  gpt-realtime       2025-08-28   Succeeded
...
```

### 3. Update Environment Variables

Add to your `.env` file:

```properties
# GPT Realtime Configuration
AZURE_OPENAI_REALTIME_DEPLOYMENT=gpt-realtime
AZURE_OPENAI_REALTIME_VOICE=alloy
```

### ✅ Code Checkpoint

You should now have:
- [ ] GPT Realtime model deployed via CLI
- [ ] Deployment verified in the list
- [ ] `.env` updated with realtime configuration

</details>

---

[← Back to Lab 2 Overview](./README.md) | [Next: Sub-Lab 2.2 →](./sub-lab-2.2-audio-playground.md)
