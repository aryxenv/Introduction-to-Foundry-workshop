# Quick setup script for Azure AI Foundry Workshop
# Works on Windows with PowerShell

Write-Host "🚀 Azure AI Foundry Workshop - Quick Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check Python
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.10 or higher from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Red
    exit 1
}

# Check pip
Write-Host "🔍 Checking pip installation..." -ForegroundColor Yellow
if (Test-Command pip) {
    Write-Host "✅ pip found" -ForegroundColor Green
} else {
    Write-Host "❌ pip not found. Trying to install..." -ForegroundColor Red
    python -m ensurepip --upgrade
}

# Check Git
Write-Host "🔍 Checking Git installation..." -ForegroundColor Yellow
if (Test-Command git) {
    Write-Host "✅ Git found" -ForegroundColor Green
} else {
    Write-Host "❌ Git not found. Please install Git from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# Check Azure CLI
Write-Host "🔍 Checking Azure CLI installation..." -ForegroundColor Yellow
if (Test-Command az) {
    Write-Host "✅ Azure CLI found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Azure CLI not found." -ForegroundColor Yellow
    $response = Read-Host "Install Azure CLI? (y/n)"
    if ($response -eq 'y') {
        Write-Host "Downloading Azure CLI installer..." -ForegroundColor Yellow
        $installerUrl = "https://aka.ms/installazurecliwindows"
        $installerPath = "$env:TEMP\AzureCLI.msi"
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
        Start-Process msiexec.exe -Wait -ArgumentList "/I $installerPath /quiet"
        Remove-Item $installerPath
        Write-Host "✅ Azure CLI installed. Please restart your terminal." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "📦 Setting up Lab 1..." -ForegroundColor Cyan
Set-Location lab-1-rag-chatbot

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing Lab 1 dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "⚠️  Created .env file. Please configure with your Azure credentials." -ForegroundColor Yellow
}

deactivate
Set-Location ..

Write-Host ""
Write-Host "📦 Setting up Lab 2..." -ForegroundColor Cyan
Set-Location lab-2-voice-capabilities

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing Lab 2 dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "⚠️  Created .env file. Please configure with your Azure credentials." -ForegroundColor Yellow
}

deactivate
Set-Location ..

# Install Azure CLI ML extension
if (Test-Command az) {
    Write-Host ""
    Write-Host "📦 Installing Azure CLI ML extension..." -ForegroundColor Cyan
    az extension add --name ml --yes 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ML extension already installed or failed to install" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Configure your Azure credentials in .env files:"
Write-Host "   - lab-1-rag-chatbot\.env"
Write-Host "   - lab-2-voice-capabilities\.env"
Write-Host ""
Write-Host "2. Login to Azure:"
Write-Host "   az login"
Write-Host ""
Write-Host "3. Start Lab 1:"
Write-Host "   cd lab-1-rag-chatbot"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   code README.md"
Write-Host ""
Write-Host "🎉 Happy coding!" -ForegroundColor Green
