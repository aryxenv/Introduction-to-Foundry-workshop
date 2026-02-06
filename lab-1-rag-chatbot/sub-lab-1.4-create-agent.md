# Sub-Lab 1.4: Create Your Agent in Foundry

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.3](./sub-lab-1.3-create-vector-index.md)

---

**⏱️ Estimated Time**: 15-20 minutes

## Overview

In this sub-lab, you'll create an AI agent in Microsoft Foundry that uses your vector index to answer questions. The agent combines GPT-4o with your indexed documents to provide accurate, context-aware responses.

---

## 🎓 Key Concepts

### What is a Foundry Agent?

A Foundry Agent is an AI-powered assistant that can:
- **Understand** natural language questions
- **Search** your knowledge base for relevant information
- **Generate** accurate responses based on your documents
- **Cite** sources so users know where answers come from

### How the Agent Uses Your Index

When a user asks a question:
1. The agent converts the question into an embedding
2. It searches your vector index for similar content
3. The relevant chunks are passed to GPT-4o as context
4. GPT-4o generates a response grounded in your documents

---

## 🖥️ Option: Console

<details>
<summary><strong>Click to expand Console instructions</strong></summary>

### 1. Navigate to Foundry Portal

1. Go to [Microsoft Foundry](https://ai.azure.com)
2. Select your project (`my-first-chatbot`)

### 2. Create a New Agent

1. In the left menu, click **Agents**
2. Click **+ New Agent**

   <img src="images/agent-1.png" width="800"/>

3. Configure the agent:
   - **Name**: `RAG Chatbot`
   - **Instructions**: 
     ```
     You are a helpful customer service assistant for TechCorp. 
     Answer questions based on the provided knowledge base. 
     If you don't know the answer, say so - don't make things up.
     Always be polite and professional.
     ```

### 3. Connect Your Knowledge Base

1. In the agent configuration, find **Knowledge** or **Data sources**
2. Click **+ Add data source**
3. Select **Azure AI Search**
4. Configure the connection:
   - **Search service**: `search-chatbot-[yourname]`
   - **Index**: Select your index (e.g., `azureblob-index`)
   - **Authentication**: System assigned managed identity
5. Click **Save**

   <img src="images/agent-2.png" width="800"/>

### 4. Configure the Model

1. In **Model configuration**:
   - **Model**: Select `gpt-4o`
   - **Temperature**: 0.7 (balanced creativity/accuracy)
   - **Max tokens**: 800
2. Click **Save**

### 5. Test Your Agent

1. In the agent view, find the **Test** panel (usually on the right)
2. Try these questions:

**Test Questions:**
```
What products does TechCorp offer?
```
```
What is the return policy?
```
```
What are the shipping options and costs?
```
```
How can I contact customer support?
```

### Expected Results

The agent should:
- ✅ Return accurate information from your documents
- ✅ Cite or reference sources when answering
- ✅ Acknowledge when information isn't available
- ✅ Stay within the scope of your knowledge base

**Example Response:**
> Based on the knowledge base, TechCorp offers three main products:
> 1. **SmartAssist** - An AI customer service platform
> 2. **DataVision** - Business intelligence and analytics
> 3. **CloudSync** - Multi-cloud data synchronization
>
> *Source: company_info.txt*

### 6. Deploy the Agent (Optional)

Once you're satisfied with the agent's responses:

1. Click **Deploy** in the agent configuration
2. Choose deployment options:
   - **Web app**: Creates a standalone chat interface
   - **API endpoint**: For integration with your own applications
3. Configure settings and deploy

### ✅ Console Checkpoint

You should now have:
- [ ] Agent created in Foundry
- [ ] Knowledge base (AI Search index) connected
- [ ] Agent responds accurately to test questions
- [ ] (Optional) Agent deployed for production use

</details>

---

## 🎉 Congratulations!

You've completed Lab 1! You now have a fully functional RAG chatbot that:

- 📚 Uses your custom knowledge base (stored in Blob Storage)
- 🔍 Performs semantic search (powered by Azure AI Search)
- 🤖 Generates accurate responses (using GPT-4o in Foundry)

### What You Built

```
┌─────────────────────────────────────────────────────────────────┐
│                     Microsoft Foundry                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Your Agent                            │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │   GPT-4o    │ ←→ │  AI Search  │ ←→ │Blob Storage │  │   │
│  │  │  (answers)  │    │  (search)   │    │  (docs)     │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Next Steps

Ready to add voice capabilities to your chatbot? Continue to:

**[Lab 2: Voice Capabilities →](../lab-2-voice-capabilities/README.md)**

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.3](./sub-lab-1.3-create-vector-index.md)
