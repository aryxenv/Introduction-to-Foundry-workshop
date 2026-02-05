#!/bin/bash
set -e

echo "🚀 Setting up Azure AI Foundry Workshop environment..."

# Update pip
python -m pip install --upgrade pip

# Install Azure CLI ML extension
echo "📦 Installing Azure CLI ML extension..."
az extension add --name ml --yes

# Install Lab 1 dependencies
echo "📦 Installing Lab 1 dependencies..."
cd /workspaces/Introduction-to-Foundry-workshop/lab-1-rag-chatbot
pip install -r requirements.txt

# Install Lab 2 dependencies
echo "📦 Installing Lab 2 dependencies..."
cd /workspaces/Introduction-to-Foundry-workshop/lab-2-voice-capabilities
pip install -r requirements.txt

# Install common development tools
echo "📦 Installing development tools..."
pip install black pylint pytest ipykernel

# Create .env templates if they don't exist
echo "📝 Creating .env template files..."
cd /workspaces/Introduction-to-Foundry-workshop/lab-1-rag-chatbot
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created lab-1-rag-chatbot/.env - Please fill in your Azure credentials"
fi

cd /workspaces/Introduction-to-Foundry-workshop/lab-2-voice-capabilities
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created lab-2-voice-capabilities/.env - Please fill in your Azure credentials"
fi

# Set up git
echo "🔧 Configuring git..."
git config --global core.autocrlf input

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your Azure credentials in .env files"
echo "2. Run 'az login' to authenticate with Azure"
echo "3. Start with Lab 1: cd lab-1-rag-chatbot && code README.md"
echo ""
echo "🎉 Happy coding!"
