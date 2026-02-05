# Troubleshooting Guide

Common issues and their solutions for the workshop.

## General Issues

### Python Environment Issues

**Issue**: `ModuleNotFoundError` when running scripts

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

**Issue**: Python version incompatibility

**Solution**:
```bash
# Check Python version
python --version

# Should be 3.9 or higher
# If not, install correct version and recreate venv
python3.10 -m venv venv
```

## Lab 1 Issues

### Azure OpenAI Connection

**Issue**: `AuthenticationError` when connecting to Azure OpenAI

**Solutions**:
1. Verify API key is correct in `.env` file
2. Check endpoint URL format: `https://your-resource.openai.azure.com/`
3. Ensure no extra spaces in `.env` values
4. Verify Azure OpenAI resource is in correct region
5. Check if API key has been regenerated

---

**Issue**: `DeploymentNotFound` error

**Solution**:
```bash
# Verify deployment names in Azure Portal
# Update .env with exact deployment names
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4-deployment  # Must match exactly
```

### Azure AI Search

**Issue**: `ResourceNotFoundError` for search index

**Solutions**:
1. Verify index name matches in `.env`
2. Check if ingestion script ran successfully
3. Verify admin key (not query key) is used
4. Check search service pricing tier supports your usage

---

**Issue**: No search results returned

**Solutions**:
1. Verify documents were ingested:
   ```bash
   python src/document_processor.py
   python scripts/ingest_documents.py
   ```
2. Check index contains documents in Azure Portal
3. Ensure embedding model is same for indexing and querying
4. Verify search endpoint URL is correct

### Document Processing

**Issue**: Documents not being processed

**Solutions**:
1. Check file formats are supported (.txt, .md)
2. Verify files exist in `data/knowledge_base/`
3. Check file permissions
4. Look for encoding issues (use UTF-8)

---

**Issue**: Chunks are too large or too small

**Solution**:
```python
# Adjust chunk size in .env
CHUNK_SIZE=500        # Try 300-1000
CHUNK_OVERLAP=50      # Try 20-100
```

### API Issues

**Issue**: FastAPI server won't start

**Solutions**:
1. Check if port 8000 is already in use:
   ```bash
   # Linux/macOS
   lsof -i :8000
   
   # Windows
   netstat -ano | findstr :8000
   ```
2. Use a different port:
   ```bash
   uvicorn src.api:app --port 8001
   ```

---

**Issue**: CORS errors in browser

**Solution**:
Already configured in `api.py`, but if issues persist:
```python
# Update CORS settings in api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Lab 2 Issues

### Microphone Access

**Issue**: "Permission denied" for microphone

**Solutions**:
1. Check browser permissions:
   - Chrome: chrome://settings/content/microphone
   - Firefox: about:preferences#privacy
2. Use HTTPS (required by browsers)
3. Try a different browser
4. Check system microphone permissions

---

**Issue**: No audio input detected

**Solutions**:
1. Verify microphone is working (test in system settings)
2. Select correct input device in browser
3. Check microphone isn't muted
4. Close other apps using microphone

### Azure Speech Service

**Issue**: Speech recognition fails

**Solutions**:
1. Verify Speech Service key and region:
   ```bash
   # Test with Azure CLI
   az cognitiveservices account show \
     --name speech-chatbot-workshop \
     --resource-group rg-foundry-chatbot-workshop
   ```
2. Check audio format compatibility
3. Verify language setting matches audio
4. Test with sample audio file first

---

**Issue**: Text-to-speech not working

**Solutions**:
1. Verify voice name is correct and available in region
2. Check audio output device
3. Test with simple text first
4. Verify Speech Service quota not exceeded

---

**Issue**: High latency in voice responses

**Solutions**:
1. Use streaming recognition instead of batch
2. Choose closer Azure region
3. Optimize RAG retrieval (reduce chunk count)
4. Cache common responses
5. Check network latency

### Audio Issues

**Issue**: Distorted or poor quality audio

**Solutions**:
1. Check audio format settings:
   ```python
   AUDIO_FORMAT=riff-24khz-16bit-mono-pcm
   ```
2. Reduce background noise
3. Use better quality microphone
4. Adjust sample rate if needed

---

**Issue**: Audio playback not working

**Solutions**:
1. Check browser audio permissions
2. Verify audio format is supported by browser
3. Check volume settings
4. Test with different audio file

## Deployment Issues

### Docker

**Issue**: Docker build fails

**Solutions**:
1. Check Dockerfile syntax
2. Ensure all dependencies are in requirements.txt
3. Verify base image is accessible
4. Check Docker daemon is running

---

**Issue**: Container won't start

**Solutions**:
1. Check logs:
   ```bash
   docker logs <container_id>
   ```
2. Verify environment variables are set
3. Check port conflicts
4. Ensure resources are sufficient

### Azure AI Foundry Deployment

**Issue**: Deployment fails

**Solutions**:
1. Verify Azure CLI is authenticated:
   ```bash
   az account show
   ```
2. Check that your project and hub exist
3. Verify all connections are configured
4. Check resource quotas
5. Review deployment logs in Azure AI Foundry portal

---

**Issue**: Service not accessible

**Solutions**:
1. Check deployment status in Azure AI Foundry portal
2. Verify health check is passing
3. Check networking configuration
4. Verify endpoint URL is correct
5. Check authentication settings

## Performance Issues

### Slow Response Times

**Solutions**:
1. Reduce number of retrieved chunks (TOP_K_RESULTS)
2. Use faster embedding model
3. Implement caching for common queries
4. Optimize vector search settings
5. Use GPT-3.5 instead of GPT-4 for simple queries

---

### High Costs

**Solutions**:
1. Monitor token usage
2. Implement response caching
3. Use appropriate model for task (don't always use GPT-4)
4. Set reasonable max_tokens limits
5. Batch embedding generation
6. Use free tiers where possible during development

## Development Tips

### Debugging

**Enable detailed logging**:
```python
# In your .env
LOG_LEVEL=DEBUG

# Or in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Test components independently**:
```bash
# Test document processing alone
python src/document_processor.py

# Test RAG agent alone
python src/rag_agent.py

# Test API endpoints individually
curl http://localhost:8000/api/health
```

**Use interactive notebooks**:
```bash
jupyter notebook notebooks/explore_rag.ipynb
```

### Common Mistakes

1. **Forgetting to activate virtual environment**
   - Always activate before running scripts

2. **Not updating .env file**
   - Copy .env.example to .env
   - Fill in all required values

3. **Using wrong API keys**
   - Don't mix up OpenAI keys with Azure OpenAI keys
   - Use admin key for Azure AI Search, not query key

4. **Not committing .gitignore**
   - Ensure .env is in .gitignore
   - Never commit API keys

5. **Port already in use**
   - Check for other running services
   - Use different port if needed

## Getting Additional Help

If issues persist:

1. **Check official documentation**
   - Azure: https://learn.microsoft.com/en-us/azure/
   - Azure AI Foundry: https://learn.microsoft.com/en-us/azure/ai-foundry/

2. **Review error messages carefully**
   - Often contain specific guidance
   - Search for exact error message

3. **Ask instructor**
   - Provide error messages
   - Describe what you've tried
   - Share relevant code snippets

4. **Community resources**
   - Stack Overflow
   - GitHub Issues
   - Azure Forums

## Reporting Issues

When reporting issues, include:

1. **Environment details**
   - OS and version
   - Python version
   - Package versions

2. **Steps to reproduce**
   - What you did
   - What you expected
   - What actually happened

3. **Error messages**
   - Full error output
   - Relevant log files
   - Stack traces

4. **What you've tried**
   - Solutions attempted
   - Results of troubleshooting

---

**Remember**: Most issues have simple solutions. Work through this guide systematically, and don't hesitate to ask for help!
