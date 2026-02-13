# Sub-Lab 2.3: Cleanup Resources

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.2](./sub-lab-2.2-add-voice-to-agent.md)

---

**⏱️ Estimated Time**: 5-10 minutes

## Overview

In this sub-lab, you'll clean up all Azure resources created during Labs 1 and 2. This ensures you don't incur ongoing costs for resources you're no longer using.

> ⚠️ **Warning**: This process is **irreversible**. All data, deployments, and configurations will be permanently deleted.

---

## 🗑️ What Will Be Deleted

### From Lab 1

| Resource | Name |
|----------|------|
| Resource Group | `rg-foundry-workshop-[yourname]` |
| Microsoft Foundry Resource | `foundry-workshop-[yourname]` |
| Foundry Project | `my-first-chatbot` |
| Storage Account | `stchatbot[yourname]` |
| Azure AI Search | `search-chatbot-[yourname]` |
| Model Deployments | Chat model (e.g., `gpt-4.1-mini`) and embedding model (e.g., `text-embedding-3-small`) |

### From Lab 1.5 (Web App)

| Resource | Name |
|----------|------|
| Resource Group | `rg-rag-chatbot-app` (created by azd) |
| Container Apps Environment | Auto-generated |
| Container App | Auto-generated |
| Container Registry | Auto-generated |
| Entra App Registration | Auto-generated |

### From Lab 2

| Resource | Name |
|----------|------|
| Model Deployment | `gpt-realtime` |

---

## 💻 Cleanup Instructions

### Step 1: Clean Up the Web App (Lab 1.5)

First, navigate to your webapp folder and remove all resources created by `azd`:

```powershell
cd lab-1-rag-chatbot/webapp
```

```powershell
# Remove all Azure resources created by azd
azd down --force --purge
```

This will:
- Delete the Container App and Container Apps Environment
- Delete the Container Registry
- Remove the Entra app registration
- Clean up all RBAC assignments

**Expected output:**
```
Deleting all resources and deployed code on Azure (azd down)
...
SUCCESS: Your application was removed from Azure.
```

---

### Step 2: Delete the Main Resource Group (Lab 1 & 2)

Now delete the main resource group containing your Foundry resources, AI Search, Storage, and model deployments:

> ✏️ **Replace `[yourname]`** with your actual name (same as Lab 1.1).

```powershell
# Delete the main resource group (this deletes EVERYTHING inside it)
az group delete `
  --name rg-foundry-workshop-[yourname] `
  --yes `
  --no-wait
```

> 💡 **Note**: The `--no-wait` flag returns immediately while deletion continues in the background. Full deletion takes 2-5 minutes.

---

### Step 3: Verify Cleanup

After a few minutes, verify the resources are deleted:

> ✏️ **Replace `[yourname]`** with your actual name (same as Lab 1.1).

```powershell
# Check if resource group still exists (should return error)
az group show --name rg-foundry-workshop-[yourname]
```

**Expected output** (if cleanup successful):
```
(ResourceGroupNotFound) Resource group 'rg-foundry-workshop-[yourname]' could not be found.
```

---

### Step 4: Clean Up Local Files (Optional)

If you want to remove the local workshop files as well:

```powershell
# Navigate to parent directory
cd ../..

# Remove the webapp folder (created by git clone in Lab 1.5)
Remove-Item -Recurse -Force lab-1-rag-chatbot/webapp
```

---

## 🖥️ Portal Alternative

If you prefer to delete resources via the Azure Portal:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Resource groups**
3. Select `rg-foundry-workshop-[yourname]`
4. Click **Delete resource group**
5. Type the resource group name to confirm
6. Click **Delete**

Repeat for `rg-rag-chatbot-app` (the webapp resource group).

---

## ✅ Cleanup Checklist

| Check | Status |
|-------|--------|
| Web app resources deleted (`azd down`) | ⬜ |
| Main resource group deleted | ⬜ |
| Verified resource group no longer exists | ⬜ |
| Local files cleaned up (optional) | ⬜ |

---

## 🎉 Congratulations!

You've completed the Foundry Workshop! You learned how to:

- ✅ Set up Azure AI Foundry resources
- ✅ Create a knowledge base with Azure Storage
- ✅ Build a vector index with Azure AI Search
- ✅ Create a RAG-powered agent with Foundry IQ
- ✅ Deploy a production web app with authentication
- ✅ Add real-time voice capabilities with GPT Realtime
- ✅ Clean up all resources responsibly

---

## 📚 Continue Learning

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [RAG Pattern Best Practices](https://learn.microsoft.com/azure/ai-services/openai/concepts/retrieval-augmented-generation)
- [GPT Realtime Audio](https://learn.microsoft.com/azure/ai-services/openai/realtime-audio)

---

[← Back to Lab 2 Overview](./README.md) | [← Previous: Sub-Lab 2.2](./sub-lab-2.2-add-voice-to-agent.md) | [Back to Workshop Home →](../README.md)
