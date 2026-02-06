# Lab 1: Building a RAG-Enabled Chatbot

## 🎯 Lab Overview

In this lab, you'll build a chatbot with Retrieval-Augmented Generation (RAG) capabilities using the Microsoft Agent Framework and deploy it on Microsoft Foundry. By the end of this lab, you'll have a production-ready chatbot hosted on Microsoft's unified AI platform that can answer questions based on your custom knowledge base.

**Estimated Time**: 40 minutes

> **Prerequisites**: Make sure you've completed the [Setup Guide](../SETUP.md) before starting this lab.

## 📖 What You'll Learn

- **RAG Fundamentals**: Understanding how RAG combines retrieval and generation
- **Azure AI Search**: Working with embeddings and semantic search on Azure
- **Foundry IQ**: Using Foundry IQ for knowledge base management and indexing
- **Microsoft Agent Framework**: Building intelligent agents with Semantic Kernel
- **Microsoft Foundry Deployment**: Hosting and scaling AI applications on Microsoft's unified platform

## 🏗️ Architecture Overview

### What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that enhances Large Language Models (LLMs) by providing them with relevant context from a knowledge base. Instead of relying solely on the model's training data, RAG:

1. **Retrieves** relevant information from your documents
2. **Augments** the user's query with this context
3. **Generates** accurate, contextually-aware responses

### System Architecture

```
User Query → Embedding → Vector Search → Relevant Context
                                              ↓
                               LLM (with context) → Response
```

### Microsoft Services Used

| Component | Microsoft Service | Purpose |
|-----------|------------------|---------|
| **AI Platform** | Microsoft Foundry | Unified platform for building, deploying, and managing AI applications |
| **Knowledge Base** | Foundry IQ | Automatic indexing, chunking, and retrieval of your documents |
| **Document Storage** | Azure Blob Storage | Stores your source documents (PDFs, text files, etc.) |
| **Vector Search** | Azure AI Search | Stores embeddings and performs semantic search |
| **Embedding Model** | Azure OpenAI (text-embedding-ada-002) | Converts text into numerical vectors |
| **LLM** | Azure OpenAI (GPT-4) | Generates natural language responses |
| **Agent Orchestration** | Microsoft Agent Framework | Coordinates the RAG workflow and tool calling |

### How It All Fits Together

1. **Microsoft Foundry** is your central hub - it's where you create your project, manage models, and deploy your agent
2. **Azure Blob Storage** is where you upload your source documents (company policies, FAQs, product info, etc.)
3. **Foundry IQ** handles your knowledge base - it reads from Blob Storage and automatically chunks, embeds, and indexes your documents
4. **Azure AI Search** powers the vector database behind Foundry IQ
5. **Azure OpenAI** provides both the embedding model (for search) and the LLM (for responses)
6. **Microsoft Agent Framework** is the SDK you use to build the agent logic in Python

## 📋 Prerequisites

Before starting, ensure you have:

- [ ] Completed the [Setup Guide](../SETUP.md)
- [ ] Azure subscription with credits
- [ ] Access to Microsoft Foundry (included with Azure subscription)

## 🛠️ Step-by-Step Instructions

### Step 1: Set Up Microsoft Foundry Resources (20 minutes)

<details>
<summary><strong>Option A: Using Azure Portal (Recommended for Beginners)</strong></summary>

1. **Create a Resource Group**
   - Go to [Azure Portal](https://portal.azure.com)
   - Click "Resource groups" → "Create"
      <td><img src="images/resource-group-console-1.png" width="800"/>

      <td><img src="images/resource-group-console-2.png" width="800"/> 

   - Name: `rg-foundry-chatbot-workshop`
   - Region: Choose closest to you
   - Click "Review + Create" and then "Create".
      <td><img src="images/resource-group-console-3.png" width="500"/>

2. **Create Microsoft Foundry Resource**
   - Search for "Microsoft Foundry"
   - Click "Create a resource"
      <td><img src="images/foundry-resource-1.png" width="500"/>

   - Select your resource group
   - Name: `foundry-workshop-`+ unique differentiator
   - Region: East US
   - Default project name: `my-first-chatbot`
   - Click "Review + Create" and then "Create"
      <td><img src="images/foundry-resource-2.png" width="500"/>

3. **Deploy Models**
   - Go to the Foundry resource you just created by either clicking 'Go to resource'' or searching Microsoft foundry and going to all resources and clicking the newply created resource.
   - Click "Go to Foundry portal".
   - Select the new FOundry experience by toggling the box next to New Foundry:
      <td><img src="images/new-foundry.png" width="800"/>

    - when being prompted to select a project to continue select the "my-first-chatbot" that we just created and click "Let's go".
      <td><img src="images/select-project.png" width="500"/>

   - Go to the Discovery tab in Foundry
      <td><img src="images/foundry-models-1.png" width="800"/>
   - Click Models on the left tab. 
   - Search for the gpt-4o model
   - Click on the model
      <td><img src="images/foundry-models-2.png" width="800"/>

   - Create a new deployment by clicking Deploy and then "Default settings"
      <td><img src="images/foundry-models-2.png" width="800"/>

   - Do the same thing for the embeddings model (Discover -> models -> **text-embedding-3-small** -> Deploy -> Default settings)



</details>

<details>
<summary><strong>Option B: Using Azure CLI (For Advanced Users) - TO DO</strong></summary>

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-foundry-chatbot-workshop --location eastus

# Create Azure OpenAI
az cognitiveservices account create \
  --name openai-chatbot-workshop \
  --resource-group rg-foundry-chatbot-workshop \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Create Azure AI Search
az search service create \
  --name search-chatbot-workshop \
  --resource-group rg-foundry-chatbot-workshop \
  --sku free
```

</details>

### Step 2: Configure Environment Variables - TO DO

After completing either Option A or B above, configure your environment:

Create a `.env` file in the `lab-1-rag-chatbot` directory:

```bash
# Copy the template
cp .env.example .env
```

Edit `.env` with your Azure credentials:

```properties
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4-deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your-search-admin-key
AZURE_SEARCH_INDEX_NAME=chatbot-knowledge-base

# Application Configuration
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
```

**Important**: Never commit `.env` file to version control!

### Step 3: Understanding the Code Structure (15 minutes) - TO DO

Let's examine the project structure:

```
lab-1-rag-chatbot/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── document_processor.py  # Document ingestion
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # Vector database operations
│   ├── rag_agent.py           # RAG chatbot logic
│   └── api.py                 # FastAPI application
├── data/
│   └── knowledge_base/        # Your documents go here
├── tests/
│   └── test_rag_agent.py     # Unit tests
├── notebooks/
│   └── explore_rag.ipynb     # Interactive exploration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── Dockerfile                # Container configuration
└── README.md                 # This file
```

**Key Concepts to Understand:**

1. **Document Processor**: Converts documents (PDF, TXT, etc.) into chunks suitable for embedding
2. **Embeddings**: Numerical representations of text that capture semantic meaning
3. **Vector Store**: Database optimized for similarity search on embeddings
4. **RAG Agent**: Orchestrates retrieval and generation using Semantic Kernel
5. **API**: Exposes chatbot functionality via REST endpoints

### Step 4: Build the Document Processing Pipeline (30 minutes)

Before RAG can work, we need to get your documents into a searchable format. There are **three different approaches** you can choose from:

| Option | Approach | Best For |
|--------|----------|----------|
| **Option A** | Upload documents via Azure Portal and index from the console | Quick setup, minimal code |
| **Option B** | Programmatically upload to Blob Storage and index via API | Automated pipelines, CI/CD  |
| **Option C** | Create embeddings programmatically and store in Azure AI Search | Full control, learning the details |

Choose the option that best fits your learning goals and proceed with the corresponding section below.

---

<details>
<summary><strong>Option A: Upload Documents via Azure Portal (Quickest Setup)</strong></summary>

   This option uses the Azure Portal to upload documents to Blob Storage and create a vector index directly from the Foundry console. Ideal for quick prototyping.

   #### Create a Storage Account

   1. **Navigate to Azure Portal**
      - Go to [Azure Portal](https://portal.azure.com)
      - Search for "Storage accounts" and click "Create"

         <td><img src="images/storage-account-1.png" width="800"/>

   2. **Configure Storage Account**
      - Resource group: `rg-foundry-chatbot-workshop`
      - Storage account name: `stchatbotworkshop[yourname]` (must be globally unique, lowercase, no special characters)
      - Region: Same as your other resources (e.g., East US)
      - Preferred storage type: Azure Blob Storage or Azure Data Lake Storage Gen 2
      - Performance: Standard
      - Redundancy: Locally-redundant storage (LRS)
      - Click "Review + Create" then "Create"

         <td><img src="images/storage-account-2.png" width="500"/>

   3. **Create a Blob Container**
      - Go to your new storage account (Click on "Go to resource" when the Deployment is complete)
      - In the left menu, click "Containers" under "Data storage"
      - Click "+ Add Container"
      - Name: `knowledge-base-container`
      - Public access level / Anonymous access level: Private
      - Click "Create"

         <td><img src="images/storage-account-3.png" width="1000"/>

   #### Upload Your Documents

   1. **Prepare Your Documents**
      - Use the sample documents from `data/knowledge_base/` folder
      - Or create your own `.txt`, `.pdf`, or `.docx` files

   2. **Upload via Portal**
      - Click on your `knowledge-basecontainer` container
      - Click "Upload"
      - Select your files (`company_info.txt`, `policies.txt`)
      - Click "Upload"
         <td><img src="images/storage-account-5.png" width="1000"/>



> ⚠️ **Warning**
>
> **If you get an error like this when accessing the container:**
>
> *You do not have permissions to list the data using your user account with Microsoft Entra ID. Click to learn more about authenticating with Microsoft Entra ID. This request is not authorized to perform this operation using this permission. RequestId:XXXX Time:XXXX.*
>
> <img src="images/storage-account-4.png" width="1000"/>
>
> A company policy might prevent you from using storage account key access. In that case you should give yourself data plane permissions on the storage account in order to upload data:
>
> 1. Go to **Access Control (IAM)**
> 2. Click **Add** → **Add role assignment**
> 3. Choose the role **"Storage Blob Data Owner"**
> 4. Press **Next**
> 5. Select **"User, group, or service principal"**
> 6. Click **"Select members"**
> 7. Select yourself
> 8. Click **Review + assign**
> 9. Click **Review + assign** again
>
> Go back to overview in your container. You may need to log in and out to refresh. Now execute the instructions above.

   #### Create Azure AI Search Service
   1. **Navigate to Azure Portal**
   - Go back to [Azure Portal](https://portal.azure.com)
   - Search for "Azure AI Search" in the top bar
   - Click "Create"
      <td><img src="images/ai-search-1.png" width="800"/>

   2. **Configure AI Search**
   - Resource group: Select existing `rg-foundry-chatbot-workshop`
   - Name: `search-chatbot-workshop-[yourname]` (must be globally unique)
   - Region: East US
   - Pricing tier: Free (sufficient for workshop, but not production-grade)
   - Click "Review + Create" and then "Create"
      <td><img src="images/ai-search-2.png" width="500"/>

   3. **Ensure your AI Search had sufficient permissions to your data**
   - When your deployment is ready go back to your storage account -> container
   - Go to access control (IAM)
   - Click Add -> Add role assignment
   - Select the role: Storage Blob Data Reader
   - Click "Next"
   - Select "Managed identity"
   - Click 'Select members"
   - Under managed identity choose 'Search service'
   - Select the search service we just created: `search-chatbot-workshop-[yourname]`
   - Click "select"
       <td><img src="images/storage-account-6" width="500"/>  

   - Click "Review + assign" and then again "Review + assign"

   4. **Ensure your AI Search had sufficient permissions to use your embeddings model**
   - Go to your Foundry resource we created
   - Go to access control (IAM)
   - Click Add -> Add role assignment
       <td><img src="images/sfoundry-resource-3" width="1000"/>     
   - Select the role: Cognitive Services OpenAI User
   - Click "Next"
   - Select "Managed identity"
   - Click 'Select members"
   - Under managed identity choose 'Search service'
   - Select the search service we just created: `search-chatbot-workshop-[yourname]`
   - Click "select"
       <td><img src="images/storage-account-6" width="500"/>  

   - Click "Review + assign" and then again "Review + assign"

   5. **Import Data into the index**
   - Go back to your AI search resource and click "Import data (new)". 
      <td><img src="images/ai-search-3.png" width="800"/>

   - Choose Azure Blob Storage
   - Choose RAG
   - Choose the storage account we just created: `stchatbotworkshop[yourname]`
   - Pick the container we created: `knowledge-base-container`
   - Click next
   - Kind: Azure AI Foundry (Preview) / Microsoft Foundry. 
   - Azure AI Foundry / Hub project: Select the one we created (my-first-chatbot (foundry-workshop-lv))
   - Model deployment: the one we deployed together (text-embedding-3-small)
   - Click the checkbox next to "I acknowledge ..."
   - Click "Next"
   - Click "Next" 
   - Click "Next" 
   - Click "Create"

   . **Navigate to Foundry Portal**
      - Go to [Microsoft Foundry](https://ai.azure.com)
      - Select your project (`my-first-chatbot`)

   2. **Create a New Index**
      - In the left navigation, click "Indexes" under "Data"
      - Click "+ New index"
      - Select "Azure Blob Storage" as the data source

   3. **Configure the Data Source**
      - Connection: Create new or select existing connection to your storage account
      - Container: `knowledge-base`
      - Click "Next"

   4. **Configure Index Settings**
      - Index name: `chatbot-knowledge-base`
      - Embedding model: Select your deployed `text-embedding-3-small` model
      - Chunking strategy: Auto (or configure custom settings)
      - Click "Create"

   5. **Wait for Indexing**
      - The indexing process will take a few minutes
      - You can monitor progress in the "Indexes" section
      - Once complete, you'll see the document count and status

   #### Verify Your Index

   1. **Test the Index**
      - Click on your index name
      - Use the "Search" feature to test queries
      - Try: "What products does TechCorp offer?"
      - Verify that relevant chunks are returned

   **Expected Result:**
   - Index shows 7+ documents indexed
   - Search returns relevant results for your test queries

</details>

---

<details>
<summary><strong>Option B: Programmatic Blob Upload and Indexing (For Automation) - TO DO </strong></summary>

This option demonstrates how to automate the entire pipeline: upload files to Blob Storage and create/update the vector index programmatically. Ideal for CI/CD pipelines and production scenarios.

#### B.1 Install Additional Dependencies

Add the Azure Storage SDK to your environment:

```bash
pip install azure-storage-blob azure-identity
```

#### B.2 Create the Upload Script

Create a new file `scripts/upload_to_blob.py`:

```python
"""
Programmatic upload of documents to Azure Blob Storage
"""
import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# Configuration
STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "knowledge-base")
DATA_FOLDER = Path(__file__).parent.parent / "data" / "knowledge_base"

def upload_documents():
    """Upload all documents from data/knowledge_base to Azure Blob Storage"""
    
    # Create blob service client using DefaultAzureCredential
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)
    
    # Get or create container
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    try:
        container_client.create_container()
        print(f"✅ Created container: {CONTAINER_NAME}")
    except Exception as e:
        if "ContainerAlreadyExists" in str(e):
            print(f"📁 Container already exists: {CONTAINER_NAME}")
        else:
            raise e
    
    # Upload each file
    uploaded_count = 0
    for file_path in DATA_FOLDER.glob("*"):
        if file_path.is_file() and file_path.suffix in ['.txt', '.pdf', '.docx', '.md']:
            blob_name = file_path.name
            blob_client = container_client.get_blob_client(blob_name)
            
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            print(f"📤 Uploaded: {blob_name}")
            uploaded_count += 1
    
    print(f"\n🎉 Successfully uploaded {uploaded_count} documents to Blob Storage!")
    return uploaded_count

if __name__ == "__main__":
    upload_documents()
```

#### B.3 Create the Indexing Script

Create a new file `scripts/create_vector_index.py`:

```python
"""
Programmatically create and populate a vector index in Azure AI Search
from documents stored in Azure Blob Storage
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
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "knowledge-base")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

def create_index():
    """Create the vector search index"""
    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(SEARCH_ENDPOINT, credential)
    
    # Define the index schema
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
    print(f"✅ Created/updated index: {result.name}")
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
        
        # Simple chunking
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
    """Generate embeddings for each chunk using Azure OpenAI"""
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
    print("🚀 Starting programmatic indexing pipeline...\n")
    
    # Step 1: Create/update the index
    create_index()
    
    # Step 2: Download and chunk documents
    chunks = download_and_chunk_documents()
    
    # Step 3: Generate embeddings
    chunks = generate_embeddings(chunks)
    
    # Step 4: Upload to index
    upload_to_index(chunks)
    
    print("\n🎉 Indexing pipeline complete!")

if __name__ == "__main__":
    main()
```

#### B.4 Update Environment Variables

Add these variables to your `.env` file:

```properties
# Azure Storage Configuration (for Option B)
AZURE_STORAGE_ACCOUNT_NAME=stchatbotworkshop[yourname]
AZURE_STORAGE_CONTAINER_NAME=knowledge-base
```

#### B.5 Run the Pipeline

Execute the scripts in order:

```bash
# Step 1: Upload documents to Blob Storage
python scripts/upload_to_blob.py

# Step 2: Create index and populate with embeddings
python scripts/create_vector_index.py
```

**Expected Output:**
```
🚀 Starting programmatic indexing pipeline...

✅ Created/updated index: chatbot-knowledge-base
📄 Processed: company_info.txt
📄 Processed: policies.txt
🧩 Created 7 chunks
🔢 Generated embeddings for 7 chunks
📤 Uploaded 7 documents to index

🎉 Indexing pipeline complete!
```

#### B.6 Verify in Azure Portal

1. Go to your Azure AI Search service
2. Click on "Indexes"
3. Verify `chatbot-knowledge-base` shows 7 documents
4. Use the "Search explorer" to test queries

</details>

---

<details>
<summary><strong>Option C: Create Your Own Embeddings Programmatically (Full Control) - TO DO </strong></summary>

   This option gives you full control over the embedding and indexing process. You'll understand exactly how documents are processed, chunked, embedded, and stored.

   #### C.1 Understanding Document Processing

   Before RAG can work, we need to:
   1. Load documents from various formats
   2. Split them into manageable chunks
   3. Create embeddings for each chunk
   4. Store embeddings in the vector database

   #### C.2 Review `document_processor.py`

   Open `src/document_processor.py` and review the code:

   ```python
   # Key function: process_document
   # - Reads a file
   # - Splits into chunks (500 chars with 50 char overlap)
   # - Preserves metadata (filename, page number)
   ```

   **Why chunking?**
   - LLMs have token limits
   - Smaller chunks = more precise retrieval
   - Overlap ensures context isn't lost at boundaries

   **Optimal chunk size**: 500-1000 characters (adjust based on your data)

   #### C.3 Add Your Knowledge Base

   1. Create sample documents in `data/knowledge_base/`:

   Create `data/knowledge_base/company_info.txt`:
   ```
   About TechCorp

   TechCorp is a leading technology company founded in 2020. We specialize in 
   AI-powered solutions for enterprise customers.

   Our Products:
   - SmartAssist: AI customer service platform
   - DataVision: Business intelligence and analytics
   - CloudSync: Multi-cloud data synchronization

   Contact: support@techcorp.com
   Office Hours: Monday-Friday, 9 AM - 5 PM EST
   ```

   Create `data/knowledge_base/policies.txt`:
   ```
   Company Policies

   Return Policy:
   Products can be returned within 30 days of purchase for a full refund.
   Items must be in original packaging and unused.

   Shipping:
   - Standard shipping: 5-7 business days (Free)
   - Express shipping: 2-3 business days ($15)
   - Overnight: 1 business day ($30)

   Customer Support:
   Email: support@techcorp.com
   Phone: 1-800-TECH-CORP
   Live Chat: Available on website 24/7
   ```

   #### C.4 Test Document Processing

   Run the document processor:

   ```bash
   python src/document_processor.py
   ```

   **Expected Output:**
   ```
   Processing documents from data/knowledge_base/...
   Processed company_info.txt: 3 chunks created
   Processed policies.txt: 4 chunks created
   Total: 7 chunks ready for embedding
   ```

   **Exercise**: Add your own document and observe how it's chunked!

</details>

---

**✅ Checkpoint:** Regardless of which option you chose, you should now have a populated vector index in Azure AI Search with your knowledge base documents. Verify this before proceeding to Step 5.

### Step 5: Create and Store Embeddings (30 minutes)

#### 4.1 Understanding Embeddings

Embeddings are vector representations of text:
- Text → Embedding Model → Dense vector (1536 dimensions for Ada-002)
- Similar meanings = Similar vectors
- Enables semantic search (not just keyword matching)

**Example:**
- "How do I return a product?" 
- "What's your refund policy?"
- These have different words but similar meanings → similar embeddings!

#### 4.2 Generate Embeddings

Review `src/embeddings.py`:

```python
# Uses Azure OpenAI text-embedding-ada-002
# Converts text chunks to 1536-dimensional vectors
# Handles batching for efficiency
```

#### 4.3 Store in Vector Database

Review `src/vector_store.py`:

The vector store:
- Creates an Azure AI Search index
- Uploads document chunks with embeddings
- Enables similarity search

**Index Schema:**
- `id`: Unique identifier
- `content`: Original text chunk
- `embedding`: 1536-dimensional vector
- `metadata`: Source file, page number, etc.

#### 4.4 Run the Ingestion Pipeline

Execute the full pipeline:

```bash
python scripts/ingest_documents.py
```

**What happens:**
1. Loads documents from `data/knowledge_base/`
2. Splits into chunks
3. Generates embeddings via Azure OpenAI
4. Creates/updates Azure AI Search index
5. Uploads all data

**Expected Output:**
```
🔄 Starting document ingestion pipeline...
📄 Found 2 documents to process
🧩 Created 7 text chunks
🔢 Generating embeddings... (using text-embedding-ada-002)
✅ Generated 7 embeddings
📤 Uploading to Azure AI Search...
✅ Successfully indexed 7 documents
🎉 Ingestion complete!
```

**Verification:**
- Go to Azure Portal → Your Search Service → Indexes
- You should see `chatbot-knowledge-base` with 7 documents

### Step 6: Build the RAG Agent (45 minutes)

#### 5.1 Understanding Semantic Kernel

Microsoft Semantic Kernel is an SDK that:
- Orchestrates AI workflows
- Manages prompts and templates
- Handles memory and context
- Integrates with various AI services

**Key Concepts:**
- **Kernel**: Central orchestrator
- **Plugins**: Reusable functions
- **Semantic Functions**: LLM-powered operations
- **Native Functions**: Traditional code
- **Memory**: Context management

#### 5.2 Review the RAG Agent Implementation

Open `src/rag_agent.py` and study the structure:

```python
class RAGChatbot:
    """
    RAG-enabled chatbot using Semantic Kernel
    
    Flow:
    1. User asks a question
    2. Generate embedding for question
    3. Search vector store for relevant chunks
    4. Build prompt with context
    5. Send to LLM
    6. Return response
    """
```

**Key Methods:**

1. **`_retrieve_context(query)`**: 
   - Embeds the user query
   - Searches vector store
   - Returns top-K relevant chunks

2. **`_generate_response(query, context)`**:
   - Creates prompt with context
   - Calls Azure OpenAI
   - Returns generated response

3. **`chat(user_message)`**:
   - Main entry point
   - Orchestrates retrieve + generate

#### 5.3 Understanding the Prompt Template

The prompt is crucial for RAG quality:

```python
PROMPT_TEMPLATE = """
You are a helpful AI assistant. Answer the user's question based on the 
provided context. If the context doesn't contain relevant information, 
acknowledge that and provide a general helpful response.

Context:
{context}

User Question: {query}

Instructions:
- Be concise and accurate
- Cite specific information from the context when possible
- If uncertain, say so
- Be helpful and professional

Answer:
"""
```

**Best Practices:**
- Clear instructions for the model
- Placeholder for context and query
- Guidelines for handling uncertainty
- Tone/style guidance

#### 5.4 Test the RAG Agent

Run the interactive test:

```bash
python scripts/test_chatbot.py
```

**Try these questions:**
1. "What products does TechCorp offer?"
2. "How long do I have to return a product?"
3. "What are your office hours?"
4. "How much is overnight shipping?"

**Expected Output:**
```
🤖 RAG Chatbot Ready!
Type 'quit' to exit

You: What products does TechCorp offer?

🔍 Retrieving relevant context...
Found 2 relevant chunks

💬 Bot: TechCorp offers three main products:
1. SmartAssist - An AI customer service platform
2. DataVision - Business intelligence and analytics
3. CloudSync - Multi-cloud data synchronization

These products are designed for enterprise customers.

You: quit
```

**Exercise**: 
1. Ask a question NOT covered in your documents
2. Observe how the chatbot handles it
3. Add more documents and re-run ingestion
4. Test again with new topics

### Step 7: Create REST API (30 minutes)

#### 6.1 Understanding the API Design

We'll use FastAPI to expose the chatbot:

**Endpoints:**
- `POST /api/chat` - Send a message, get response
- `GET /api/health` - Check service status
- `GET /api/stats` - Usage statistics
- `POST /api/feedback` - Submit feedback (optional)

#### 6.2 Review API Implementation

Open `src/api.py`:

```python
# FastAPI application with:
# - CORS middleware for web clients
# - Request validation with Pydantic
# - Error handling
# - Logging
# - Rate limiting (optional)
```

**Key Components:**

1. **Pydantic Models** (request/response validation):
```python
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    
class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    session_id: str
```

2. **Chat Endpoint**:
```python
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Validate input
    # 2. Call RAG agent
    # 3. Return response with sources
```

#### 6.3 Run the API Locally

Start the FastAPI server:

```bash
uvicorn src.api:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### 6.4 Test the API

**Option 1: Using cURL**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your shipping options?"
  }'
```

**Option 2: Using Python**

```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "What are your shipping options?"}
)
print(response.json())
```

**Option 3: Interactive API Docs**

Visit: `http://localhost:8000/docs`

FastAPI provides automatic interactive documentation:
1. Click on `/api/chat` endpoint
2. Click "Try it out"
3. Enter your message
4. Click "Execute"

**Expected Response:**
```json
{
  "response": "We offer three shipping options: Standard (5-7 business days, free), Express (2-3 business days, $15), and Overnight (1 business day, $30).",
  "sources": ["policies.txt"],
  "session_id": "abc-123"
}
```

### Step 8: Deploy to Microsoft Foundry (45 minutes)

#### 7.1 Understanding Azure AI Foundry

Microsoft Azure AI Foundry is a unified platform for AI development that provides:
- Integrated development environment for AI applications
- Seamless integration with Azure AI services (OpenAI, Speech, Search, etc.)
- Model deployment and management
- Built-in monitoring and evaluation tools
- Prompt flow for orchestrating AI workflows
- Collaborative workspace for teams

**Key Benefits:**
- **Unified Experience**: Single platform for all Azure AI services
- **Rapid Development**: Pre-built templates and components
- **Production Ready**: Built-in scaling, monitoring, and security
- **Cost Effective**: Pay only for what you use
- **Integration**: Works with existing Azure resources

#### 7.2 Set Up Azure AI Foundry Project

**Using Azure Portal:**

1. **Navigate to Azure AI Foundry**
   - Go to [Azure AI Foundry](https://ai.azure.com)
   - Sign in with your Azure account

2. **Create a New Hub**
   - Click "Create hub"
   - Name: `aifoundry-chatbot-workshop`
   - Resource group: `rg-foundry-chatbot-workshop` (same as before)
   - Region: Choose same as your other resources
   - This hub will contain all AI projects and resources
   - Click "Create"

3. **Create a Project**
   - In your hub, click "Create project"
   - Name: `rag-chatbot`
   - Description: "RAG-enabled chatbot with knowledge base"
   - Click "Create"

4. **Connect Your Azure Resources**
   - Go to "Settings" → "Connections"
   - Add connection to Azure OpenAI Service:
     - Connection name: `openai-connection`
     - Select your Azure OpenAI resource
     - Authenticate
   - Add connection to Azure AI Search:
     - Connection name: `search-connection`
     - Select your Azure AI Search resource
     - Authenticate

**Using Azure CLI:**

```bash
# Install Azure AI extension
az extension add --name ml

# Create AI Hub
az ml workspace create \
  --kind hub \
  --name aifoundry-chatbot-workshop \
  --resource-group rg-foundry-chatbot-workshop \
  --location eastus

# Create AI Project
az ml workspace create \
  --kind project \
  --hub-id /subscriptions/{subscription-id}/resourceGroups/rg-foundry-chatbot-workshop/providers/Microsoft.MachineLearningServices/workspaces/aifoundry-chatbot-workshop \
  --name rag-chatbot \
  --resource-group rg-foundry-chatbot-workshop
```

#### 7.3 Deploy Using Prompt Flow

Azure AI Foundry uses Prompt Flow for orchestrating AI applications.

**Option A: Using the Portal (Recommended for Beginners)**

1. **Create a Prompt Flow**
   - In your project, go to "Prompt flow"
   - Click "Create"
   - Choose "Chat flow" template
   - Name: `rag-chatbot-flow`

2. **Configure the Flow**
   - Add a "Vector DB Lookup" node:
     - Connect to your Azure AI Search index
     - Configure to search for relevant documents
   - Add a "LLM" node:
     - Select your Azure OpenAI deployment
     - Configure the prompt template with context
   - Connect nodes: User Input → Vector Search → LLM → Output

3. **Test the Flow**
   - Use the built-in test panel
   - Enter test queries
   - Verify responses are correct

4. **Deploy as Web App**
   - Click "Deploy"
   - Choose "Web app"
   - Configure:
     - Name: `rag-chatbot-webapp`
     - Compute: Standard (F2 or higher)
     - Authentication: Enable (optional)
   - Click "Deploy"

**Option B: Using Python SDK**

Create `deploy_to_foundry.py`:

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment
from azure.identity import DefaultAzureCredential

# Authenticate
credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id="your-subscription-id",
    resource_group_name="rg-foundry-chatbot-workshop",
    workspace_name="rag-chatbot"
)

# Create endpoint
endpoint = ManagedOnlineEndpoint(
    name="rag-chatbot-endpoint",
    description="RAG chatbot endpoint",
    auth_mode="key"
)
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# Create deployment
deployment = ManagedOnlineDeployment(
    name="rag-chatbot-deployment",
    endpoint_name="rag-chatbot-endpoint",
    model="path/to/your/model",  # or use registered model
    instance_type="Standard_DS3_v2",
    instance_count=1
)
ml_client.online_deployments.begin_create_or_update(deployment).result()

print("Deployment complete!")
print(f"Endpoint: {endpoint.scoring_uri}")
```

Run deployment:

```bash
python deploy_to_foundry.py
```

#### 7.4 Alternative: Deploy as Azure Web App

If you prefer a simpler deployment:

1. **Build Docker Image (Optional)**
   
   Review the `Dockerfile`:
   
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application code
   COPY src/ ./src/
   COPY data/ ./data/
   
   ENV PORT=8000
   
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD python -c "import requests; requests.get('http://localhost:8000/api/health')"
   
   CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Deploy to Azure Web App**

   ```bash
   # Create App Service Plan
   az appservice plan create \
     --name chatbot-plan \
     --resource-group rg-foundry-chatbot-workshop \
     --sku B1 \
     --is-linux
   
   # Create Web App
   az webapp create \
     --name rag-chatbot-webapp-[yourname] \
     --resource-group rg-foundry-chatbot-workshop \
     --plan chatbot-plan \
     --runtime "PYTHON:3.10"
   
   # Configure environment variables
   az webapp config appsettings set \
     --name rag-chatbot-webapp-[yourname] \
     --resource-group rg-foundry-chatbot-workshop \
     --settings \
       AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
       AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
       AZURE_SEARCH_ENDPOINT="$AZURE_SEARCH_ENDPOINT" \
       AZURE_SEARCH_API_KEY="$AZURE_SEARCH_API_KEY"
   
   # Deploy code
   az webapp up \
     --name rag-chatbot-webapp-[yourname] \
     --resource-group rg-foundry-chatbot-workshop
   ```

#### 7.5 Configure Azure AI Foundry Monitoring

1. **Enable Application Insights**
   - In Azure AI Foundry project, go to "Settings"
   - Enable Application Insights
   - This automatically tracks:
     - Request rates
     - Response times
     - Error rates
     - Token usage

2. **Set Up Metrics Dashboard**
   - Go to "Monitoring" in AI Foundry
   - Create custom dashboard with:
     - Total requests
     - Average response time
     - Success rate
     - Token consumption
     - Cost tracking

3. **Configure Alerts**
   - Set up alerts for:
     - High error rate (>5%)
     - Slow responses (>10s)
     - High token usage
     - Service downtime

#### 7.6 Verify Deployment

**Using Azure AI Foundry Portal:**

1. Go to your project in AI Foundry
2. Navigate to "Deployments"
3. Click on your deployment
4. Test using the built-in test interface

**Using Command Line:**

```bash
# Get endpoint URL
ENDPOINT_URL=$(az ml online-endpoint show \
  --name rag-chatbot-endpoint \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot \
  --query scoring_uri -o tsv)

# Get API key
API_KEY=$(az ml online-endpoint get-credentials \
  --name rag-chatbot-endpoint \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot \
  --query primaryKey -o tsv)

# Test endpoint
curl -X POST $ENDPOINT_URL \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What products does TechCorp offer?"
  }'
```

**Expected Response:**
```json
{
  "response": "TechCorp offers three main products: SmartAssist (AI customer service platform), DataVision (Business intelligence and analytics), and CloudSync (Multi-cloud data synchronization).",
  "sources": ["company_info.txt"],
  "session_id": "abc-123"
}
```

#### 7.7 Manage and Monitor in Azure AI Foundry

**View Deployment Metrics:**

1. In AI Foundry, go to "Deployments"
2. Select your deployment
3. View real-time metrics:
   - Request count
   - Latency percentiles
   - Error rates
   - Token usage

**View Logs:**

```bash
# Stream logs
az ml online-endpoint get-logs \
  --name rag-chatbot-endpoint \
  --deployment rag-chatbot-deployment \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot \
  --tail 100
```

**Update Deployment:**

```bash
# Update with new code
az ml online-deployment update \
  --name rag-chatbot-deployment \
  --endpoint rag-chatbot-endpoint \
  --resource-group rg-foundry-chatbot-workshop \
  --workspace-name rag-chatbot \
  --set instance_count=2  # Scale up
```

#### 8.5 Deploy Container (Alternative)

```bash
# Deploy container
foundry container deploy \
  --file foundry-deployment.yml \
  --namespace chatbot-workshop

# Check deployment status
foundry container status rag-chatbot-api

# View logs
foundry container logs rag-chatbot-api
```

**Using Foundry UI:**

1. Log into Foundry
2. Navigate to "Workloads" → "Container Workloads"
3. Click "New Container Workload"
4. Upload your Docker image or provide registry URL
5. Configure environment variables from secrets
6. Set resource limits
7. Configure health checks
8. Deploy!

#### 7.6 Verify Deployment

```bash
# Get service URL
foundry container get-url rag-chatbot-api

# Test endpoint
curl https://your-foundry-instance.com/chatbot-workshop/api/health

# Test chat
curl -X POST https://your-foundry-instance.com/chatbot-workshop/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What products do you offer?"}'
```

**Expected**: Should see the same responses as local testing!

### Step 9: Testing and Validation (20 minutes)

#### 9.1 Run Unit Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

#### 9.2 Manual Testing Checklist

Test various scenarios:

- [ ] Simple factual question
- [ ] Multi-part question
- [ ] Question outside knowledge base
- [ ] Ambiguous question
- [ ] Follow-up question
- [ ] Very long query
- [ ] Empty message
- [ ] Special characters

#### 8.3 Performance Testing

```bash
# Simple load test
python scripts/load_test.py --requests 100 --concurrent 10
```

Expected metrics:
- Average response time: < 2 seconds
- P95 response time: < 5 seconds
- Success rate: > 99%

#### 8.4 Monitoring Setup

In Azure AI Foundry:
1. Application Insights is automatically enabled
2. View metrics in the Azure AI Foundry portal:
   - Request count
   - Response time
   - Error rate
   - Token usage
   - Cost tracking
3. Set up alerts in Application Insights:
   - Error rate > 5%
   - Response time > 10s
   - High token usage
   - Deployment failures

### Step 10: Best Practices and Optimization (20 minutes)

#### 9.1 Improving RAG Quality

**Techniques to try:**

1. **Better Chunking**:
   ```python
   # Use semantic chunking instead of fixed size
   # Keep sentences together
   # Add overlap between chunks
   ```

2. **Hybrid Search**:
   ```python
   # Combine vector search with keyword search
   # Use RRF (Reciprocal Rank Fusion) to merge results
   ```

3. **Re-ranking**:
   ```python
   # Use a cross-encoder to re-rank retrieved chunks
   # Improves relevance of top results
   ```

4. **Query Enhancement**:
   ```python
   # Expand query with synonyms
   # Generate hypothetical documents
   # Use LLM to reformulate query
   ```

#### 9.2 Cost Optimization

Monitor and reduce costs:

1. **Caching**:
   ```python
   # Cache frequent queries
   # Cache embeddings
   # Use Redis or similar
   ```

2. **Batch Processing**:
   ```python
   # Process embeddings in batches
   # Reduces API calls
   ```

3. **Model Selection**:
   - Use GPT-3.5 for simple queries
   - Reserve GPT-4 for complex questions
   - Use smaller embedding models if appropriate

#### 9.3 Security Best Practices

- [ ] Never commit API keys
- [ ] Use managed identities where possible
- [ ] Implement rate limiting
- [ ] Add authentication to API
- [ ] Sanitize user inputs
- [ ] Audit data access
- [ ] Encrypt data at rest and in transit

#### 9.4 Error Handling

Implement robust error handling:

```python
try:
    response = await chatbot.chat(user_message)
except RateLimitError:
    # Return 429 with retry-after
except ServiceUnavailable:
    # Return 503 with appropriate message
except InvalidInput:
    # Return 400 with validation errors
except Exception as e:
    # Log error, return 500
    logger.error(f"Unexpected error: {e}")
```

## 🎓 Key Takeaways

Congratulations! You've learned:

- ✅ How RAG works and why it's powerful
- ✅ Building a chatbot with Semantic Kernel
- ✅ Working with Azure AI Search for vector storage
- ✅ Deploying to Azure AI Foundry
- ✅ Best practices for production AI systems

## 🔍 Troubleshooting

### Common Issues

**Issue**: "Authentication failed" when connecting to Azure OpenAI

**Solution**: 
- Verify your API key is correct in `.env`
- Check that your IP isn't blocked in Azure
- Ensure your subscription is active

---

**Issue**: Search returns no results

**Solution**:
- Verify index exists in Azure AI Search
- Check that documents were ingested successfully
- Ensure embedding model is the same for indexing and querying

---

**Issue**: Responses are not relevant

**Solution**:
- Improve document chunking strategy
- Increase number of retrieved chunks (top_k)
- Enhance prompt template
- Try hybrid search

---

**Issue**: Deployment fails in Azure AI Foundry

**Solution**:
- Check deployment logs in Azure AI Foundry portal
- Verify all connections are configured correctly
- Check resource quotas in your subscription
- Ensure your Azure OpenAI and Search services are in compatible regions
- Review Application Insights logs for errors

## 📚 Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Azure AI Search RAG Tutorial](https://learn.microsoft.com/en-us/azure/search/search-get-started-rag)
- [Prompt Flow Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/)
- [RAG Best Practices](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

## ✅ Lab Completion Checklist

Before moving to Lab 2, ensure you have:

- [ ] Successfully set up Azure resources
- [ ] Created Azure AI Foundry project and hub
- [ ] Ingested documents into Azure AI Search
- [ ] Tested RAG chatbot locally
- [ ] Deployed to Azure AI Foundry
- [ ] Verified deployment with test queries
- [ ] Understand the RAG workflow
- [ ] Reviewed best practices

## 🚀 Next Steps

Ready to add voice capabilities? Head over to [Lab 2: Adding Voice Capabilities](../lab-2-voice-capabilities/README.md)!

---

**Questions or Issues?** Check the [resources](../resources/README.md) folder or ask your instructor.
