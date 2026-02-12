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

> ✏️ **Replace [yourname]** with your actual name or identifier (e.g., `jsmith`) throughout these instructions. This ensures your resources are uniquely named.

### 1. Create a Resource Group

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Resource groups" → "Create"

   <img src="images/resource-group-console-1.png" width="800"/>
   <img src="images/resource-group-console-2.png" width="800"/>

3. Configure:
   - **Name**: `rg-foundry-workshop-[yourname]`
   - **Region**: East US 2
4. Click "Review + Create" → "Create"

   <img src="images/resource-group-console-3.png" width="500"/>

### 2. Create Microsoft Foundry Resource

1. Search for "Microsoft Foundry" in the Azure Portal
2. Click "Create"

   <img src="images/foundry-resource-1.png" width="500"/>

3. Configure:
   - **Resource group**: `rg-foundry-workshop-[yourname]`
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
- [ ] Resource group: `rg-foundry-workshop-[yourname]`
- [ ] Foundry resource with project: `my-first-chatbot`
- [ ] Deployed models: `gpt-4o` and `text-embedding-3-small`

</details>

---

## 💻 Option: Code 

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

### 1. Complete Development Environment Setup

Before proceeding, complete the development environment setup:

👉 **[Complete the Setup Guide](../SETUP.md)** - Choose either GitHub Codespaces or VS Code Local Setup

### 2. Verify Prerequisites

Once your environment is ready. Go to the main folder and verify you have (make sure to use the git bash terminal):

```bash
# Check Azure CLI is installed
az --version

# Login to Azure
az login
```

### 3. Create Resources via CLI
Copy the instructions below in a text editor, fill in the placeholders and execute in your Git Bash terminal

```bash
# Create resource group
az group create \
  --name rg-foundry-workshop-[yourname] \
  --location eastus2

# Create Foundry resource (with project management enabled)
az cognitiveservices account create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --kind AIServices \
  --sku s0 \
  --location eastus2 \
  --allow-project-management

# Create custom subdomain (must be globally unique)
az cognitiveservices account update \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --custom-domain foundry-workshop-[yourname]

# Create project within the Foundry resource
az cognitiveservices account project create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --project-name my-first-chatbot \
  --location eastus2
```

### 4. Deploy Models via CLI

> ✏️ Copy the code below into a text editor, **replace `[yourname]`** with your actual name, then run the commands.

```bash
# Deploy GPT-4o
az cognitiveservices account deployment create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version "2024-11-20" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# Deploy embedding model
az cognitiveservices account deployment create \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --deployment-name text-embedding-3-small \
  --model-name text-embedding-3-small \
  --model-version "1" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# Verify deployments
az cognitiveservices account deployment show \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --deployment-name gpt-4o

az cognitiveservices account deployment show \
  --name foundry-workshop-[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --deployment-name text-embedding-3-small
```

### 5. Configure Environment Variables

If you haven't done so yet during the initial set-up: Create a `.env` file in the `lab-1-rag-chatbot` directory:

```bash
cp .env.example .env
```

Get your endpoint (found in Foundry Portal on the project welcome screen, or construct it):

```
https://foundry-workshop-[yourname].cognitiveservices.azure.com/
```

Edit `.env` with your endpoint:

```properties
# Foundry Configuration (using Azure Identity - no API key needed)
AZURE_OPENAI_ENDPOINT=https://foundry-workshop-[yourname].cognitiveservices.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search Configuration (will be added in Sub-Lab 1.3)
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_INDEX_NAME=chatbot-knowledge-base

# Azure Storage Configuration (will be added in Sub-Lab 1.2)
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_CONTAINER_NAME=knowledge-base-container
```

> 💡 **Note**: We're using Azure Identity (DefaultAzureCredential) for authentication instead of API keys. This is more secure and uses your `az login` credentials automatically.

> ⚠️ **Important**: Never commit `.env` file to version control!

### ✅ Code Checkpoint

You should now have:
- [ ] Resource group created
- [ ] Foundry resource with project: `my-first-chatbot`
- [ ] Models deployed: `gpt-4o` and `text-embedding-3-small`
- [ ] `.env` file configured with Foundry credentials

</details>

---

[← Back to Lab 1 Overview](./README.md) | [Next: Sub-Lab 1.2 →](./sub-lab-1.2-prepare-knowledge-base.md)
