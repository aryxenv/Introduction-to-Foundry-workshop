# Lab 1: Building a RAG-Enabled Chatbot

## 🎯 Lab Overview

In this lab, you'll build a chatbot with Retrieval-Augmented Generation (RAG) capabilities using Microsoft Foundry. By the end of this lab, you'll have a production-ready chatbot that can answer questions based on your custom knowledge base.

**Estimated Time**: 75-105 minutes (depending on path chosen)

---

## 🛤️ Choose Your Path

This lab offers two parallel paths. Choose the one that best fits your learning goals:

| Path | Description | Best For |
|------|-------------|----------|
| **🖥️ Portal Path** | Use Azure Portal and Foundry UI exclusively | Quick setup, visual learners, no coding required |
| **💻 Code Path** | Build everything programmatically with Python | Developers, automation, deeper understanding |

> **Tip**: You can mix and match! Start with Portal to understand concepts, then try Code for specific sections.

---

## 📖 What You'll Learn

- **RAG Fundamentals**: Understanding how RAG works and is implemented in Azure
- **Azure AI Search**: Working with embeddings and semantic search on Azure
- **Azure Blob Storage**: Storing and managing your source documents
- **Microsoft Foundry**: Using the unified AI platform for deployment

---

## 🏗️ Architecture Overview

### What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that enhances Large Language Models (LLMs) by providing them with relevant context from a knowledge base. Instead of relying solely on the model's training data, RAG:

1. **Retrieves** relevant information from your documents
2. **Augments** the user's query with this context
3. **Generates** accurate, contextually-aware responses

### System Architecture

```
                                                    
                                                                      
User Query ──┬──→ Embedding → Vector Search → Relevant Context        
             │                                      │                  
             │                                      ↓                  
             └─────────────────────────────────→  LLM  ───→ Response   
                                                                     
                                                    
```

### Microsoft Services Used

| Component | Microsoft Service | Purpose |
|-----------|------------------|---------|
| **AI Platform** | Microsoft Foundry | Unified platform for building, deploying, and managing AI applications || **Knowledge Layer** | Foundry IQ | Manages knowledge bases with agentic retrieval and permission-aware responses || **Document Storage** | Azure Blob Storage | Stores your source documents (PDFs, text files, etc.) |
| **Vector Search** | Azure AI Search | Stores embeddings and performs semantic search |
| **Embedding Model** | Microsoft Foundry Model (text-embedding-3-small) | Converts text into numerical vectors |
| **LLM** | Microsoft Foundry Model (GPT-4o) | Generates natural language responses |

### How It All Fits Together

1. **Microsoft Foundry** is your central hub - it's where you create your project, manage models, and deploy your agent. It also provides both the embedding model (for search) and the LLM (for responses)
2. **Azure Blob Storage** is where you upload your source documents (company policies, FAQs, product info, etc.)
3. **Azure AI Search** indexes your documents, chunks them, creates embeddings, and enables semantic search
4. **Foundry IQ** connects it all together - it creates a knowledge base from your indexed data and uses agentic retrieval to provide your agent with permission-aware, grounded answers with citations

---

## 📋 Sub-Labs

| Sub-Lab | Time | Portal | Code |
|---------|------|:------:|:----:|
| [1.1 Set Up Azure Resources](./sub-lab-1.1-setup-azure-resources.md) | 15-20 min | ✅ | ✅ |
| [1.2 Prepare Your Knowledge Base](./sub-lab-1.2-prepare-knowledge-base.md) | 10-15 min | ✅ | ✅ |
| [1.3 Create Vector Index](./sub-lab-1.3-create-vector-index.md) | 15-20 min | ✅ | ✅ |
| [1.4 Create Your Agent in Foundry](./sub-lab-1.4-create-agent.md) | 15-20 min | ✅ | ✅ |
| [1.5 Host Agent as Web App](./sub-lab-1.5-host-agent-webapp.md) | 20-30 min | ❌ | ✅ |

---

Complete these individual labs before continuing to Lab 2. 

## 🔍 Troubleshooting

### Common Issues

**Issue**: "Authentication failed" when connecting to Azure services

**Solution**: 
- Ensure you're logged in: `az login`
- Check your `.env` file has correct values
- Verify role assignments are in place

---

**Issue**: Search returns no results

**Solution**:
- Verify documents were uploaded to Blob Storage
- Check the indexing job completed successfully
- Ensure embedding model deployment is correct

---

**Issue**: Responses are not relevant

**Solution**:
- Add more context to your documents
- Adjust chunk size (try 300-800 characters)
- Increase `top_k` in retrieval

---

## 📚 Additional Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure AI Search RAG Tutorial](https://learn.microsoft.com/en-us/azure/search/search-get-started-rag)
- [RAG Best Practices](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

---

## 🚀 Next Steps

Ready to add voice capabilities? Head over to [Lab 2: Adding Voice Capabilities](../lab-2-voice-capabilities/README.md)!


