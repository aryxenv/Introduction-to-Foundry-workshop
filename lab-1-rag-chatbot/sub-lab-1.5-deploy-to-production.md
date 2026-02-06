# Sub-Lab 1.5: Deploy to Production

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.4](./sub-lab-1.4-test-chatbot.md)

---

**⏱️ Estimated Time**: 20-30 minutes

## Overview

In this sub-lab, you'll deploy your RAG chatbot for production use, making it accessible to users.

---

## 🖥️ Option: Console

<details>
<summary><strong>Click to expand Console instructions</strong></summary>

### 1. Deploy via Foundry Portal

1. Go to [Microsoft Foundry](https://ai.azure.com)
2. Select your project (`my-first-chatbot`)
3. Go to **Playground** → **Chat**
4. Configure your chat with the AI Search data source (as done in Sub-Lab 1.4)
5. Once satisfied with the configuration, click **"Deploy"** → **"Web app"**

### 2. Configure the Web App Deployment

1. Configure deployment settings:
   - **Name**: `rag-chatbot-webapp-[yourname]`
   - **Subscription**: Your subscription
   - **Resource group**: `rg-foundry-chatbot-workshop`
   - **Location**: East US
   - **Pricing plan**: Basic (B1)
2. Click **Deploy**
3. Wait for deployment to complete (5-10 minutes)

### 3. Access Your Deployed Chatbot

1. Once deployed, you'll receive a URL
2. Open the URL in your browser
3. Test with your sample questions:
   - "What products does TechCorp offer?"
   - "What is the return policy?"

### 4. Configure Authentication (Optional)

For production use, you may want to add authentication:

1. Go to your Web App in Azure Portal
2. Navigate to **Authentication**
3. Click **Add identity provider**
4. Choose **Microsoft** (or your preferred provider)
5. Configure settings and save

### ✅ Console Checkpoint

- [ ] Web app deployed successfully
- [ ] Chatbot accessible via URL
- [ ] Responses are accurate
- [ ] (Optional) Authentication configured

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

### 1. Create FastAPI Application

Create `src/api.py`:

```python
"""
FastAPI application for RAG chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid

from rag_agent import RAGChatbot

app = FastAPI(
    title="RAG Chatbot API",
    description="A RAG-enabled chatbot using Azure AI Search and OpenAI",
    version="1.0.0"
)

# Enable CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = RAGChatbot()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    session_id: str

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the RAG chatbot and get a response.
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        result = chatbot.chat(request.message)
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. Create Requirements File

Update `requirements.txt`:

```
fastapi>=0.104.0
uvicorn>=0.24.0
python-dotenv>=1.0.0
azure-identity>=1.15.0
azure-search-documents>=11.4.0
azure-storage-blob>=12.19.0
openai>=1.3.0
pydantic>=2.5.0
```

### 3. Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn src.api:app --reload --port 8000
```

Test at: http://localhost:8000/docs

**Test with cURL:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What products does TechCorp offer?"}'
```

### 4. Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Set environment variables
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/api/health')" || exit 1

# Run the application
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5. Deploy to Azure Web App

```bash
# Create App Service Plan
az appservice plan create \
  --name chatbot-plan \
  --resource-group rg-foundry-chatbot-workshop \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name rag-chatbot-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --plan chatbot-plan \
  --runtime "PYTHON:3.10"

# Configure environment variables
az webapp config appsettings set \
  --name rag-chatbot-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --settings \
    AZURE_OPENAI_ENDPOINT="https://foundry-workshop-[yourname].openai.azure.com/" \
    AZURE_OPENAI_CHAT_DEPLOYMENT="gpt-4o" \
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small" \
    AZURE_SEARCH_ENDPOINT="https://search-chatbot-[yourname].search.windows.net" \
    AZURE_SEARCH_INDEX_NAME="chatbot-knowledge-base"

# Deploy code (from lab-1-rag-chatbot directory)
az webapp up \
  --name rag-chatbot-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --runtime "PYTHON:3.10"
```

### 6. Enable Managed Identity

For secure authentication without API keys:

```bash
# Enable system-assigned managed identity
az webapp identity assign \
  --name rag-chatbot-[yourname] \
  --resource-group rg-foundry-chatbot-workshop

# Get the principal ID
PRINCIPAL_ID=$(az webapp identity show \
  --name rag-chatbot-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --query principalId -o tsv)

# Grant access to Azure OpenAI
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Cognitive Services OpenAI User" \
  --scope /subscriptions/{subscription-id}/resourceGroups/rg-foundry-chatbot-workshop/providers/Microsoft.CognitiveServices/accounts/foundry-workshop-[yourname]

# Grant access to Azure AI Search
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Search Index Data Reader" \
  --scope /subscriptions/{subscription-id}/resourceGroups/rg-foundry-chatbot-workshop/providers/Microsoft.Search/searchServices/search-chatbot-[yourname]
```

### 7. Verify Deployment

```bash
# Test health endpoint
curl https://rag-chatbot-[yourname].azurewebsites.net/api/health

# Test chat endpoint
curl -X POST https://rag-chatbot-[yourname].azurewebsites.net/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What products does TechCorp offer?"}'
```

**Expected Response:**
```json
{
  "response": "TechCorp offers three main products: SmartAssist (AI customer service platform), DataVision (Business intelligence and analytics), and CloudSync (Multi-cloud data synchronization).",
  "sources": ["company_info.txt"],
  "session_id": "abc-123-def-456"
}
```

### ✅ Code Checkpoint

- [ ] API runs locally on port 8000
- [ ] Deployed to Azure Web App
- [ ] Health endpoint responds
- [ ] Chat endpoint returns correct responses
- [ ] Managed identity configured for secure access

</details>

---

## 🎓 Key Concepts

### Deployment Options

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Foundry Web App** | Easy, integrated | Less customization | Quick demos |
| **Azure Web App** | Flexible, scalable | More setup | Production |
| **Container Apps** | Serverless, auto-scale | More complex | High traffic |

### Production Considerations

#### Security
- ✅ Use Managed Identity (no API keys in code)
- ✅ Enable HTTPS only
- ✅ Add authentication for users
- ✅ Use Azure Key Vault for secrets

#### Monitoring
- Enable Application Insights
- Set up alerts for errors
- Monitor token usage and costs

#### Scaling
- Use auto-scaling for traffic spikes
- Consider caching frequent queries
- Monitor response times

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/api/health` | GET | Health check |
| `/api/chat` | POST | Send message, get response |
| `/docs` | GET | Interactive API documentation |

---

## 🎉 Congratulations!

You've completed Lab 1! You now have:

- ✅ A fully functional RAG chatbot
- ✅ Documents indexed in Azure AI Search
- ✅ A deployed API accessible via URL

### What You've Learned

1. **RAG Architecture**: How retrieval and generation work together
2. **Azure Services**: Foundry, Blob Storage, AI Search, OpenAI
3. **Vector Search**: Embeddings and semantic similarity
4. **Deployment**: Taking AI from development to production

---

## 🚀 Next Steps

Ready to add voice capabilities? Head over to [Lab 2: Adding Voice Capabilities](../lab-2-voice-capabilities/README.md)!

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.4](./sub-lab-1.4-test-chatbot.md)
