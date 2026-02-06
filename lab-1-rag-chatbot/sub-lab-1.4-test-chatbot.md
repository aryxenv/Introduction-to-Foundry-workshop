# Sub-Lab 1.4: Test Your RAG Chatbot

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.3](./sub-lab-1.3-create-vector-index.md) | [Next: Sub-Lab 1.5 →](./sub-lab-1.5-deploy-to-production.md)

---

**⏱️ Estimated Time**: 10-15 minutes

## Overview

In this sub-lab, you'll test your RAG chatbot to ensure it can retrieve relevant information and generate accurate responses.

---

## 🖥️ Option: Console

<details>
<summary><strong>Click to expand Console instructions</strong></summary>

### 1. Test in Azure AI Search

First, verify your index is working correctly.

1. Go to your **Azure AI Search** resource
2. Click on your index name (e.g., `azureblob-index`)
3. Click **"Search explorer"**
4. Try a simple search:
   - Enter: `products`
   - Click **Search**
5. Verify relevant chunks are returned

### 2. Test Vector Search

1. In Search explorer, click **"Query options"**
2. Enable **"Vector search"**
3. Enter a natural language query:
   - "What products does TechCorp offer?"
4. Verify semantically relevant results are returned

### 3. Test in Foundry Portal (Chat Playground)

1. Go to [Microsoft Foundry](https://ai.azure.com)
2. Select your project (`my-first-chatbot`)
3. Go to **Playground** → **Chat**
4. Configure the chat:
   - Select your `gpt-4o` deployment
   - Click **"Add your data"** (or similar option)
   - Connect to your AI Search index
5. Test with questions:

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
What are the office hours?
```

### Expected Results

The chatbot should:
- ✅ Return accurate information from your documents
- ✅ Cite or reference sources when answering
- ✅ Acknowledge when information isn't available

**Example Response:**
> TechCorp offers three main products:
> 1. **SmartAssist** - An AI customer service platform
> 2. **DataVision** - Business intelligence and analytics
> 3. **CloudSync** - Multi-cloud data synchronization

### ✅ Console Checkpoint

- [ ] Search explorer returns relevant document chunks
- [ ] Vector search finds semantically similar content
- [ ] Chat playground answers questions correctly

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

### 1. Create the RAG Agent

Create `src/rag_agent.py`:

```python
"""
RAG Chatbot using Azure OpenAI and AI Search
"""
import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

class RAGChatbot:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        
        # Initialize Azure OpenAI
        self.openai_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token=self.credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            ).token,
            api_version="2024-02-15-preview"
        )
        
        # Initialize Search Client
        self.search_client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
            credential=self.credential
        )
        
        self.chat_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
        self.embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    
    def _get_embedding(self, text: str) -> list:
        """Generate embedding for text"""
        response = self.openai_client.embeddings.create(
            input=text,
            model=self.embedding_deployment
        )
        return response.data[0].embedding
    
    def _retrieve_context(self, query: str, top_k: int = 3) -> tuple:
        """Retrieve relevant documents from search index"""
        query_embedding = self._get_embedding(query)
        
        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields="embedding"
        )
        
        results = self.search_client.search(
            search_text=None,
            vector_queries=[vector_query],
            select=["content", "source"]
        )
        
        contexts = []
        sources = []
        for result in results:
            contexts.append(result["content"])
            sources.append(result["source"])
        
        return "\n\n".join(contexts), list(set(sources))
    
    def chat(self, user_message: str) -> dict:
        """Process user message and return response"""
        print(f"🔍 Retrieving relevant context...")
        context, sources = self._retrieve_context(user_message)
        
        system_prompt = f"""You are a helpful AI assistant. Answer the user's question based on the provided context.
If the context doesn't contain relevant information, acknowledge that and provide a general helpful response.

Context:
{context}

Instructions:
- Be concise and accurate
- Cite specific information from the context when possible
- If uncertain, say so
"""
        
        response = self.openai_client.chat.completions.create(
            model=self.chat_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return {
            "response": response.choices[0].message.content,
            "sources": sources
        }

def main():
    """Interactive chatbot test"""
    print("🤖 RAG Chatbot Ready!")
    print("Type 'quit' to exit\n")
    
    chatbot = RAGChatbot()
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        result = chatbot.chat(user_input)
        print(f"\n💬 Bot: {result['response']}")
        print(f"📚 Sources: {', '.join(result['sources'])}\n")

if __name__ == "__main__":
    main()
```

### 2. Test the Chatbot

```bash
python src/rag_agent.py
```

### 3. Test Questions

Try these questions:

```
What products does TechCorp offer?
```
```
How long do I have to return a product?
```
```
What are the shipping options and costs?
```
```
What are the office hours?
```
```
Who is the CEO?
```
(This last question tests how the bot handles missing information)

### Expected Output

```
🤖 RAG Chatbot Ready!
Type 'quit' to exit

You: What products does TechCorp offer?
🔍 Retrieving relevant context...

💬 Bot: TechCorp offers three main products:
1. SmartAssist - An AI customer service platform
2. DataVision - Business intelligence and analytics
3. CloudSync - Multi-cloud data synchronization

These products are designed for enterprise customers.

📚 Sources: company_info.txt

You: What is the return policy?
🔍 Retrieving relevant context...

💬 Bot: According to the company policies, products can be returned within 30 days of purchase for a full refund. Items must be in original packaging and unused.

📚 Sources: policies.txt

You: quit
Goodbye!
```

### ✅ Code Checkpoint

- [ ] RAG agent runs without errors
- [ ] Questions are answered correctly using your documents
- [ ] Sources are properly cited
- [ ] Bot handles missing information gracefully

</details>

---

## 🎓 Key Concepts

### The RAG Flow

```
1. User asks: "What products does TechCorp offer?"
                    ↓
2. Generate embedding for the question
                    ↓
3. Vector search finds similar chunks:
   - "Our Products: SmartAssist, DataVision, CloudSync..."
                    ↓
4. Build prompt with context + question
                    ↓
5. LLM generates response using context
                    ↓
6. Return response with sources
```

### Why RAG is Powerful

| Without RAG | With RAG |
|-------------|----------|
| LLM uses only training data | LLM uses your specific documents |
| May hallucinate facts | Grounded in real information |
| Can't answer about your business | Accurate domain-specific answers |
| No source attribution | Can cite sources |

### Testing Best Practices

1. **Test factual questions**: Verify accuracy against documents
2. **Test edge cases**: Questions not covered in documents
3. **Test variations**: Different ways to ask the same thing
4. **Check sources**: Ensure correct documents are cited

---

## 🧪 Additional Test Scenarios

Try these to fully test your chatbot:

### Factual Questions
- "What is the company contact email?"
- "How much does express shipping cost?"

### Multi-part Questions
- "What products do you offer and what's the return policy?"

### Out-of-scope Questions
- "What is the weather today?"
- "Who is the CEO of TechCorp?"

### Ambiguous Questions
- "Tell me about shipping"
- "What are the policies?"

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.3](./sub-lab-1.3-create-vector-index.md) | [Next: Sub-Lab 1.5 →](./sub-lab-1.5-deploy-to-production.md)
