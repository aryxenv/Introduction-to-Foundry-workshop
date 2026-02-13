# Sub-Lab 1.2: Prepare Your Knowledge Base

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.1](./sub-lab-1.1-setup-azure-resources.md) | [Next: Sub-Lab 1.3 →](./sub-lab-1.3-create-vector-index.md)

---

**⏱️ Estimated Time**: 10-15 minutes

## Overview

In this sub-lab, you'll upload your documents to Azure Blob Storage. These documents become the knowledge base that your chatbot can search and reference when answering questions.

---

## 🎓 Key Concepts

### What is Azure Blob Storage?

Azure Blob Storage is Microsoft's object storage solution for the cloud:
- **Blobs**: Binary Large Objects - any type of file
- **Containers**: Logical groupings of blobs (like folders)
- **Storage Account**: Top-level namespace for your data

### Why Blob Storage for RAG?

1. **Scalable**: Handle any amount of documents
2. **Integrated**: Works seamlessly with Azure AI Search
3. **Secure**: Fine-grained access control
4. **Cost-effective**: Pay only for what you store

### Sample Documents

The `data/knowledge_base/` folder contains sample documents:

| File | Contents |
|------|----------|
| `company_info.txt` | Company name, founding date, products, contact info |
| `policies.txt` | Return policy, shipping options, support channels |

---

## Resources You'll Create

- **Storage Account**: For storing your documents
- **Blob Container**: Organized storage for knowledge base files
- **Documents**: Sample files for the chatbot to learn from

---

## 🖥️ Option: Portal

<details>
<summary><strong>Click to expand Portal instructions</strong></summary>

> ✏️ **Replace [yourname]** with your actual name or identifier (e.g., `jsmith`) throughout these instructions. Use the same value you chose in sub-lab 1.1.

### 1. Create a Storage Account

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Storage accounts" → Click "Create"

   <img src="images/storage-account-1.png" width="800"/>

3. Configure:
   - **Resource group**: `rg-foundry-workshop-[yourname]`
   - **Storage account name**: `stchatbot[yourname]` (must be globally unique, lowercase, no special characters)
   - **Region**: East US 2
   - **Performance**: Standard
   - **Redundancy**: Locally-redundant storage (LRS)
4. Click "Review + Create" → "Create"

   <img src="images/storage-account-2.png" width="500"/>

### 2. Create a Blob Container

1. Go to your new storage account (Click "Go to resource")
2. In the left menu, click "Containers" under "Data storage"
3. Click "+ Container"
4. Configure:
   - **Name**: `knowledge-base-container`
   - **Anonymous access level**: Private
5. Click "Create"

   <img src="images/storage-account-3.png" width="1000"/>

### 3. Upload Your Documents

1. Click on your `knowledge-base-container`

> ⚠️ **Warning: Permissions Error?**
>
> If you see: *"You do not have permissions to list the data using your user account with Microsoft Entra ID..."*
>
> <img src="images/storage-account-4.png" width="1000"/>
>
> **Solution - Grant yourself data plane permissions:**
>
> 1. Go to **Access Control (IAM)** on your storage account
> 2. Click **Add** → **Add role assignment**
> 3. Choose role: **"Storage Blob Data Owner"**
> 4. Press **Next**
> 5. Select **"User, group, or service principal"**
> 6. Click **"Select members"** → Select yourself
> 7. Click **Review + assign** (twice)
>
> Log out and back in, then retry the upload.

2. Click "Upload"
3. Select files from the `data/knowledge_base/` folder:
   - `company_info.txt`
   - `policies.txt`
4. Click "Upload"

   <img src="images/storage-account-5.png" width="1000"/>


### ✅ Portal Checkpoint

You should now have:
- [ ] Storage account: `stchatbot[yourname]`
- [ ] Container: `knowledge-base-container`
- [ ] Uploaded documents (company_info.txt, policies.txt)

</details>

---

## 💻 Option: Code

<details>
<summary><strong>Click to expand Code instructions</strong></summary>

> 📝 **First time using the Code option?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.

### 1. Install Dependencies

```bash
pip install azure-storage-blob azure-identity python-dotenv
```

### 2. Create Storage Account via CLI

> ✏️ Copy the code below into a text editor, **replace `[yourname]`** with your actual name, then run the commands. Storage account names must be under 24 characters.

```bash
# Create storage account
az storage account create \
  --name stchatbot[yourname] \
  --resource-group rg-foundry-workshop-[yourname] \
  --location eastus2 \
  --sku Standard_LRS

# Create container
az storage container create \
  --name knowledge-base-container \
  --account-name stchatbot[yourname] \
  --auth-mode login
```

> ✅ **What you just created:**
> - **Storage Account** (`stchatbot[yourname]`): A cloud storage service that holds your files. Think of it as a hard drive in Azure.
> - **Blob Container** (`knowledge-base-container`): A folder-like structure inside the storage account where your documents will be stored. This is where your chatbot's knowledge base lives.

### 3. Grant Yourself Data Permissions

> ⚠️ **Important**: You need the **Storage Blob Data Contributor** role to upload files using Azure Identity.

> ✏️ **Use a PowerShell terminal for this step**. Replace `[yourname]` with your actual name.

```powershell
# Make sure you're logged in first
az login

# Get your user object ID
$USER_OBJECT_ID = az ad signed-in-user show --query id -o tsv

# Get your subscription ID
$SUBSCRIPTION_ID = az account show --query id -o tsv

# Verify variables are set
Write-Host "USER_OBJECT_ID: $USER_OBJECT_ID"
Write-Host "SUBSCRIPTION_ID: $SUBSCRIPTION_ID"

# Assign Storage Blob Data Contributor role (single line command)
az role assignment create --role "Storage Blob Data Contributor" --assignee-object-id $USER_OBJECT_ID --assignee-principal-type User --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/rg-foundry-workshop-[yourname]/providers/Microsoft.Storage/storageAccounts/stchatbot[yourname]"
```

> 💡 **Note**: Role assignments can take a few minutes to propagate. If you still get permission errors, wait 2-3 minutes and try again.

### 4. Upload Documents Programmatically

Create a folder `scripts` under lab-1-rag-chatbot. in this folder create the following file: `upload_to_blob.py`

```python
"""
Upload documents to Azure Blob Storage
"""
import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "knowledge-base-container")
DATA_FOLDER = Path(__file__).parent.parent / "data" / "knowledge_base"

def upload_documents():
    """Upload all documents from data/knowledge_base to Azure Blob Storage"""
    
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)
    
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    
    # Create container if it doesn't exist
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
            blob_client = container_client.get_blob_client(file_path.name)
            
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            print(f"📤 Uploaded: {file_path.name}")
            uploaded_count += 1
    
    print(f"\n🎉 Successfully uploaded {uploaded_count} documents!")
    return uploaded_count

if __name__ == "__main__":
    upload_documents()
```

### 5. Update Environment Variables

Add to your `.env` file:

```properties
# Azure Storage Configuration
AZURE_STORAGE_ACCOUNT_NAME=stchatbot[yourname]
AZURE_STORAGE_CONTAINER_NAME=knowledge-base-container
```

### 6. Run the Upload Script
Make sure you are in the lab-1-rag-chatbot folder. If not: `cd lab-1-rag-chatbot`

```bash
python scripts/upload_to_blob.py
```

**Expected Output:**
```
📁 Container already exists: knowledge-base-container
📤 Uploaded: company_info.txt
📤 Uploaded: policies.txt

🎉 Successfully uploaded 2 documents!
```

### ✅ Code Checkpoint

You should now have:
- [ ] Storage account created
- [ ] Container with uploaded documents
- [ ] `.env` updated with storage credentials

</details>

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.1](./sub-lab-1.1-setup-azure-resources.md) | [Next: Sub-Lab 1.3 →](./sub-lab-1.3-create-vector-index.md)
