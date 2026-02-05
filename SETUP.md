# VS Code Local Setup Guide

This guide will help you set up your local development environment for the Azure AI Foundry Workshop using Visual Studio Code.

## Prerequisites

Before you begin, ensure you have:
- Windows 10/11, macOS 10.15+, or Linux
- Administrative/sudo access on your machine
- Internet connection
- At least 5GB of free disk space

## Step 1: Install Required Software

### 1.1 Install Visual Studio Code

**Windows:**
1. Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Run the installer
3. Check "Add to PATH" during installation

**macOS:**
1. Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Open the .dmg file
3. Drag VS Code to Applications folder
4. Add to PATH:
   ```bash
   cat << EOF >> ~/.bash_profile
   # Add Visual Studio Code (code)
   export PATH="\$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
   EOF
   source ~/.bash_profile
   ```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code
```

### 1.2 Install Python 3.10 or 3.11

**Windows:**
1. Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

**macOS:**
Using Homebrew (recommended):
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Verify
python3 --version
pip3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
python3 --version
pip3 --version
```

### 1.3 Install Git

**Windows:**
1. Download from [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Run installer with default options
3. Verify: `git --version`

**macOS:**
```bash
# Install via Homebrew
brew install git

# Or use Xcode Command Line Tools
xcode-select --install
```

**Linux:**
```bash
sudo apt update
sudo apt install git
```

### 1.4 Install Azure CLI

**Windows:**
1. Download MSI installer from [https://aka.ms/installazurecliwindows](https://aka.ms/installazurecliwindows)
2. Run the installer
3. Restart terminal
4. Verify: `az --version`

**macOS:**
```bash
brew install azure-cli
az --version
```

**Linux:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az --version
```

### 1.5 Install Docker (Optional but Recommended)

**Windows:**
1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Run installer
3. Start Docker Desktop
4. Verify: `docker --version`

**macOS:**
1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Install and start Docker Desktop
3. Verify: `docker --version`

**Linux:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Restart terminal or logout/login
docker --version
```

## Step 2: Install VS Code Extensions

Open VS Code and install these extensions:

### Required Extensions

1. **Python** (ms-python.python)
   - Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
   - Search for "Python"
   - Click "Install"

2. **Pylance** (ms-python.vscode-pylance)
   - Search for "Pylance"
   - Click "Install"

3. **Jupyter** (ms-toolsai.jupyter)
   - Search for "Jupyter"
   - Click "Install"

### Recommended Extensions

4. **Azure Account** (ms-vscode.azure-account)
5. **Azure Tools** (ms-vscode.vscode-node-azure-pack)
6. **Docker** (ms-azuretools.vscode-docker)
7. **YAML** (redhat.vscode-yaml)
8. **GitLens** (eamodio.gitlens)

**Quick Install via Command Palette:**

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Extensions: Install Extensions"
3. Paste this command in VS Code terminal:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension ms-vscode.azure-account
code --install-extension ms-azuretools.vscode-docker
code --install-extension redhat.vscode-yaml
code --install-extension eamodio.gitlens
```

## Step 3: Clone the Workshop Repository

```bash
# Navigate to your preferred directory
cd ~/Documents  # or C:\Users\YourName\Documents on Windows

# Clone the repository
git clone https://github.com/LauraVerghote/Introduction-to-Foundry-workshop.git

# Open in VS Code
cd Introduction-to-Foundry-workshop
code .
```

## Step 4: Set Up Python Environment

### 4.1 Create Virtual Environment for Lab 1

```bash
# Navigate to Lab 1
cd lab-1-rag-chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 4.2 Configure VS Code Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `lab-1-rag-chatbot/venv`

### 4.3 Set Up Lab 2 Environment

```bash
# Navigate to Lab 2
cd ../lab-2-voice-capabilities

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Configure Azure CLI

```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "Your-Subscription-Name"

# Install Azure ML extension
az extension add --name ml
```

## Step 6: Configure Environment Variables

### 6.1 Lab 1 Configuration

```bash
cd lab-1-rag-chatbot

# Copy example env file
cp .env.example .env

# Edit .env file with your credentials
# On Windows: notepad .env
# On macOS: open .env
# On Linux: nano .env or vim .env
```

### 6.2 Lab 2 Configuration

```bash
cd ../lab-2-voice-capabilities

# Copy example env file
cp .env.example .env

# Edit .env file
```

## Step 7: Verify Installation

Run this verification script to check all installations:

```bash
# Create verification script
cat << 'EOF' > verify-setup.sh
#!/bin/bash

echo "🔍 Verifying Workshop Setup..."
echo ""

# Check Python
if command -v python &> /dev/null; then
    echo "✅ Python: $(python --version)"
else
    echo "❌ Python: Not found"
fi

# Check pip
if command -v pip &> /dev/null; then
    echo "✅ pip: $(pip --version | cut -d' ' -f1-2)"
else
    echo "❌ pip: Not found"
fi

# Check Git
if command -v git &> /dev/null; then
    echo "✅ Git: $(git --version)"
else
    echo "❌ Git: Not found"
fi

# Check Azure CLI
if command -v az &> /dev/null; then
    echo "✅ Azure CLI: $(az --version | head -n1)"
else
    echo "❌ Azure CLI: Not found"
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo "✅ Docker: $(docker --version)"
else
    echo "⚠️  Docker: Not found (optional)"
fi

# Check VS Code
if command -v code &> /dev/null; then
    echo "✅ VS Code: $(code --version | head -n1)"
else
    echo "❌ VS Code: Not found"
fi

echo ""
echo "📦 Checking Python packages in Lab 1..."
cd lab-1-rag-chatbot
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
pip list | grep -E "fastapi|semantic-kernel|azure-search|openai" || echo "⚠️  Some packages may be missing"
deactivate 2>/dev/null

echo ""
echo "✅ Verification complete!"
EOF

chmod +x verify-setup.sh
./verify-setup.sh
```

**On Windows (PowerShell):**

```powershell
# Create verification script
@'
Write-Host "🔍 Verifying Workshop Setup..." -ForegroundColor Cyan
Write-Host ""

# Check Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python: $(python --version)" -ForegroundColor Green
} else {
    Write-Host "❌ Python: Not found" -ForegroundColor Red
}

# Check pip
if (Get-Command pip -ErrorAction SilentlyContinue) {
    $pipVersion = pip --version
    Write-Host "✅ pip: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "❌ pip: Not found" -ForegroundColor Red
}

# Check Git
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "✅ Git: $(git --version)" -ForegroundColor Green
} else {
    Write-Host "❌ Git: Not found" -ForegroundColor Red
}

# Check Azure CLI
if (Get-Command az -ErrorAction SilentlyContinue) {
    Write-Host "✅ Azure CLI: Installed" -ForegroundColor Green
} else {
    Write-Host "❌ Azure CLI: Not found" -ForegroundColor Red
}

# Check Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker: $(docker --version)" -ForegroundColor Green
} else {
    Write-Host "⚠️  Docker: Not found (optional)" -ForegroundColor Yellow
}

# Check VS Code
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "✅ VS Code: Installed" -ForegroundColor Green
} else {
    Write-Host "❌ VS Code: Not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ Verification complete!" -ForegroundColor Green
'@ | Out-File -FilePath verify-setup.ps1 -Encoding UTF8

powershell -ExecutionPolicy Bypass -File verify-setup.ps1
```

## Troubleshooting Common Issues

### Python not found in PATH

**Windows:**
1. Search for "Environment Variables" in Start menu
2. Edit "Path" under User variables
3. Add Python installation directory (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python310`)

**macOS/Linux:**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="/usr/local/bin:$PATH"
```

### Virtual environment activation fails

**Windows:**
If you get execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
Ensure the script is executable:
```bash
chmod +x venv/bin/activate
```

### Azure CLI login issues

1. Clear Azure CLI cache:
   ```bash
   az account clear
   az login
   ```

2. Use device code authentication:
   ```bash
   az login --use-device-code
   ```

### pip install fails

1. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```

2. If SSL errors occur:
   ```bash
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```

## VS Code Recommended Settings

Create `.vscode/settings.json` in the workshop root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/lab-1-rag-chatbot/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/venv": true
  },
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

## Next Steps

1. ✅ All software installed
2. ✅ VS Code extensions installed
3. ✅ Repository cloned
4. ✅ Virtual environments created
5. ✅ Azure CLI configured
6. ✅ Environment variables configured

**You're ready to start!** 🎉

Head to [Lab 1](../lab-1-rag-chatbot/README.md) to begin building your RAG chatbot!

## Getting Help

- Check the [troubleshooting guide](../resources/troubleshooting.md)
- Review [Azure AI Foundry Guide](../resources/azure-ai-foundry-guide.md)
- Ask your workshop instructor

---

**Quick Start Commands:**

```bash
# Activate Lab 1 environment
cd lab-1-rag-chatbot
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start working
code README.md
```
