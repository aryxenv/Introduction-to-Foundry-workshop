# Sub-Lab 1.5: Host Your Agent as a Web App

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.4](./sub-lab-1.4-create-agent.md) | [Next: Lab 2 →](../lab-2-voice-capabilities/README.md)

---

**⏱️ Estimated Time**: 20-30 minutes

## Overview

In this sub-lab, you'll deploy your Foundry agent as a production-ready web application using the [Foundry Agent Web App](https://github.com/microsoft-foundry/foundry-agent-webapp) template. This creates a professional chat interface with authentication, streaming responses, and Azure Container Apps hosting.

---

## 🎓 Key Concepts

### What is the Foundry Agent Web App?

The Foundry Agent Web App is an open-source template that provides:
- **React Frontend**: Modern chat UI with streaming responses
- **ASP.NET Core Backend**: API that connects to your Foundry agent
- **Entra ID Authentication**: Secure user sign-in with MSAL
- **Azure Container Apps**: Serverless hosting with scale-to-zero
- **One-Command Deployment**: `azd up` handles everything

### Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                     Azure Container Apps                          │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                  Foundry Agent Web App                       │  │
│  │  ┌─────────────────┐         ┌─────────────────────────┐    │  │
│  │  │  React Frontend │ ──API──▶│  ASP.NET Core Backend   │    │  │
│  │  │  (Chat UI)      │         │  (Streaming + Auth)     │    │  │
│  │  └─────────────────┘         └───────────┬─────────────┘    │  │
│  └──────────────────────────────────────────│──────────────────┘  │
└─────────────────────────────────────────────│─────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Microsoft Foundry                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Your RAG Agent (from Sub-Lab 1.4)                          │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │ │
│  │  │   GPT-4o    │ ←→ │ Foundry IQ  │ ←→ │ AI Search Index │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### What Gets Deployed

| Resource | Purpose |
|----------|---------|
| **Azure Container Apps** | Hosts the web app (scale-to-zero) |
| **Azure Container Registry** | Stores the container image |
| **Entra ID App Registration** | Handles user authentication |
| **Log Analytics Workspace** | Application logging |
| **RBAC Assignment** | Grants app access to your Foundry agent |

---

## 📋 Prerequisites
> 📝 **First time using the Code option?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.
Before starting this sub-lab, ensure you have:

- ✅ Completed Sub-Lab 1.4 (agent created and tested)
- ✅ Your agent name from Sub-Lab 1.4 (e.g., `RAG-Chatbot`)
- ✅ The following tools installed:

| Tool | Installation |
|------|--------------|
| **PowerShell 7+** | See instructions below |
| **Azure Developer CLI (azd)** | `winget install microsoft.azd` |
| **Azure CLI** | `winget install Microsoft.AzureCLI` |
| **.NET 9 SDK** | https://dot.net |
| **Node.js 18+** | https://nodejs.org |
| **Docker Desktop** (optional) | https://docker.com |

> 💡 **Note**: Docker is optional. If not installed, `azd` automatically uses Azure Container Registry cloud build.

#### Installing PowerShell 7 (Required)

The deployment scripts require PowerShell 7 (`pwsh`). Windows comes with PowerShell 5.1 by default, but you need to install PowerShell 7 separately.

**1. Install PowerShell 7:**

```powershell
winget install Microsoft.PowerShell
```

**2. Close and reopen VS Code** (or your terminal) for `pwsh` to be available in your PATH.

**3. Verify the installation:**

```powershell
pwsh --version
```

You should see output like `PowerShell 7.x.x`. If you get "command not found", restart VS Code again.

---

## 💻 Code Instructions

### Step 1: Create the Web App Folder

Create a `webapp` folder inside the `lab-1-rag-chatbot` directory to hold your web application code:

```powershell
# Navigate to the lab folder
cd c:\Users\lverghote\source\repos\Intro-to-Foundry-workshop\Introduction-to-Foundry-workshop\lab-1-rag-chatbot

# Create the webapp folder
mkdir webapp
cd webapp
```

Your folder structure should now look like:
```
lab-1-rag-chatbot/
├── src/
│   └── rag_agent.py
├── webapp/              # <-- New folder for the web app
│   ├── (files will be added here)
├── data/
├── README.md
└── ...
```

### Step 2: Initialize from the Template

Use the Azure Developer CLI to download the template files (this does NOT create a nested git repo):

```powershell
# Initialize from the template (inside the webapp folder)
azd init -t microsoft-foundry/foundry-agent-webapp

# When prompted for an environment name, enter: rag-chatbot-app
```

This downloads the template files into your `webapp/` folder without any git history conflicts.

---

### Step 3: Configure Your Agent

Set the agent ID to connect to your RAG chatbot from Sub-Lab 1.4:

```powershell
# Set your agent name (the one you created in Sub-Lab 1.4)
azd env set AI_AGENT_ID "RAG-Chatbot"
```

> 💡 **Tip**: If you're unsure of your agent name, check the Foundry portal under **Build** → **Agents**, or run the list script after `azd up`:
> ```powershell
> .\deployment\scripts\list-agents.ps1
> ```

**If you have multiple AI Foundry resources**, you must also specify which one to use. Otherwise the script will pick a random one and fail:

```powershell
# Replace with your actual resource name and resource group from sub-lab 1.1
azd env set AI_FOUNDRY_RESOURCE_NAME "foundry-workshop-[yourname]"
azd env set AI_FOUNDRY_RESOURCE_GROUP "rg-foundry-chatbot-workshop"
```

---

### Step 4: Configure PowerShell Execution Policy (Windows Only)

On Windows, PowerShell scripts are blocked by default. The `azd up` command runs pre-provision hooks that require script execution. If you skip this step, you'll see an error like:

```
ERROR: 'preprovision' hook failed... running scripts is disabled on this system
```

**Fix it by running (in PowerShell):**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

**Or if you're using Git Bash:**

```bash
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
```

This allows locally-created scripts to run while still protecting against unsigned scripts from the internet.

---

### Step 5: Deploy to Azure

Run a single command to deploy everything:

```powershell
azd up
```

**When prompted:**
1. **Select your Azure subscription** - Choose the same subscription where your Foundry resources are deployed
2. **Select a location** - Choose `East US 2` (to match your other resources and important for Lab 2)

This command will:
1. ✅ Create an Entra ID app registration (for authentication)
2. ✅ Discover your AI Foundry resource automatically
3. ✅ Deploy Azure infrastructure (Container Apps, ACR, Log Analytics)
4. ✅ Build and deploy the web application
5. ✅ Configure RBAC so the app can access your agent
6. ✅ Open your browser to the deployed app

**Expected duration**: 10-12 minutes for first deployment

**Expected output:**
```
Packaging services (azd package)

  (✓) Done: Packaging service web
  - Image Tag: ...

Provisioning Azure resources (azd provision)
Provisioning Azure resources can take some time.

  (✓) Done: Resource group: rg-rag-chatbot-app
  (✓) Done: Container Registry
  (✓) Done: Container Apps Environment
  (✓) Done: Container App

SUCCESS: Your application was provisioned and deployed to Azure.

You can view the resources created under the resource group rg-rag-chatbot-app in Azure Portal:
https://portal.azure.com/...

Web endpoint: https://ca-web-xxxxx.azurecontainerapps.io
```

---
### Step 6: Assign Project-Level Permissions

The `azd up` command assigns roles at the Foundry **resource** level, but the web app also needs the `Cognitive Services User` role at the **project** level to invoke agents.

**Get the web app's managed identity:**

```powershell
azd env get-values | Select-String "WEB_IDENTITY_PRINCIPAL_ID"
```

**Assign the role at project level:**

```powershell
# Replace the placeholders with your actual values:
# - [principal-id]: The value from above (e.g., 0530fde3-8bd4-4d25-abb7-c73195c59411)
# - [your-subscription-id]: Your Azure subscription ID
# - [yourname]: Your name suffix from sub-lab 1.1

az role assignment create `
  --role "Cognitive Services User" `
  --assignee [principal-id] `
  --scope "/subscriptions/[your-subscription-id]/resourceGroups/rg-foundry-chatbot-workshop/providers/Microsoft.CognitiveServices/accounts/foundry-workshop-[yourname]/projects/my-first-chatbot"
```

> **⏱️ Note:** Role assignments can take 1-2 minutes to propagate.

---

### Step 7: Test Your Deployed App

**Get your deployed URL:**

If your browser didn't open automatically, you can get the URL with:

```powershell
azd env get-values | Select-String "WEB_ENDPOINT"
```

**Test the app:**

1. Open the URL in your browser
2. Sign in with your Microsoft account
3. You should see a chat interface connected to your RAG agent
4. Try asking questions about your knowledge base:
   - "What products does TechCorp offer?"
   - "What is the return policy?"
   - "How can I contact support?"

The responses should be the same as when you tested in the Foundry portal, but now in a professional web interface!

---


## 🧹 Cleanup

> ⚠️ **Planning to continue to Lab 2?** Skip this section for now! The resources created here are reused in Lab 2.

When you're ready to remove all Azure resources created by this sub-lab, run:

```powershell
azd down --force --purge
```

This will:
- Delete the resource group and all resources
- Remove the Entra app registration
- Clean up RBAC assignments

---

## ✅ Checkpoint

You should now have:
- [ ] Foundry Agent Web App template cloned
- [ ] Agent ID configured
- [ ] App deployed to Azure Container Apps
- [ ] Working chat interface at your deployment URL
- [ ] Successfully tested with your RAG knowledge base

---

## 🎉 Congratulations!

You've successfully deployed your RAG chatbot as a production web application! Your agent is now:

- 🌐 Accessible via a public URL
- 🔒 Secured with Entra ID authentication
- 📊 Monitored with Log Analytics
- ⚡ Automatically scaling based on demand

---

## 📚 Additional Resources

- [Foundry Agent Web App Repository](https://github.com/microsoft-foundry/foundry-agent-webapp)
- [Azure Developer CLI Documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Azure Container Apps Documentation](https://learn.microsoft.com/azure/container-apps/)

---

## ➡️ Next Steps

Ready to add voice capabilities to your chatbot? Continue to:

**[Lab 2: Voice Capabilities →](../lab-2-voice-capabilities/README.md)**

---

[← Back to Lab 1 Overview](./README.md) | [← Previous: Sub-Lab 1.4](./sub-lab-1.4-create-agent.md) | [Next: Lab 2 →](../lab-2-voice-capabilities/README.md)
