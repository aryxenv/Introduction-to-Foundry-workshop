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

## 💻 Option: Code - TO DO

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

> 📝 **First time using the Code option?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.

### 1. Create AI Search Service via CLI

> ✏️ Copy the code below into a text editor, **replace `[yourname]`** with your actual name, then run the command.

```bash
# Create Azure AI Search service
az search service create \
  --name search-chatbot-[yourname] \
  --resource-group rg-foundry-chatbot-workshop \
  --sku free \
  --location eastus2
```

### 2. Install Additional Dependencies

```bash
pip install azure-search-documents openai
```

### 3. Create Vector Index Programmatically

Create `scripts/create_vector_index.py`:

```python
"""
Create and populate a vector index in Azure AI Search
"""
import os
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SearchableField,
    SimpleField,
)
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "chatbot-knowledge-base")
STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

def create_index():
    """Create the vector search index"""
    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(SEARCH_ENDPOINT, credential)
    
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="myHnswProfile",
        ),
    ]
    
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
        profiles=[VectorSearchProfile(name="myHnswProfile", algorithm_configuration_name="myHnsw")],
    )
    
    index = SearchIndex(name=INDEX_NAME, fields=fields, vector_search=vector_search)
    result = index_client.create_or_update_index(index)
    print(f"✅ Created index: {result.name}")
    return result

def download_and_chunk_documents():
    """Download documents from Blob Storage and split into chunks"""
    credential = DefaultAzureCredential()
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url, credential=credential)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    
    chunks = []
    chunk_size = 500
    overlap = 50
    
    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob.name)
        content = blob_client.download_blob().readall().decode('utf-8')
        
        for i in range(0, len(content), chunk_size - overlap):
            chunk_text = content[i:i + chunk_size]
            if chunk_text.strip():
                chunks.append({
                    "id": f"{blob.name}_{i}",
                    "content": chunk_text,
                    "source": blob.name
                })
        
        print(f"📄 Processed: {blob.name}")
    
    print(f"🧩 Created {len(chunks)} chunks")
    return chunks

def generate_embeddings(chunks):
    """Generate embeddings for each chunk"""
    credential = DefaultAzureCredential()
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_ad_token=credential.get_token("https://cognitiveservices.azure.com/.default").token,
        api_version="2024-02-15-preview"
    )
    
    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk["content"],
            model=EMBEDDING_DEPLOYMENT
        )
        chunk["embedding"] = response.data[0].embedding
    
    print(f"🔢 Generated embeddings for {len(chunks)} chunks")
    return chunks

def upload_to_index(chunks):
    """Upload chunks with embeddings to Azure AI Search"""
    credential = DefaultAzureCredential()
    search_client = SearchClient(SEARCH_ENDPOINT, INDEX_NAME, credential)
    
    result = search_client.upload_documents(documents=chunks)
    print(f"📤 Uploaded {len(result)} documents to index")
    return result

def main():
    print("🚀 Starting indexing pipeline...\n")
    
    create_index()
    chunks = download_and_chunk_documents()
    chunks = generate_embeddings(chunks)
    upload_to_index(chunks)
    
    print("\n🎉 Indexing complete!")

if __name__ == "__main__":
    main()
```

### 4. Update Environment Variables

Add to your `.env` file:

```properties
# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://search-chatbot-[yourname].search.windows.net
AZURE_SEARCH_API_KEY=your-search-admin-key
AZURE_SEARCH_INDEX_NAME=chatbot-knowledge-base
```

### 5. Run the Indexing Script

```bash
python scripts/create_vector_index.py
```

**Expected Output:**
```
🚀 Starting indexing pipeline...

✅ Created index: chatbot-knowledge-base
📄 Processed: company_info.txt
📄 Processed: policies.txt
🧩 Created 7 chunks
🔢 Generated embeddings for 7 chunks
📤 Uploaded 7 documents to index

🎉 Indexing complete!
```

### ✅ Code Checkpoint

You should now have:
- [ ] Azure AI Search service created
- [ ] Vector index with embedded documents
- [ ] `.env` updated with Search credentials

</details>

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.2](./sub-lab-1.2-prepare-knowledge-base.md) | [Next: Sub-Lab 1.4 →](./sub-lab-1.4-create-agent.md)
