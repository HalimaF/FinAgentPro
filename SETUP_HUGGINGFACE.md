# 🤖 Connect Hugging Face AI to FinAgent Pro

## Quick Setup (5 Minutes)

### Step 1: Get Your Free Hugging Face Token

1. **Visit** https://huggingface.co/settings/tokens
2. **Sign in** or create a free account (takes 1 minute)
3. **Click** "New token"
   - Name: `FinAgent Pro`
   - Type: `Read` (default)
4. **Copy** the token (starts with `hf_...`)

### Step 2: Add Token to Your Project

Open `d:\Fintech\backend\.env` and replace this line:
```
HUGGINGFACE_API_TOKEN=your_token_will_go_here
```

With your actual token:
```
HUGGINGFACE_API_TOKEN=hf_YourActualTokenHere
```

**Example:**
```
HUGGINGFACE_API_TOKEN=hf_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
```

### Step 3: Install Dependencies

```powershell
cd d:\Fintech\backend

# Activate virtual environment
.venv\Scripts\activate

# Install Hugging Face libraries
pip install -r requirements-huggingface.txt
```

This installs:
- ✅ `transformers` - Core Hugging Face library
- ✅ `sentence-transformers` - Text embeddings
- ✅ `requests` - API client
- ✅ `pillow` - Image processing

### Step 4: Start Backend with Real AI

```powershell
cd d:\Fintech\backend

# Make sure DEMO_MODE=0 in .env file (check with notepad)
# Start server
python -m uvicorn main:app --reload
```

You should see:
```
✅ HuggingFace service initialized with API token
✅ Models ready: FinBERT, LayoutLMv3, Zephyr-7B, BART, MiniLM
```

### Step 5: Test Your AI Connection

Open a **new terminal** and test:

```powershell
# Test 1: Health check
curl http://localhost:8000/api/v1/agents/health

# Test 2: Smart chat with real AI
curl http://localhost:8000/api/v1/agents/smart/chat -X POST -H "Content-Type: application/json" -d "{\"query\":\"Analyze my spending patterns\"}"

# Test 3: Receipt analysis
curl http://localhost:8000/api/v1/agents/smart/analyze-receipt -X POST -H "Content-Type: application/json" -d "{\"image_path\":\"test.jpg\"}"
```

---

## 🎯 What You Get with Hugging Face AI

### 5 AI Models (All Included FREE):

1. **FinBERT** (ProsusAI/finbert)
   - Financial sentiment analysis
   - Fraud detection signals
   - Market context understanding

2. **LayoutLMv3** (microsoft/layoutlmv3-base)
   - Receipt OCR and extraction
   - Invoice parsing
   - Document understanding

3. **Zephyr-7B** (HuggingFaceH4/zephyr-7b-beta)
   - Natural language queries
   - Conversational AI
   - Financial advice

4. **BART** (facebook/bart-large-cnn)
   - Financial insights summarization
   - Trend analysis
   - Report generation

5. **MiniLM** (sentence-transformers/all-MiniLM-L6-v2)
   - Smart expense categorization
   - Similarity matching
   - Semantic search

### API Limits (Free Tier):
- ✅ **5000 requests/month**
- ✅ **No credit card required**
- ✅ **All 5 models included**

---

## 🚀 Alternative: Quick Demo Mode

If you want to test the UI without setting up Hugging Face:

```powershell
cd d:\Fintech\backend

# Set demo mode
set DEMO_MODE=1

# Start server (instant, no API keys needed)
python -m uvicorn main:app --reload
```

Demo mode gives simulated AI responses - perfect for UI testing and demos!

---

## 🔧 Troubleshooting

### Error: "Invalid Hugging Face token"
- Check token starts with `hf_`
- Verify no spaces before/after in `.env` file
- Regenerate token at https://huggingface.co/settings/tokens

### Error: "Model loading failed"
- Make sure you installed dependencies: `pip install -r requirements-huggingface.txt`
- Check internet connection (models access API)
- Try setting `DEMO_MODE=1` as fallback

### Error: "Rate limit exceeded"
- Free tier: 5000 calls/month
- Wait for reset or switch to `DEMO_MODE=1`
- Consider upgrading to Hugging Face Pro ($9/month for 100K calls)

### Backend won't start
```powershell
# Check Python environment
cd d:\Fintech\backend
.venv\Scripts\activate
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt
pip install -r requirements-huggingface.txt

# Check .env file exists
dir .env

# Try demo mode first
set DEMO_MODE=1
python -m uvicorn main:app --reload
```

---

## 📊 Verify AI is Working

Once backend is running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/agents/health

In API docs, try the `/agents/smart/chat` endpoint:
```json
{
  "query": "What's my biggest expense category?"
}
```

You should get AI-powered responses using real Hugging Face models!

---

## 🎯 Quick Reference

| Setup | Time | Requirements | AI Quality |
|-------|------|--------------|------------|
| **Demo Mode** | 10 seconds | None | Simulated ⭐⭐⭐ |
| **HuggingFace API** | 5 minutes | Free token | Real AI ⭐⭐⭐⭐⭐ |
| **Local Models** | 30 minutes | 2GB download | Offline ⭐⭐⭐⭐ |

**For Hackathon**: Use HuggingFace API mode (5 minutes, real AI, impressive demos!)

---

## ✅ Done!

Your FinAgent Pro now has:
- ✅ Real AI-powered financial analysis
- ✅ Natural language understanding
- ✅ Smart receipt OCR
- ✅ Fraud detection with sentiment analysis
- ✅ Conversational queries
- ✅ 5 production-grade models

**Next Steps:**
1. Start frontend: `cd d:\Fintech\frontend && npm run dev`
2. Test Voice Assistant: http://localhost:5173/voice
3. Run demo scripts: `cd d:\Fintech\demos && python expense_processing_demo.py`

**Questions?** Check `AI_MODELS_SETUP.md` for advanced configuration.
