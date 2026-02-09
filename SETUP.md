# Setup Guide

This guide helps you set up your development environment for the Code path of the workshop.

---

## 🚀 Choose Your Setup Option

### Option A: GitHub Codespaces (Fastest)

If available in your org/account - no local setup needed:

1. Click the green **"Code"** button on this GitHub repo
2. Select **"Codespaces"** → **"Create codespace on main"**
3. Wait 2-3 minutes - everything is pre-installed!
4. Start with [Lab 1](./lab-1-rag-chatbot/README.md)

> ✅ **Done!** You can skip the rest of this guide if using Codespaces.

---

### Option B: VS Code Local Setup

Follow the steps below to set up your local development environment.

---

## 📋 Prerequisites

Ensure you have installed:

| Tool | Download Link |
|------|---------------|
| **VS Code** | https://code.visualstudio.com/ |
| **Python 3.10+** | https://www.python.org/downloads/ (check "Add Python to PATH" during install) |
| **Git** | https://git-scm.com/download/win |

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/LauraVerghote/Introduction-to-Foundry-workshop.git
cd Introduction-to-Foundry-workshop
```

---

## Step 2: Install VS Code Extensions

Press `Ctrl+Shift+X` and install:

- **Python** (ms-python.python)
- **Jupyter** (ms-toolsai.jupyter)

---

## Step 3: Set Up Lab 1 Environment

In VS Code, open a terminal (`` Ctrl+` ``) and run:

```bash
cd lab-1-rag-chatbot
pip install -r requirements.txt
```

---

## Step 4: Select Python Interpreter

1. Press `Ctrl+Shift+P`
2. Type **"Python: Select Interpreter"**
3. Choose your installed Python version

---

## Step 5: Create Environment File

Create a `.env` file in the `lab-1-rag-chatbot` folder:

```bash
cd lab-1-rag-chatbot
copy .env.example .env
```

You'll fill in the values during Lab 1.

---

## Step 6: Set Up Lab 2 (When Needed)

When you reach Lab 2, run:

```bash
cd lab-2-voice-capabilities
pip install -r requirements.txt
```

---

## ✅ Verification

To verify your setup is working:

```bash
python --version
# Should show Python 3.10 or higher

pip list | grep azure
# Should show azure packages after Lab 1 setup
```

---

## 🔍 Troubleshooting

### Python not found

- Ensure Python is added to PATH
- Restart VS Code after installing Python

### Permission errors on Windows

Run VS Code as Administrator, or use:
```bash
pip install --user -r requirements.txt
```

### Module not found errors

Ensure you're in the correct directory and have activated the right Python interpreter.

---

**You're ready to start!** 🎉 Head to [Lab 1](./lab-1-rag-chatbot/README.md) to begin.
