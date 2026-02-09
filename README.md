# Introduction Workshop to Microsoft Foundry: Building an Intelligent RAG Chatbot with Voice Capabilities

## 🎯 Workshop Overview

Welcome to this hands-on workshop where you'll learn to build an intelligent chatbot with Retrieval-Augmented Generation (RAG) capabilities using Microsoft Foundry and add real-time voice conversations using GPT Realtime. This workshop is designed to be educational and provides insights into modern AI application development using Microsoft's AI platform.

### What You'll Build

By the end of this workshop, you will have:
1. **Lab 1**: A fully functional RAG chatbot that answers questions using your custom knowledge base, powered by Foundry IQ and Azure AI Search, deployed as a web application
2. **Lab 2**: Voice-enabled conversations with your chatbot using GPT Realtime (speech-to-speech)

### Learning Objectives

- Understand the RAG (Retrieval-Augmented Generation) architecture
- Set up a knowledge base using Azure AI Search and Azure Blob Storage
- Learn to use Foundry IQ for knowledge base management with agentic retrieval
- Create an AI agent in Microsoft Foundry
- Deploy your agent as a web app using the Foundry Agent Web App template
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
- **Azure subscription** 
- **Microsoft Foundry access** 

## 🗂️ Workshop Structure

This workshop is divided into two progressive labs, each with multiple sub-labs offering **Portal** and **Code** paths:

### [Lab 1: Building a RAG-Enabled Chatbot](./lab-1-rag-chatbot/README.md)
**Duration**: 75-105 minutes

| Sub-Lab | Description | Time | Portal | Code |
|---------|-------------|------|:------:|:----:|
| 1.1 Set Up Azure Resources | Create Foundry project, deploy models | 15-20 min | ✅ | ✅ |
| 1.2 Prepare Knowledge Base | Upload documents to Azure Blob Storage | 10-15 min | ✅ | ✅ |
| 1.3 Create Vector Index | Set up Azure AI Search with embeddings | 15-20 min | ✅ | ✅ |
| 1.4 Create Your Agent | Build agent with Foundry IQ | 15-20 min | ✅ | ✅ |
| 1.5 Host Agent as Web App | Deploy using Foundry Agent Web App | 20-30 min | ❌ | ✅ |

### [Lab 2: Adding Voice Capabilities](./lab-2-voice-capabilities/README.md)
**Duration**: 25-35 minutes

| Sub-Lab | Description | Time | Portal | Code |
|---------|-------------|------|:------:|:----:|
| 2.1 Deploy GPT Realtime Model | Deploy the realtime voice model | 10-15 min | ✅ | ✅ |
| 2.2 Add Voice to Your Agent | Integrate voice using GPT Realtime API | 15-20 min | ❌ | ✅ |

##  Additional Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-foundry)
- [Understanding RAG](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)
- [GPT Realtime API](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/realtime-audio-quickstart)


## 📄 License

This workshop content is provided for educational purposes.

---

**Ready to begin?** Head over to [Lab 1](./lab-1-rag-chatbot/README.md) to get started!
