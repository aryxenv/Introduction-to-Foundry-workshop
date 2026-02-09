# Sub-Lab 1.1: Set Up Azure Resources

[← Back to Lab 1 Overview](./README.md) | [Next: Sub-Lab 1.2 →](./sub-lab-1.2-prepare-knowledge-base.md)

---

**⏱️ Estimated Time**: 15-20 minutes

## Overview

In this sub-lab, you'll set up Microsoft Foundry and deploy the AI models that power your chatbot:
- **GPT-4o** – generates responses to user questions
- **text-embedding-3-small** – converts text into vectors for semantic search

---

## 🎓 Key Concepts

### What is Microsoft Foundry?

Microsoft Foundry is a unified AI platform that provides:
- **Project Management**: Organize your AI resources and deployments
- **Model Catalog**: Access to GPT, embedding, and other AI models
- **Development Tools**: Build, test, and deploy AI applications
- **Monitoring**: Track usage, costs, and performance

### What are Model Deployments?

A deployment is an instance of a model that you can call via API:
- **GPT-4o**: For generating natural language responses
- **text-embedding-3-small**: For converting text to vectors (embeddings)

---

## Resources You'll Create

- **Resource Group**: Container for all your Azure resources
- **Microsoft Foundry**: AI platform hub and project
- **Models in Microsoft Foundry**: GPT-4o (chat) and text-embedding-3-small (embeddings)

---

## 🖥️ Option: Portal

<details>
<summary><strong>Click to expand Portal instructions</strong></summary>

### 1. Create a Resource Group

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Resource groups" → "Create"

   <img src="images/resource-group-console-1.png" width="800"/>
   <img src="images/resource-group-console-2.png" width="800"/>

3. Configure:
   - **Name**: `rg-foundry-chatbot-workshop`
   - **Region**: East US 2
4. Click "Review + Create" → "Create"

   <img src="images/resource-group-console-3.png" width="500"/>

### 2. Create Microsoft Foundry Resource

1. Search for "Microsoft Foundry" in the Azure Portal
2. Click "Create"

   <img src="images/foundry-resource-1.png" width="500"/>

3. Configure:
   - **Resource group**: `rg-foundry-chatbot-workshop`
   - **Name**: `foundry-workshop-[yourname]`
   - **Region**: East US 2
   - **Default project name**: `my-first-chatbot`
4. Click "Review + Create" → "Create"

   <img src="images/foundry-resource-2.png" width="500"/>

### 3. Deploy AI Models

1. Go to your Foundry resource → Click "Go to Foundry portal"
2. Toggle "New Foundry" experience if prompted

   <img src="images/new-foundry.png" width="800"/>

3. Select your project (`my-first-chatbot`) → "Let's go"

   <img src="images/select-project.png" width="500"/>

4. **Deploy GPT-4o**:
   - Go to Discovery → Models
   - Search for `gpt-4o`
   - Click the model → Deploy → "Default settings"

   <img src="images/foundry-models-1.png" width="800"/>
   <img src="images/foundry-models-2.png" width="800"/>

5. **Deploy Embedding Model**:
   - Repeat for `text-embedding-3-small`
   - Discovery → Models → Search → Deploy → "Default settings"

### ✅ Portal Checkpoint

You should now have:
- [ ] Resource group: `rg-foundry-chatbot-workshop`
- [ ] Foundry resource with project: `my-first-chatbot`
- [ ] Deployed models: `gpt-4o` and `text-embedding-3-small`

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

> 📝 **First time using Code path?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.

### Prerequisites

- Azure CLI installed (`az --version`)
- Logged in to Azure (`az login`)

### 1. Create Resources via CLI

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name rg-foundry-chatbot-workshop \
  --location eastus2

# Create Foundry resource
az cognitiveservices account create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --kind OpenAI \
  --sku S0 \
  --location eastus2
```

### 2. Deploy Models via CLI

```bash
# Deploy GPT-4o
az cognitiveservices account deployment create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version "2024-05-13" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# Deploy embedding model
az cognitiveservices account deployment create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --deployment-name text-embedding-3-small \
  --model-name text-embedding-3-small \
  --model-version "1" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard
```

### 3. Configure Environment Variables

Create a `.env` file in the `lab-1-rag-chatbot` directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```properties
# Foundry Configuration
AZURE_OPENAI_ENDPOINT=https://foundry-workshop-[yourname].openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search Configuration (will be added in Sub-Lab 1.3)
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_INDEX_NAME=chatbot-knowledge-base

# Azure Storage Configuration (will be added in Sub-Lab 1.2)
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_CONTAINER_NAME=knowledge-base-container
```

> ⚠️ **Important**: Never commit `.env` file to version control!

### ✅ Code Checkpoint

You should now have:
- [ ] Resource group created
- [ ] Foundry resource with deployed models
- [ ] `.env` file configured with Foundry credentials

</details>

---

[← Back to Lab 1 Overview](./README.md) | [Next: Sub-Lab 1.2 →](./sub-lab-1.2-prepare-knowledge-base.md)
