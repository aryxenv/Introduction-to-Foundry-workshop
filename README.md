# Introduction Workshop to Microsoft Foundry and Micrsoft Agent Framework: Building an Intelligent RAG Chatbot with voice capabilities

## 🎯 Workshop Overview

Welcome to this hands-on workshop where you'll learn to build an intelligent chatbot with Retrieval-Augmented Generation (RAG) capabilities using the Microsoft Agent Framework and deploy it on Microsoft Foundry. This workshop is designed to be educational and provides insights into modern AI application development using the newest Microsoft AI technologies

### What You'll Build

By the end of this workshop, you will have:
1. **Lab 1**: A fully functional chatbot with RAG capabilities that can answer questions using your custom knowledge base
2. **Lab 2**: Voice-enabled chatbot that supports speech-to-text input and text-to-speech output

### Learning Objectives

- Understand the architecture of our Retrieval-Augmented Generation (RAG) part on Azure
- Set up a knowledge base using Azure AI Search that will be used by our chatbot
- Learn to use the Microsoft Agent Framework for building conversational AI
- Deploy and host AI applications on Microsoft Foundry
- Implement voice capabilities using Azure Speech Services

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

This workshop is divided into two progressive labs:

### [Lab 1: Building a RAG-Enabled Chatbot](./lab-1-rag-chatbot/README.md)
**Duration**: 40 minutes

In this lab, you will:
- Set up your Azure AI Foundry environment
- Understand RAG architecture and its benefits
- Build a knowledge base using Azure AI Search
- Create a chatbot using Microsoft Agent Framework (Semantic Kernel)
- Deploy your chatbot to Azure AI Foundry
- Test and validate your implementation

### [Lab 2: Adding Voice Capabilities](./lab-2-voice-capabilities/README.md)
**Duration**: 20 minutes

In this lab, you will:
- Integrate Azure Speech Services
- Add speech-to-text (STT) functionality
- Add text-to-speech (TTS) functionality
- Create a voice-enabled interface
- Deploy the enhanced chatbot

## 🚀 Getting Started

### Option 1: GitHub Codespaces (Recommended - Fastest Setup) ⚡

GitHub Codespaces provides a pre-configured cloud development environment with everything installed. If you have this available in your org/account this will be the fastest way.

**Steps:**
1. Click the green "Code" button on the GitHub repository
2. Select "Codespaces" tab
3. Click "Create codespace on main"
4. Wait for the environment to build (2-3 minutes)
5. Everything is pre-installed and ready to go! 🎉

**What's included:**
- ✅ Python 3.10
- ✅ All dependencies installed
- ✅ Azure CLI with ML extension
- ✅ VS Code extensions
- ✅ Docker support

**Next steps after Codespace loads:**
1. Run `az login` to authenticate with Azure
2. Configure your `.env` files with Azure credentials
3. Start with [Lab 1](./lab-1-rag-chatbot/README.md)

---

### Option 2: Local Development with VS Code

For local development on your machine, follow our comprehensive setup guide.

**Prerequisites:**
- Visual Studio Code
- Python 3.10 or 3.11
- Git
- Azure CLI

📖 **[Complete VS Code Setup Guide →](./SETUP.md)**

The setup guide includes:
- Step-by-step installation instructions for all platforms (Windows, macOS, Linux)
- Required VS Code extensions
- Environment configuration
- Troubleshooting common issues
- Verification scripts

**Quick Start:**
```bash
# Clone repository
git clone https://github.com/LauraVerghote/Introduction-to-Foundry-workshop.git
cd Introduction-to-Foundry-workshop

# Follow the setup guide
cat SETUP.md
```

---

### Option 3: Manual Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/LauraVerghote/Introduction-to-Foundry-workshop.git
   cd Introduction-to-Foundry-workshop
   ```

2. **Install prerequisites:**
   - Python 3.10+
   - Azure CLI
   - Git

3. **Set up Lab 1:**
   ```bash
   cd lab-1-rag-chatbot
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

4. **Follow the labs in order**
   - Start with [Lab 1](./lab-1-rag-chatbot/README.md)
   - Then proceed to [Lab 2](./lab-2-voice-capabilities/README.md)

---

**💡 Tip:** We recommend Codespaces for workshop environments or if you want to get started quickly. Use local setup if you prefer working on your own machine or need offline access.

## 📚 Additional Resources

- [Microsoft Foundry Documentation]([https://learn.microsoft.com/en-us/azure/ai-foundry/](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-foundry?view=foundry))
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Understanding RAG](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)
- [Azure Speech Services](https://azure.microsoft.com/en-us/products/ai-services/speech-to-text)


## 📄 License

This workshop content is provided for educational purposes.

---

**Ready to begin?** Head over to [Lab 1](./lab-1-rag-chatbot/README.md) to get started!
