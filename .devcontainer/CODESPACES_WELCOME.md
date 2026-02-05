# 🚀 Welcome to Azure AI Foundry Workshop on Codespaces!

Your development environment is ready! Everything has been pre-installed and configured.

## ✅ What's Already Installed

- ✅ Python 3.10
- ✅ All Lab 1 dependencies
- ✅ All Lab 2 dependencies
- ✅ Azure CLI with ML extension
- ✅ VS Code extensions (Python, Jupyter, Azure Tools)
- ✅ Docker support

## 📋 Quick Start (3 Steps)

### Step 1: Authenticate with Azure

```bash
az login
```

Follow the prompts to sign in to your Azure account.

### Step 2: Configure Your Credentials

Edit the `.env` files in both labs with your Azure credentials:

**Lab 1:**
```bash
cd lab-1-rag-chatbot
code .env
```

Fill in:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_CHAT_DEPLOYMENT`
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`
- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_API_KEY`

**Lab 2:**
```bash
cd ../lab-2-voice-capabilities
code .env
```

Add:
- `AZURE_SPEECH_KEY`
- `AZURE_SPEECH_REGION`

### Step 3: Start Lab 1

```bash
cd lab-1-rag-chatbot
code README.md
```

Follow the instructions in the README!

## 🎯 Workshop Structure

```
├── lab-1-rag-chatbot/          # Build RAG chatbot
│   ├── README.md               # Step-by-step guide
│   ├── src/                    # Source code
│   ├── data/knowledge_base/    # Sample documents
│   └── .env                    # Your Azure credentials
│
├── lab-2-voice-capabilities/   # Add voice features
│   ├── README.md               # Step-by-step guide
│   ├── src/                    # Voice handler code
│   ├── web/                    # Web interface
│   └── .env                    # Voice service credentials
│
└── resources/                  # Helpful guides
    ├── azure-ai-foundry-guide.md
    ├── troubleshooting.md
    └── example-prompts.md
```

## 💡 Useful Commands

### Activate Virtual Environments

**Lab 1:**
```bash
cd lab-1-rag-chatbot
source venv/bin/activate
```

**Lab 2:**
```bash
cd lab-2-voice-capabilities
source venv/bin/activate
```

### Test API Locally

```bash
cd lab-1-rag-chatbot
source venv/bin/activate
uvicorn src.api:app --reload --port 8000
```

Access at: http://localhost:8000/docs

### View Logs

```bash
# Codespaces exposes ports automatically
# Look for "Ports" tab at bottom of VS Code
```

## 🆘 Need Help?

1. **Check the guides:**
   - [Lab 1 README](lab-1-rag-chatbot/README.md)
   - [Lab 2 README](lab-2-voice-capabilities/README.md)
   - [Troubleshooting Guide](resources/troubleshooting.md)
   - [Azure AI Foundry Guide](resources/azure-ai-foundry-guide.md)

2. **Common Issues:**
   - Missing Azure credentials? → Edit `.env` files
   - Import errors? → Check virtual environment is activated
   - Port already in use? → Kill existing process or use different port

3. **Still stuck?**
   - Ask your workshop instructor
   - Check the troubleshooting guide
   - Review Azure documentation

## 🎉 Ready to Start!

Head over to **[Lab 1](lab-1-rag-chatbot/README.md)** to build your first RAG chatbot!

---

**Pro Tips:**
- 💾 Save frequently (Codespaces auto-saves your work)
- 🔄 Codespaces stops after 30 minutes of inactivity (free tier)
- 📊 Use the integrated terminal (View → Terminal)
- 🐛 VS Code debugger is pre-configured
- 📝 Jupyter notebooks work out of the box

Happy coding! 🚀
