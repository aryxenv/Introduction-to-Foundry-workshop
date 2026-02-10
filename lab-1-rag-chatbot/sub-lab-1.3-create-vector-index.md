# Sub-Lab 1.3: Create Vector Index

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.2](./sub-lab-1.2-prepare-knowledge-base.md) | [Next: Sub-Lab 1.4 →](./sub-lab-1.4-create-agent.md)

---

**⏱️ Estimated Time**: 15-20 minutes

## Overview

In this sub-lab, you'll create a vector index in Azure AI Search. This index stores embeddings (numerical representations) of your documents, enabling the chatbot to find relevant information based on meaning rather than just keywords.

You'll also configure the necessary permissions so AI Search can read your documents from Blob Storage and use the embedding model from Foundry.

---

## 🎓 Key Concepts

### What is a Vector Index?

A vector index stores numerical representations (embeddings) of your documents:
- **Embeddings**: Dense vectors (e.g., 1536 dimensions) that capture semantic meaning
- **Vector Search**: Find similar documents based on meaning, not just keywords
- **HNSW Algorithm**: Efficient approximate nearest neighbor search

### How Embeddings Work

```
"What is the return policy?" 
    ↓ Embedding Model
[0.023, -0.456, 0.789, ..., 0.234]  (1536 numbers)
```

Similar meanings → Similar vectors → Found together in search

### Example

These questions have different words but similar meanings:
- "How do I return a product?"
- "What's your refund policy?"
- "Can I get my money back?"

The embedding model understands this similarity!

### Index Schema

Our index has these fields:
| Field | Type | Purpose |
|-------|------|---------|
| `id` | String | Unique identifier for each chunk |
| `content` | String | The actual text content |
| `source` | String | Original document name |
| `embedding` | Vector (1536) | Numerical representation |

---

## Resources You'll Create

- **Azure AI Search Service**: Search infrastructure
- **Vector Index**: Searchable index with embeddings
- **Role Assignments**: Permissions for AI Search to access Storage and Foundry

---

## 🖥️ Option: Portal

<details>
<summary><strong>Click to expand Portal instructions</strong></summary>

### 1. Create Azure AI Search Service

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Azure AI Search" → Click "Create"

   <img src="images/ai-search-1.png" width="800"/>

3. Configure:
   - **Resource group**: `rg-foundry-chatbot-workshop`
   - **Service name**: `search-chatbot-[yourname]` (must be globally unique)
   - **Location**: East US 2
   - **Pricing tier**: Free (sufficient for workshop)
4. Click "Review + Create" → "Create"

   <img src="images/ai-search-2.png" width="500"/>

### 2. Grant AI Search Access to Storage

Your AI Search service needs permission to read documents from Blob Storage.

1. Go to your **Storage Account** → Access Control (IAM)
2. Click **Add** → **Add role assignment**
3. Select role: **Storage Blob Data Reader**
4. Click **Next**
5. Select **Managed identity**
6. Click **Select members**
7. Under "Managed identity", choose **Search service**
8. Select: `search-chatbot-[yourname]`
9. Click **Select** → **Review + assign** (twice)

   <img src="images/storage-account-6.png" width="500"/>

### 3. Grant AI Search Access to Foundry

Your AI Search service needs permission to use the embedding model.

1. Go to your **Foundry resource** → Access Control (IAM)
2. Click **Add** → **Add role assignment**

   <img src="images/foundry-resource-3.png" width="1000"/>

3. Select role: **Cognitive Services OpenAI User**
4. Click **Next**
5. Select **Managed identity** → **Select members**
6. Choose **Search service** → Select: `search-chatbot-[yourname]`
7. Click **Select** → **Review + assign** (twice)

### 4. Import and Index Your Data

1. Go to your AI Search resource
2. Click **"Import data (new)"**

   <img src="images/ai-search-3.png" width="800"/>

3. **Configure data source**:
   - **Data source**: Azure Blob Storage
   - **Use case**: RAG
   - **Storage account**: `stchatbot[yourname]`
   - **Container**: `knowledge-base-container`
4. Click **Next**

5. **Configure embeddings**:
   - **Kind**: Microsoft Foundry
   - **Hub project**: Select your project (`my-first-chatbot`)
   - **Model deployment**: `text-embedding-3-small`
   - ✅ Check: "I acknowledge..."
6. Click **Next** → **Next** → **Next** → **Create**

### 5. Wait for Indexing

- The indexing process takes 2-5 minutes
- Monitor progress in the Search service → Indexes section
- Once complete, you'll see document count and status

### ✅ Portal Checkpoint

You should now have:
- [ ] Azure AI Search service: `search-chatbot-[yourname]`
- [ ] Vector index with your documents
- [ ] Proper role assignments for Search to access Storage and Foundry

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

> 📝 **First time using the Code option?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.

### 1. Create AI Search Service via CLI

> ✏️ Copy the code below into a text editor, **replace `[yourname]`** with your actual name, then run the command **in Git Bash**.

```bash
# Create Azure AI Search service
az search service create \
  --name search-chatbot-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --sku free \
  --location eastus2
```

> 💡 **Note**: If you get an error about free tier quota being exhausted, use `--sku basic` instead. Basic tier has a small cost but offers more capacity.

### 2. Enable Managed Identity and RBAC on AI Search

> ✏️ **Use PowerShell for this step.** Replace `[yourname]` with your actual name.

AI Search needs a managed identity to access other Azure resources, and RBAC authentication must be enabled for Azure AD-based access.

```powershell
# Enable system-assigned managed identity
az search service update `
  --name search-chatbot-[yourname] `
  --resource-group rg-foundry-chatbot-workshop `
  --identity-type SystemAssigned

# Enable RBAC authentication (required for Azure AD/managed identity access)
az search service update `
  --name search-chatbot-[yourname] `
  --resource-group rg-foundry-chatbot-workshop `
  --auth-options aadOrApiKey `
  --aad-auth-failure-mode http401WithBearerChallenge
```

> 💡 **Important**: By default, AI Search only allows API key authentication. The second command enables Azure AD authentication which is required for the Python script to work.

### 3. Grant AI Search Access to Storage

Your AI Search service needs permission to read documents from Blob Storage.

```powershell
# Get the AI Search managed identity principal ID
$SEARCH_IDENTITY = az search service show `
  --name search-chatbot-[yourname] `
  --resource-group rg-foundry-chatbot-workshop `
  --query identity.principalId -o tsv

# Verify the identity is set
Write-Host "SEARCH_IDENTITY: $SEARCH_IDENTITY"

# Get the storage account resource ID
$STORAGE_ID = az storage account show `
  --name stchatbot[yourname] `
  --resource-group rg-foundry-chatbot-workshop `
  --query id -o tsv

# Assign Storage Blob Data Reader role to AI Search
az role assignment create `
  --assignee "$SEARCH_IDENTITY" `
  --role "Storage Blob Data Reader" `
  --scope "$STORAGE_ID"
```

### 4. Grant AI Search Access to Foundry

Your AI Search service needs permission to use the embedding model.

```powershell
# Get the Foundry resource ID
$FOUNDRY_ID = az cognitiveservices account show `
  --name foundry-workshop-[yourname] `
  --resource-group rg-foundry-chatbot-workshop `
  --query id -o tsv

# Assign Cognitive Services OpenAI User role to AI Search
az role assignment create `
  --assignee "$SEARCH_IDENTITY" `
  --role "Cognitive Services OpenAI User" `
  --scope "$FOUNDRY_ID"
```

### 5. Grant Yourself Access to Manage AI Search

Your user account needs permission to create indexes, data sources, skillsets, and indexers via the REST API.

```powershell
# Get your user ID
$USER_ID = az ad signed-in-user show --query id -o tsv

# Get the AI Search resource ID
$SEARCH_ID = az search service show `
  --name search-chatbot-[yourname] `
  --resource-group rg-foundry-chatbot-workshop `
  --query id -o tsv

# Assign Search Service Contributor role (manage service resources)
az role assignment create `
  --assignee "$USER_ID" `
  --role "Search Service Contributor" `
  --scope "$SEARCH_ID"

# Assign Search Index Data Contributor role (manage index data)
az role assignment create `
  --assignee "$USER_ID" `
  --role "Search Index Data Contributor" `
  --scope "$SEARCH_ID"
```

> 💡 **Note**: Role assignments can take 1-2 minutes to propagate. Wait before running the indexing script.

### 6. Install Additional Dependencies

Run this in Git Bash:

```bash
pip install azure-search-documents requests
```

### 7. Create Vector Index with Integrated Vectorization

This approach uses AI Search's built-in vectorization - the same as the Portal "Import data" wizard.

Create a new file `create_vector_index.py` in the `scripts` folder:

```python
"""
Create a vector index with integrated vectorization in Azure AI Search
This matches the Portal 'Import data (new)' approach
"""
import os
import requests
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# Configuration
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "chatbot-knowledge-base")
STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "knowledge-base-container")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP", "rg-foundry-chatbot-workshop")

API_VERSION = "2024-07-01"

def get_auth_header():
    """Get authorization header using DefaultAzureCredential"""
    credential = DefaultAzureCredential()
    token = credential.get_token("https://search.azure.com/.default").token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def get_subscription_id():
    """Get current subscription ID"""
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default").token
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "https://management.azure.com/subscriptions?api-version=2022-01-01",
        headers=headers
    )
    return response.json()["value"][0]["subscriptionId"]

def create_index():
    """Create the vector search index"""
    index = {
        "name": INDEX_NAME,
        "fields": [
            {"name": "chunk_id", "type": "Edm.String", "key": True, "analyzer": "keyword"},
            {"name": "parent_id", "type": "Edm.String", "filterable": True},
            {"name": "chunk", "type": "Edm.String", "searchable": True},
            {"name": "title", "type": "Edm.String", "searchable": True, "filterable": True},
            {
                "name": "vector",
                "type": "Collection(Edm.Single)",
                "searchable": True,
                "dimensions": 1536,
                "vectorSearchProfile": "myHnswProfile"
            }
        ],
        "vectorSearch": {
            "algorithms": [{"name": "myHnsw", "kind": "hnsw"}],
            "profiles": [{"name": "myHnswProfile", "algorithm": "myHnsw"}]
        }
    }
    
    url = f"{SEARCH_ENDPOINT}/indexes/{INDEX_NAME}?api-version={API_VERSION}"
    response = requests.put(url, json=index, headers=get_auth_header())
    
    if response.status_code in [200, 201, 204]:
        print(f"✅ Created index: {INDEX_NAME}")
    else:
        print(f"❌ Error creating index ({response.status_code}): {response.text or response.reason}")

def create_data_source():
    """Create a data source connection to Blob Storage"""
    subscription_id = get_subscription_id()
    data_source = {
        "name": "chatbot-datasource",
        "type": "azureblob",
        "credentials": {
            "connectionString": f"ResourceId=/subscriptions/{subscription_id}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Storage/storageAccounts/{STORAGE_ACCOUNT_NAME}"
        },
        "container": {"name": CONTAINER_NAME}
    }
    
    url = f"{SEARCH_ENDPOINT}/datasources/chatbot-datasource?api-version={API_VERSION}"
    response = requests.put(url, json=data_source, headers=get_auth_header())
    
    if response.status_code in [200, 201, 204]:
        print(f"✅ Created data source: chatbot-datasource")
    else:
        print(f"❌ Error creating data source ({response.status_code}): {response.text or response.reason}")

def create_skillset():
    """Create a skillset with text splitting and embedding skills"""
    skillset = {
        "name": "chatbot-skillset",
        "skills": [
            {
                "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
                "name": "splitSkill",
                "textSplitMode": "pages",
                "maximumPageLength": 2000,
                "pageOverlapLength": 500,
                "inputs": [{"name": "text", "source": "/document/content"}],
                "outputs": [{"name": "textItems", "targetName": "chunks"}]
            },
            {
                "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
                "name": "embeddingSkill",
                "resourceUri": AZURE_OPENAI_ENDPOINT.rstrip('/'),
                "deploymentId": EMBEDDING_DEPLOYMENT,
                "modelName": "text-embedding-3-small",
                "inputs": [{"name": "text", "source": "/document/chunks/*"}],
                "outputs": [{"name": "embedding", "targetName": "vector"}]
            }
        ],
        "indexProjections": {
            "selectors": [{
                "targetIndexName": INDEX_NAME,
                "parentKeyFieldName": "parent_id",
                "sourceContext": "/document/chunks/*",
                "mappings": [
                    {"name": "chunk", "source": "/document/chunks/*"},
                    {"name": "vector", "source": "/document/chunks/*/vector"},
                    {"name": "title", "source": "/document/metadata_storage_name"}
                ]
            }],
            "parameters": {"projectionMode": "skipIndexingParentDocuments"}
        }
    }
    
    url = f"{SEARCH_ENDPOINT}/skillsets/chatbot-skillset?api-version={API_VERSION}"
    response = requests.put(url, json=skillset, headers=get_auth_header())
    
    if response.status_code in [200, 201, 204]:
        print(f"✅ Created skillset: chatbot-skillset")
    else:
        print(f"❌ Error creating skillset ({response.status_code}): {response.text or response.reason}")

def create_indexer():
    """Create an indexer to process documents"""
    indexer = {
        "name": "chatbot-indexer",
        "dataSourceName": "chatbot-datasource",
        "targetIndexName": INDEX_NAME,
        "skillsetName": "chatbot-skillset",
        "parameters": {
            "configuration": {
                "dataToExtract": "contentAndMetadata",
                "parsingMode": "default"
            }
        }
    }
    
    url = f"{SEARCH_ENDPOINT}/indexers/chatbot-indexer?api-version={API_VERSION}"
    response = requests.put(url, json=indexer, headers=get_auth_header())
    
    if response.status_code in [200, 201, 204]:
        print(f"✅ Created indexer: chatbot-indexer")
        print("⏳ Indexing in progress... (this may take a few minutes)")
    else:
        print(f"❌ Error creating indexer ({response.status_code}): {response.text or response.reason}")

def main():
    print("🚀 Starting indexing pipeline...\n")
    
    create_index()
    create_data_source()
    create_skillset()
    create_indexer()
    
    print("\n🎉 Indexing pipeline created!")
    print("📊 Monitor progress in Azure Portal → AI Search → Indexers")

if __name__ == "__main__":
    main()
```

### 8. Update Environment Variables

Add to your `.env` file:

```properties
# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://search-chatbot-[yourname].search.windows.net
AZURE_SEARCH_INDEX_NAME=chatbot-knowledge-base

# Azure Resource Group (must match your actual resource group name)
AZURE_RESOURCE_GROUP=rg-foundry-chatbot-workshop
```

### 9. Run the Indexing Script

```bash
cd lab-1-rag-chatbot
python scripts/create_vector_index.py
```

**Expected Output:**
```
🚀 Starting indexing pipeline...

✅ Created index: chatbot-knowledge-base
✅ Created data source: chatbot-datasource
✅ Created skillset: chatbot-skillset
✅ Created indexer: chatbot-indexer
⏳ Indexing in progress... (this may take a few minutes)

🎉 Indexing pipeline created!
📊 Monitor progress in Azure Portal → AI Search → Indexers
```

### ✅ Code Checkpoint

You should now have:
- [ ] Azure AI Search service created with managed identity and RBAC enabled
- [ ] Role assignments for AI Search to access Storage and Foundry
- [ ] Role assignments for your user to manage AI Search (Search Service Contributor, Search Index Data Contributor)
- [ ] Vector index with integrated vectorization (matching Portal approach)
- [ ] `.env` updated with Search endpoint and resource group

</details>

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.2](./sub-lab-1.2-prepare-knowledge-base.md) | [Next: Sub-Lab 1.4 →](./sub-lab-1.4-create-agent.md)
