# Introduction to Azure AI Foundry Workshop: Building an Intelligent Chatbot

## 🎯 Workshop Overview

Welcome to this hands-on workshop where you'll learn to build an intelligent chatbot with Retrieval-Augmented Generation (RAG) capabilities using the Microsoft Agent Framework and deploy it on Microsoft Azure AI Foundry. This workshop is designed to be educational and provides deep insights into modern AI application development on Azure's unified AI platform.

### What You'll Build

By the end of this workshop, you will have:
1. **Lab 1**: A fully functional chatbot with RAG capabilities that can answer questions using your custom knowledge base
2. **Lab 2**: Voice-enabled chatbot that supports speech-to-text input and text-to-speech output

### Learning Objectives

- Understand the fundamentals of Retrieval-Augmented Generation (RAG)
- Learn to use the Microsoft Agent Framework for building conversational AI
- Deploy and host AI applications on Microsoft Azure AI Foundry
- Implement voice capabilities using Azure Speech Services
- Work with Azure AI services in an integrated environment
- Apply best practices for building production-ready AI applications

## 📋 Prerequisites

### Required Knowledge
- Basic understanding of Python programming
- Familiarity with REST APIs
- Basic understanding of cloud services
- Understanding of basic AI/ML concepts (helpful but not required)

### Required Tools
- **Python 3.9+** installed on your machine
- **Visual Studio Code** or another code editor
- **Git** for version control
- **Azure subscription** (free tier available)
- **Palantir Foundry access** (your instructor will provide details)
- **Postman** or similar API testing tool (optional but recommended)

### Required Accounts
- Microsoft Azure account (sign up for free at https://azure.microsoft.com/free/)
- Access to Azure AI Foundry (included with Azure subscription)
- Azure OpenAI Service access (request at https://aka.ms/oai/access)

## 🗂️ Workshop Structure

This workshop is divided into two progressive labs:

### [Lab 1: Building a RAG-Enabled Chatbot](./lab-1-rag-chatbot/README.md)
**Duration**: 2-3 hours

In this lab, you will:
- Set up your Azure AI Foundry environment
- Understand RAG architecture and its benefits
- Build a knowledge base using Azure AI Search
- Create a chatbot using Microsoft Agent Framework (Semantic Kernel)
- Deploy your chatbot to Azure AI Foundry
- Test and validate your implementation

### [Lab 2: Adding Voice Capabilities](./lab-2-voice-capabilities/README.md)
**Duration**: 1-2 hours

In this lab, you will:
- Integrate Azure Speech Services
- Add speech-to-text (STT) functionality
- Add text-to-speech (TTS) functionality
- Create a voice-enabled interface
- Deploy the enhanced chatbot

## 🚀 Getting Started

### Option 1: GitHub Codespaces (Recommended - Fastest Setup) ⚡

GitHub Codespaces provides a pre-configured cloud development environment with everything installed.

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

- [Microsoft Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Microsoft Agent Framework (Semantic Kernel)](https://github.com/microsoft/semantic-kernel)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Understanding RAG](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)
- [Azure Speech Services](https://azure.microsoft.com/en-us/products/ai-services/speech-to-text)

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section in each lab's README
2. Review the [resources](./resources/README.md) folder for additional guidance
3. Ask your instructor or workshop facilitator
4. Open an issue in this repository

## 📝 Workshop Feedback

We value your feedback! After completing the workshop, please share your experience to help us improve.

## 📄 License

This workshop content is provided for educational purposes.

---

**Ready to begin?** Head over to [Lab 1](./lab-1-rag-chatbot/README.md) to get started!
