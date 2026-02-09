# Sub-Lab 1.4: Create Your Agent in Foundry

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.3](./sub-lab-1.3-create-vector-index.md) | [Next: Sub-Lab 1.5 →](./sub-lab-1.5-host-agent-webapp.md)

---

**⏱️ Estimated Time**: 15-20 minutes

## Overview

In this sub-lab, you'll create an AI agent in Microsoft Foundry that uses your vector index to answer questions. The agent combines GPT-4o with your indexed documents to provide accurate, context-aware responses.

---

## 🎓 Key Concepts

### What is Foundry IQ?

Foundry IQ is a managed knowledge layer that connects your enterprise data to AI agents. It provides:
- **Multi-source knowledge bases**: Connect Azure Blob Storage, SharePoint, OneLake, and web data
- **Agentic retrieval**: Automatically decomposes complex questions into subqueries, executes them in parallel, and aggregates results
- **Permission-aware responses**: Enforces access control so agents only return content users are authorized to see
- **Grounded answers with citations**: Returns extractive data with sources so agents can trace answers back to documents

### What is a Foundry Agent?

A Foundry Agent is an AI-powered assistant that can:
- **Understand** natural language questions
- **Search** your knowledge base for relevant information
- **Generate** accurate responses based on your documents
- **Cite** sources so users know where answers come from

### What is Microsoft Agent Framework?

Microsoft Agent Framework is an open-source SDK for building AI agents in Python and .NET. It's the unified foundation for building agents, combining the best of Semantic Kernel and AutoGen:
- **Single agents**: Use LLMs to process inputs, call tools, and generate responses
- **Workflows**: Connect multiple agents for complex multi-step tasks
- **Hosted agents**: Deploy agents to Foundry Agent Service for production use

### How the Agent Uses Foundry IQ

When a user asks a question:
1. The agent sends the question to Foundry IQ
2. Foundry IQ uses agentic retrieval to search your indexed content
3. Relevant chunks are returned with citations
4. GPT-4o generates a response grounded in your documents

---

## 🖥️ Option: Portal

<details>
<summary><strong>Click to expand Portal instructions</strong></summary>

### 1. Navigate to Foundry Portal

1. Go back to [Microsoft Foundry](https://ai.azure.com)
2. Select your project (`my-first-chatbot`)

### 2. Create a Foundry IQ connection

1. In the top menu, go to Build
2. Go to "Knowledge" on the left
3. Connect to an AI Search resource by selecting your index at the bottom. This allows Foundry IQ to intelligently search between different knowledge sources in the knowledge base
4. choose API Key as the Auth Type. 
5. Press connect

   <img src="images/Foundry-IQ.png" width="1000"/>

### 3. Create a knowledge base in Foundry IQ

1. Click "Create a knowledge base"
2. Choose Azure AI Search Index (under "Configure a knowledge base")
3. Give a description: e.g. `Contains company info and policies`
4. Select the `rag-XXXX` option you see under "Select search index"
5. Select a chat completions model; gpt-4o
5. Click Save "knowledge base"  on the top right

### 4. Create an agent
1. Go to Build -> Agents 
2. Click "Create agent"
3. Give the agent a name, e.g. `RAG-Chatbot`
4. Add instructions to the agent:
     ```
     You are a helpful customer service assistant for TechCorp. 
     Answer questions based on the provided knowledge base. 
     If you don't know the answer, say so - don't make things up.
     Always be polite and professional.
     ```
5. Click "Knowledge" and then "Add" and then Connect ot Foundry IQ
6. Select the knowledge base in the list and then "Connect".
   <img src="images/create-agent-1.png" width="500"/>
7. Press "Save" on the top right
    <img src="images/create-agent-2.png" width="1000"/>



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
3. Your Agent will ask you to retrieve context from the knowledge base
    <img src="images/test-agent-1.png" width="800"/>

4. The agent will provide an answer based on the info in the knowledge base: 
    <img src="images/test-agent-2.png" width="800"/>

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

### 6. Publish the Agent (Optional)

Once you're satisfied with the agent's responses:

1. Click **Publish** on the top right (and then publish and publish)
2. Your agent will now return a:
   - **Activity Protocol endpoint**: 
   - **Responses API endpoint**: For integration with your own applications

When you publish an agent, Microsoft Foundry creates an Agent Application resource with a dedicated invocation URL and its own Microsoft Entra agent identity blueprint and agent identity. A deployment is created under the application that references your agent version and registers it in the Entra Agent Registry for discovery and governance.

Publishing enables you to share agents with teammates, your organization, or customers without granting access to your Foundry project or source code. The stable endpoint remains consistent as you iterate and deploy new agent versions.
### ✅ Portal Checkpoint

You should now have:
- [ ] Agent created in Foundry
- [ ] Knowledge base (AI Search index) connected
- [ ] Agent responds accurately to test questions
- [ ] (Optional) Agent deployed for production use

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

> 📝 **First time using Code path?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.

### 1. Install Microsoft Agent Framework

```bash
pip install agent-framework azure-ai-projects azure-identity python-dotenv --pre
```

### 2. Update Environment Variables

Add to your `.env` file:

```properties
# Foundry Project Configuration
AZURE_AI_PROJECT_CONNECTION_STRING=your-project-connection-string
```

> 💡 **Tip**: Find your connection string in the Foundry portal under **Project settings** → **Overview** → **Project connection string**

### 3. Create the RAG Agent

Create `src/rag_agent.py`:

```python
"""
RAG Chatbot Agent using Microsoft Agent Framework
Deployed as a hosted agent in Foundry
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from agent_framework import AIAgent
from agent_framework.azure_ai import AzureAIAgent

load_dotenv()

# Configuration
PROJECT_CONNECTION_STRING = os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "chatbot-knowledge-base")

# Agent instructions
AGENT_INSTRUCTIONS = """
You are a helpful customer service assistant for TechCorp.
Answer questions based on the provided knowledge base.
If you don't know the answer, say so - don't make things up.
Always be polite and professional.
When citing information, mention the source document.
"""


def create_rag_agent():
    """Create a RAG agent with Azure AI Search grounding"""
    
    # Initialize the project client
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=PROJECT_CONNECTION_STRING,
        credential=credential
    )
    
    # Create agent with Azure AI Search tool for knowledge retrieval
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="RAG-Chatbot",
        instructions=AGENT_INSTRUCTIONS,
        tools=[{
            "type": "azure_ai_search",
            "azure_ai_search": {
                "index_name": SEARCH_INDEX_NAME
            }
        }]
    )
    
    print(f"✅ Created agent: {agent.name} (ID: {agent.id})")
    return agent, project_client


def chat_with_agent(agent, project_client):
    """Interactive chat session with the agent"""
    
    # Create a conversation thread
    thread = project_client.agents.create_thread()
    print(f"📝 Created thread: {thread.id}")
    print("\n🤖 RAG Chatbot ready! Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        if not user_input:
            continue
        
        # Add user message to thread
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        
        # Run the agent
        run = project_client.agents.create_and_process_run(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        # Get the response
        messages = project_client.agents.list_messages(thread_id=thread.id)
        assistant_message = next(
            (m for m in messages.data if m.role == "assistant"),
            None
        )
        
        if assistant_message:
            response_text = assistant_message.content[0].text.value
            print(f"\n🤖 Agent: {response_text}\n")


def main():
    print("🚀 Starting RAG Chatbot Agent...\n")
    
    agent, project_client = create_rag_agent()
    
    try:
        chat_with_agent(agent, project_client)
    finally:
        # Cleanup: delete the agent when done (optional)
        # project_client.agents.delete_agent(agent.id)
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
```

### 4. Run the Agent Locally

```bash
python src/rag_agent.py
```

**Expected Output:**
```
🚀 Starting RAG Chatbot Agent...

✅ Created agent: RAG-Chatbot (ID: asst_abc123...)
📝 Created thread: thread_xyz789...

🤖 RAG Chatbot ready! Type 'quit' to exit.

You: What products does TechCorp offer?

🤖 Agent: Based on the knowledge base, TechCorp offers three main products:
1. **SmartAssist** - An AI customer service platform
2. **DataVision** - Business intelligence and analytics
3. **CloudSync** - Multi-cloud data synchronization

*Source: company_info.txt*
```

### 5. Deploy as Hosted Agent (Optional)

To deploy your agent as a hosted service in Foundry:

```python
"""
Deploy the agent as a hosted agent in Foundry
"""
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def deploy_agent_to_foundry(agent_id: str):
    """Deploy an existing agent as a hosted agent"""
    
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=PROJECT_CONNECTION_STRING,
        credential=credential
    )
    
    # Create an agent application for hosting
    app = project_client.agents.create_agent_application(
        agent_id=agent_id,
        name="rag-chatbot-app",
        description="RAG Chatbot for TechCorp customer service"
    )
    
    print(f"✅ Agent deployed!")
    print(f"📍 Endpoint URL: {app.endpoint_url}")
    print(f"🆔 Application ID: {app.id}")
    
    return app
```

### ✅ Code Checkpoint

You should now have:
- [ ] Microsoft Agent Framework installed
- [ ] RAG agent created with Azure AI Search tool
- [ ] Agent responds to questions using your knowledge base
- [ ] (Optional) Agent deployed as hosted service in Foundry

</details>

---

## 🎉 Congratulations!

You've completed Lab 1! You now have a fully functional RAG chatbot that:

- 📚 Uses your custom knowledge base (stored in Blob Storage)
- 🔍 Performs semantic search (powered by Azure AI Search)
- 🤖 Generates accurate responses (using GPT-4o in Foundry)

### What You Built

```
┌────────────────────────────────────────────────────────────────┐
│                     Microsoft Foundry                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Your Agent                           │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │   GPT-4o    │ ←→ │  AI Search  │ ←→ │Blob Storage │  │   │
│  │  │  (answers)  │    │  (search)   │    │  (docs)     │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### Next Steps

Ready to deploy your agent as a web app? Continue to:

**[Sub-Lab 1.5: Host Agent as Web App →](./sub-lab-1.5-host-agent-webapp.md)**

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.3](./sub-lab-1.3-create-vector-index.md) | [Next: Sub-Lab 1.5 →](./sub-lab-1.5-host-agent-webapp.md)
