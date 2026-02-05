#!/bin/bash
# Quick setup script for Azure AI Foundry Workshop
# Works on macOS and Linux

set -e

echo "🚀 Azure AI Foundry Workshop - Quick Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
echo "🔍 Checking Python installation..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.10 or higher.${NC}"
    exit 1
fi

# Check pip
echo "🔍 Checking pip installation..."
if command_exists pip3; then
    echo -e "${GREEN}✅ pip found${NC}"
else
    echo -e "${RED}❌ pip not found. Installing...${NC}"
    python3 -m ensurepip --upgrade
fi

# Check Git
echo "🔍 Checking Git installation..."
if command_exists git; then
    echo -e "${GREEN}✅ Git found${NC}"
else
    echo -e "${RED}❌ Git not found. Please install Git.${NC}"
    exit 1
fi

# Check Azure CLI
echo "🔍 Checking Azure CLI installation..."
if command_exists az; then
    echo -e "${GREEN}✅ Azure CLI found${NC}"
else
    echo -e "${YELLOW}⚠️  Azure CLI not found.${NC}"
    read -p "Install Azure CLI? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew install azure-cli
        else
            # Linux
            curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
        fi
    fi
fi

echo ""
echo "📦 Setting up Lab 1..."
cd lab-1-rag-chatbot

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing Lab 1 dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Created .env file. Please configure with your Azure credentials.${NC}"
fi

deactivate
cd ..

echo ""
echo "📦 Setting up Lab 2..."
cd lab-2-voice-capabilities

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing Lab 2 dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Created .env file. Please configure with your Azure credentials.${NC}"
fi

deactivate
cd ..

# Install Azure CLI ML extension
if command_exists az; then
    echo ""
    echo "📦 Installing Azure CLI ML extension..."
    az extension add --name ml --yes 2>/dev/null || echo "ML extension already installed or failed to install"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "📋 Next steps:"
echo "1. Configure your Azure credentials in .env files:"
echo "   - lab-1-rag-chatbot/.env"
echo "   - lab-2-voice-capabilities/.env"
echo ""
echo "2. Login to Azure:"
echo "   az login"
echo ""
echo "3. Start Lab 1:"
echo "   cd lab-1-rag-chatbot"
echo "   source venv/bin/activate"
echo "   code README.md"
echo ""
echo "🎉 Happy coding!"
