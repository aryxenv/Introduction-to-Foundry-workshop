# Introduction Workshop to Microsoft Foundry: Building an Intelligent RAG Chatbot with Voice Capabilities

## 🎯 Workshop Overview

Welcome to this hands-on workshop where you'll learn to build an intelligent chatbot with Retrieval-Augmented Generation (RAG) capabilities using Microsoft Foundry and add real-time voice conversations using GPT Realtime. This workshop is designed to be educational and provides insights into modern AI application development using Microsoft's AI platform.

### What You'll Build

By the end of this workshop, you will have:
1. **Lab 1**: A fully functional RAG chatbot that answers questions using your custom knowledge base, powered by Foundry IQ and Azure AI Search
2. **Lab 2**: Voice-enabled conversations with your chatbot using GPT Realtime (speech-to-speech)

### Learning Objectives

- Understand the RAG (Retrieval-Augmented Generation) architecture
- Set up a knowledge base using Azure AI Search and Azure Blob Storage
- Learn to use Foundry IQ for knowledge base management with agentic retrieval
- Create an AI agent in Microsoft Foundry
- Add real-time voice capabilities using GPT Realtime

## 📋 Prerequisites

### Required Knowledge
- Basic understanding of Python programming
- Familiarity with REST APIs
- Basic understanding of cloud services
- Understanding of basic AI/ML concepts 

### Required Tools
- **Python 3.9+** installed on your machine
- **Visual Studio Code** or another code editor
- **Git** for version control
- **Azure subscription** (free tier available)
- **Microsoft Foundry access** (your instructor will provide details)

### Required Accounts
- Microsoft Azure account (sign up for free at https://azure.microsoft.com/free/ or in case of an event, ask your Microsoft representative for account access)
- Access to Microsoft Foundry (included with Azure subscription)

## 🗂️ Workshop Structure

This workshop is divided into two progressive labs, each with multiple sub-labs offering **Console** (portal) and **Code** (Python) paths:

### [Lab 1: Building a RAG-Enabled Chatbot](./lab-1-rag-chatbot/README.md)
**Duration**: 55-75 minutes

| Sub-Lab | Description | Time |
|---------|-------------|------|
| 1.1 Set Up Azure Resources | Create Foundry project, deploy models | 15-20 min |
| 1.2 Prepare Knowledge Base | Upload documents to Azure Blob Storage | 10-15 min |
| 1.3 Create Vector Index | Set up Azure AI Search with embeddings | 15-20 min |
| 1.4 Create Your Agent | Build agent with Foundry IQ | 15-20 min |

### [Lab 2: Adding Voice Capabilities](./lab-2-voice-capabilities/README.md)
**Duration**: 30-45 minutes

| Sub-Lab | Description | Time |
|---------|-------------|------|
| 2.1 Deploy GPT Realtime Model | Deploy the realtime voice model | 10-15 min |
| 2.2 Add Voice to Your Agent | Enable voice on your RAG agent | 15-20 min |

## 🚀 Getting Started

Choose one of the following options:

### Option A: GitHub Codespaces (Fastest)

If available in your org/account - no local setup needed:
1. Click the green "Code" button on this GitHub repo
2. Select "Codespaces" → "Create codespace on main"
3. Wait 2-3 minutes - everything is pre-installed!
4. Start with [Lab 1](./lab-1-rag-chatbot/README.md)

### Option B: VS Code Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/LauraVerghote/Introduction-to-Foundry-workshop.git
   cd Introduction-to-Foundry-workshop
   ```
2. Follow the [Setup Guide](./SETUP.md)
3. Start with [Lab 1](./lab-1-rag-chatbot/README.md)


## 📚 Additional Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-foundry)
- [Understanding RAG](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)
- [GPT Realtime API](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/realtime-audio-quickstart)


## 📄 License

This workshop content is provided for educational purposes.

---

**Ready to begin?** Head over to [Lab 1](./lab-1-rag-chatbot/README.md) to get started!
