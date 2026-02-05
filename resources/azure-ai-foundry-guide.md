# Azure AI Foundry Guide for Workshop

## What is Azure AI Foundry?

Microsoft Azure AI Foundry (formerly Azure AI Studio) is a unified platform for building, evaluating, and deploying AI applications on Azure. It provides an integrated experience for working with all Azure AI services.

### Key Features

1. **Unified Workspace**: Single platform for all Azure AI services
2. **Prompt Flow**: Visual designer for orchestrating AI workflows
3. **Model Catalog**: Access to various AI models (OpenAI, Hugging Face, etc.)
4. **Built-in Evaluation**: Test and validate AI applications
5. **Deployment Options**: Multiple ways to deploy (endpoints, web apps, containers)
6. **Monitoring & Observability**: Track performance, costs, and quality

## Architecture in Azure AI Foundry

### Hierarchy

```
Azure Subscription
  └── Resource Group
      ├── Azure AI Hub (Workspace)
      │   ├── Project 1 (Our RAG Chatbot)
      │   │   ├── Connections
      │   │   │   ├── Azure OpenAI
      │   │   │   ├── Azure AI Search
      │   │   │   └── Azure Speech
      │   │   ├── Deployments
      │   │   ├── Prompt Flows
      │   │   └── Evaluations
      │   └── Project 2
      ├── Azure OpenAI Service
      ├── Azure AI Search
      └── Azure Speech Service
```

### Key Concepts

**Hub**: Central workspace that contains shared resources, connections, and compute
- Reusable across multiple projects
- Manages security and governance
- Centralized billing

**Project**: Individual AI application workspace
- Contains specific deployments
- Has its own data and configurations
- Links to shared hub resources

**Connections**: Secure links to Azure services
- Azure OpenAI for LLMs and embeddings
- Azure AI Search for vector storage
- Azure Speech for voice capabilities
- Other data sources and services

## Setting Up Azure AI Foundry

### Prerequisites

1. **Azure Subscription**: Active subscription with credits
2. **Required Permissions**:
   - Contributor or Owner role on subscription/resource group
   - Azure AI Developer role
3. **Services Access**:
   - Azure OpenAI approved access
   - Regional availability check

### Step-by-Step Setup

#### 1. Create Azure AI Hub

**Via Portal:**

1. Go to [https://ai.azure.com](https://ai.azure.com)
2. Sign in with Azure credentials
3. Click "Create hub"
4. Configure:
   - **Name**: `aifoundry-chatbot-workshop`
   - **Subscription**: Select your subscription
   - **Resource group**: Create new or select existing
   - **Region**: eastus or westus (check OpenAI availability)
   - **Azure OpenAI**: Select existing or create new
   - **Azure AI Search**: Select existing or create new
5. Click "Create" (takes 2-5 minutes)

**Via Azure CLI:**

```bash
# Login
az login

# Install extension
az extension add --name ml

# Create resource group (if needed)
az group create \
  --name rg-foundry-chatbot-workshop \
  --location eastus

# Create hub
az ml workspace create \
  --kind hub \
  --name aifoundry-chatbot-workshop \
  --resource-group rg-foundry-chatbot-workshop \
  --location eastus
```

#### 2. Create Project

**Via Portal:**

1. In your hub, click "Create project"
2. Configure:
   - **Name**: `rag-chatbot`
   - **Description**: "RAG-enabled chatbot with voice"
3. Click "Create"

**Via CLI:**

```bash
az ml workspace create \
  --kind project \
  --hub-id /subscriptions/{sub-id}/resourceGroups/rg-foundry-chatbot-workshop/providers/Microsoft.MachineLearningServices/workspaces/aifoundry-chatbot-workshop \
  --name rag-chatbot \
  --resource-group rg-foundry-chatbot-workshop
```

#### 3. Set Up Connections

**Azure OpenAI Connection:**

1. In project, go to "Settings" → "Connections"
2. Click "+ New connection"
3. Select "Azure OpenAI"
4. Configure:
   - **Name**: `openai-connection`
   - **Subscription**: Your subscription
   - **Resource**: Select your Azure OpenAI resource
   - **API key**: Auto-filled if you have access
5. Click "Save"

**Azure AI Search Connection:**

1. Click "+ New connection"
2. Select "Azure AI Search"
3. Configure:
   - **Name**: `search-connection`
   - **Subscription**: Your subscription
   - **Resource**: Select your AI Search resource
   - **Admin key**: Provide admin key
4. Click "Save"

**Azure Speech Connection:**

1. Click "+ New connection"
2. Select "Azure AI Services" or "Custom"
3. Configure:
   - **Name**: `speech-connection`
   - **Subscription**: Your subscription
   - **Resource**: Select Speech Service
   - **API key**: Provide key
4. Click "Save"

## Working with Prompt Flow

Prompt Flow is Azure AI Foundry's visual tool for orchestrating AI workflows.

### Creating a RAG Flow

1. **Start New Flow**:
   - Go to "Prompt flow" in your project
   - Click "Create"
   - Select "Chat flow" template

2. **Add Nodes**:

   **Input Node**:
   - Name: `user_question`
   - Type: String
   - Description: User's question

   **Vector Search Node**:
   - Name: `retrieve_context`
   - Connection: `search-connection`
   - Index name: `chatbot-knowledge-base`
   - Query: `${user_question}`
   - Top K: 3

   **LLM Node**:
   - Name: `generate_response`
   - Connection: `openai-connection`
   - Deployment: `gpt-4`
   - Prompt template:
     ```
     You are a helpful assistant. Answer based on context.
     
     Context: ${retrieve_context.output}
     Question: ${user_question}
     
     Answer:
     ```
   - Temperature: 0.7
   - Max tokens: 1000

   **Output Node**:
   - Name: `response`
   - Value: `${generate_response.output}`

3. **Test Flow**:
   - Click "Test" in the interface
   - Enter test questions
   - Verify responses

4. **Deploy Flow**:
   - Click "Deploy"
   - Choose deployment type:
     - **Managed Online Endpoint**: Scalable, fully managed
     - **Web App**: Simpler deployment
   - Configure resources
   - Click "Deploy"

### Adding Voice to Prompt Flow

**Add Speech-to-Text Node**:
- Connection: `speech-connection`
- Input: Audio file
- Language: en-US
- Output: Transcribed text

**Add Text-to-Speech Node**:
- Connection: `speech-connection`
- Input: Response text
- Voice: en-US-JennyNeural
- Output: Audio file

## Deployment Options

### Option 1: Managed Online Endpoint (Recommended)

**Best for**: Production applications needing scale and reliability

```bash
# Create endpoint
az ml online-endpoint create \
  --name rag-chatbot-endpoint \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot

# Deploy
az ml online-deployment create \
  --name rag-chatbot-deployment \
  --endpoint rag-chatbot-endpoint \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot \
  --model-path ./model \
  --instance-type Standard_DS3_v2 \
  --instance-count 1
```

**Features**:
- Auto-scaling
- Load balancing
- Blue-green deployments
- Built-in monitoring
- HTTPS endpoints with authentication

### Option 2: Azure Web App

**Best for**: Simpler deployments, prototypes

```bash
# Create app service plan
az appservice plan create \
  --name chatbot-plan \
  --resource-group rg-foundry-chatbot-workshop \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --name rag-chatbot-webapp \
  --resource-group rg-foundry-chatbot-workshop \
  --plan chatbot-plan \
  --runtime "PYTHON:3.10"

# Deploy code
az webapp up \
  --name rag-chatbot-webapp \
  --resource-group rg-foundry-chatbot-workshop
```

**Features**:
- Simple deployment
- Integrated with VS Code
- Easy configuration
- Built-in SSL

### Option 3: Container Apps

**Best for**: Microservices, event-driven apps

```bash
# Create container app environment
az containerapp env create \
  --name chatbot-env \
  --resource-group rg-foundry-chatbot-workshop \
  --location eastus

# Deploy container app
az containerapp create \
  --name rag-chatbot-container \
  --resource-group rg-foundry-chatbot-workshop \
  --environment chatbot-env \
  --image your-registry/rag-chatbot:latest \
  --target-port 8000 \
  --ingress external
```

**Features**:
- Serverless containers
- Auto-scaling to zero
- Event-driven scaling
- Kubernetes-based

## Monitoring and Evaluation

### Application Insights

Automatically enabled in Azure AI Foundry:

1. **View Metrics**:
   - Go to "Monitoring" in project
   - View dashboards:
     - Request rate
     - Response time
     - Error rate
     - Dependencies

2. **Set Up Alerts**:
   ```bash
   az monitor metrics alert create \
     --name high-error-rate \
     --resource-group rg-foundry-chatbot-workshop \
     --scopes /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Web/sites/rag-chatbot-webapp \
     --condition "count exceptions/count > 10" \
     --window-size 5m \
     --evaluation-frequency 1m
   ```

### Cost Management

**View Costs**:
1. Azure Portal → Cost Management
2. Filter by resource group
3. View breakdown by service

**Optimize Costs**:
- Use GPT-3.5 for simple queries
- Cache frequent queries
- Set appropriate token limits
- Use auto-scaling effectively
- Monitor and adjust compute resources

### Evaluation Tools

**Built-in Evaluations**:

1. Go to "Evaluation" in AI Foundry
2. Create evaluation:
   - Select your flow
   - Upload test dataset
   - Choose metrics:
     - Groundedness
     - Relevance
     - Coherence
     - Fluency
3. Run evaluation
4. Review results and iterate

## Best Practices

### Security

1. **Use Managed Identities**:
   ```bash
   az ml workspace update \
     --name rag-chatbot \
     --system-assigned-identity \
     --resource-group rg-foundry-chatbot-workshop
   ```

2. **Network Isolation**:
   - Use private endpoints
   - Configure VNet integration
   - Restrict public access

3. **Access Control**:
   - Use Azure RBAC
   - Separate dev/prod environments
   - Audit access logs

### Performance

1. **Optimize Retrieval**:
   - Fine-tune chunk size
   - Use hybrid search
   - Implement caching

2. **Optimize Generation**:
   - Choose appropriate model
   - Set reasonable token limits
   - Use streaming for long responses

3. **Scale Appropriately**:
   - Start small, scale as needed
   - Use auto-scaling
   - Monitor performance metrics

### Development Workflow

1. **Local Development**:
   - Develop locally with `.env` file
   - Test with sample data
   - Use Python SDK

2. **CI/CD**:
   - Use GitHub Actions
   - Automate testing
   - Deploy to staging first

3. **Version Control**:
   - Track prompt versions
   - Version model deployments
   - Document changes

## Troubleshooting

### Common Issues

**Can't create hub**:
- Check subscription quotas
- Verify region supports AI services
- Check permissions

**Connection failed**:
- Verify service exists
- Check API keys
- Ensure network connectivity

**Deployment failed**:
- Check logs in Application Insights
- Verify all connections configured
- Check resource quotas

**High costs**:
- Review token usage
- Optimize model selection
- Implement caching
- Check for unnecessary API calls

## Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Prompt Flow Guide](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/)
- [Azure OpenAI Best Practices](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/best-practices)
- [Python SDK Reference](https://learn.microsoft.com/en-us/python/api/overview/azure/ml)

---

**Need Help?** Check the [troubleshooting guide](./troubleshooting.md) or ask your instructor!
