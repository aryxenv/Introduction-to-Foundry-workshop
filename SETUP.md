# Setup Guide

This guide helps you set up your development environment for the Code path of the workshop.

---

## VS Code Local Setup

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

1. Go to VS Code, create an empty project. 
2. Open a terminal window (view -> Terminal) 
3. Open a git bash terminal. ('+'sign on the top right of the terminal window) 
4. Go to the desired file location ( `cd [location]` )
4. Execute the command below to clone the repo

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

1. Executing the code below to create a `.env` file in the `lab-1-rag-chatbot` folder (make sure you are still in folder **lab-1-rag-chatbot**)

```bash
copy .env.example .env
```

You'll fill in the values during Lab 1.

---

## Step 6: Set Up Lab 2 (When Needed)

If you are planning on doing Lab 2 as well. Go back to the main folder (`cd ..`) and run:

```bash
cd lab-2-voice-capabilities
pip install -r requirements.txt
```

---

## ✅ Verification

To verify your setup is working (make sure your terminal is a git bash one)

```bash
python --version
# Should show Python 3.10 or higher

pip list | grep azure
# Should show azure packages after Lab 1 setup
```

---

**You're ready to start!** 🎉 Head to [Lab 1](./lab-1-rag-chatbot/README.md) to begin.
