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
> 📝 **First time using Code path?** Make sure you've completed the [Setup Guide](../SETUP.md) before continuing.
Before starting this sub-lab, ensure you have:

- ✅ Completed Sub-Lab 1.4 (agent created and tested)
- ✅ Your agent name from Sub-Lab 1.4 (e.g., `RAG-Chatbot`)
- ✅ The following tools installed:

| Tool | Installation |
|------|--------------|
| **PowerShell 7+** | `winget install Microsoft.PowerShell` |
| **Azure Developer CLI (azd)** | `winget install microsoft.azd` |
| **Azure CLI** | `winget install Microsoft.AzureCLI` |
| **.NET 9 SDK** | https://dot.net |
| **Node.js 18+** | https://nodejs.org |
| **Docker Desktop** (optional) | https://docker.com |

> 💡 **Note**: Docker is optional. If not installed, `azd` automatically uses Azure Container Registry cloud build.

---

## 💻 Code Instructions

### Step 1: Clone the Template

```powershell
# Create a new directory for the web app
cd c:\Users\lverghote\source\repos

# Initialize from the template
azd init -t microsoft-foundry/foundry-agent-webapp

# When prompted, enter an environment name (e.g., "rag-chatbot-app")
```

**Or clone directly:**

```powershell
git clone https://github.com/microsoft-foundry/foundry-agent-webapp.git
cd foundry-agent-webapp
```

---

### Step 2: Configure Your Agent

Set the agent ID to connect to your RAG chatbot from Sub-Lab 1.4:

```powershell
# Set your agent name (the one you created in Sub-Lab 1.4)
azd env set AI_AGENT_ID "RAG-Chatbot"
```

> 💡 **Tip**: If you're unsure of your agent name, check the Foundry portal under **Build** → **Agents**, or run the list script after `azd up`:
> ```powershell
> .\deployment\scripts\list-agents.ps1
> ```

---

### Step 3: Deploy to Azure

Run a single command to deploy everything:

```powershell
azd up
```

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

### Step 4: Test Your Deployed App

1. Your browser should automatically open to the deployed URL
2. Sign in with your Microsoft account
3. You should see a chat interface connected to your RAG agent
4. Try asking questions about your knowledge base:
   - "What products does TechCorp offer?"
   - "What is the return policy?"
   - "How can I contact support?"

The responses should be the same as when you tested in the Foundry portal, but now in a professional web interface!

---

### Step 5: (Optional) Run Locally for Development

For local development and testing:

```powershell
# Start both frontend and backend
.\deployment\scripts\start-local-dev.ps1
```

**Local URLs:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080

**Hot Reload:**
- React changes update instantly in the browser
- C# changes auto-compile on save

---

### Step 6: (Optional) Update and Redeploy

When you make code changes:

```powershell
# Deploy code changes only (faster than azd up)
azd deploy
```

**Expected duration**: 3-5 minutes

---

## 🔧 Configuration Options

### Change the Agent

To switch to a different agent:

```powershell
# List available agents
.\deployment\scripts\list-agents.ps1

# Set a different agent
azd env set AI_AGENT_ID "My-Other-Agent"

# Redeploy (no infrastructure changes needed)
azd deploy
```

### Change the AI Foundry Resource

If you have multiple AI Foundry resources:

```powershell
# Manually set the resource
azd env set AI_FOUNDRY_RESOURCE_GROUP "my-resource-group"
azd env set AI_FOUNDRY_RESOURCE_NAME "my-foundry-resource"

# Re-provision to update RBAC
azd provision
```

---

## 🔍 Troubleshooting

### Common Issues

**Issue**: "AI_AGENT_ID required" error

**Solution**:
```powershell
azd env set AI_AGENT_ID "Your-Agent-Name"
azd up
```

---

**Issue**: Authentication fails after deployment

**Solution**:
- Clear browser cache and cookies
- Try an incognito/private window
- Verify Entra app redirect URIs include your deployment URL

---

**Issue**: Agent not responding

**Solution**:
- Check the agent exists in Foundry portal
- Verify the agent name matches exactly (case-sensitive)
- Check Container App logs in Azure Portal

---

**Issue**: Deployment fails

**Solution**:
```powershell
# Check deployment status
az deployment sub show -n <deployment-name>

# View Container App logs
az containerapp logs show -n <app-name> -g <resource-group>
```

---

## 🧹 Cleanup

To remove all Azure resources created by this sub-lab:

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
