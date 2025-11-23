# IBM watsonx Orchestrate Skill Definition

## 📁 File: `finagent_orchestrate_skill.json`

This file contains the complete skill definition for importing FinAgent Pro into IBM watsonx Orchestrate.

---

## 🚀 How to Use This File

### Step 1: Update the Base URL

Before importing, you **MUST** update line 13 with your actual public URL:

**Current (placeholder):**
```json
"baseUrl": "https://YOUR_PUBLIC_URL/"
```

**Replace with your ngrok URL:**
```json
"baseUrl": "https://abc123.ngrok-free.app/"
```

Or your deployed URL:
```json
"baseUrl": "https://finagent-pro.mybluemix.net/"
```

### Step 2: Import to IBM watsonx Orchestrate

1. **Login to IBM watsonx Orchestrate**
   - Go to: https://cloud.ibm.com/
   - Navigate to your watsonx Orchestrate instance

2. **Navigate to Skills**
   - Click "Skills" in the left sidebar
   - Or go to "Build" → "Skills"

3. **Import Skill**
   - Click "Add skill" or "Import skill"
   - Select "Upload file"
   - Choose this file: `finagent_orchestrate_skill.json`
   - Click "Import"

4. **Configure Authentication**
   - Set API key value: `demo_key` (or your custom key)
   - Verify header name: `X-IBM-ORCH-KEY`

5. **Test the Skill**
   - Click "Test" in the skill settings
   - Try the "Smart Chat" action
   - Input: `{"query": "test"}`
   - Should return success response

---

## 📋 What's Included

This skill definition includes **5 actions**:

### 1. Classify Expense
- **Operation ID:** `expense.classify`
- **Purpose:** Extracts and classifies expense receipts using OCR and AI
- **Inputs:**
  - `ocrText` (string, optional) - Receipt text
  - `fileUrl` (string, optional) - Receipt image URL
  - `userId` (string, optional) - User identifier

### 2. Create Invoice
- **Operation ID:** `invoice.create`
- **Purpose:** Creates professional invoices from customer data
- **Inputs:**
  - `customer` (string, required) - Customer name
  - `items` (string, required) - Invoice items description

### 3. Scan Fraud
- **Operation ID:** `fraud.scan`
- **Purpose:** Analyzes transactions for fraud signals
- **Inputs:**
  - `transactions` (string, required) - Transaction data to analyze

### 4. Forecast Cashflow
- **Operation ID:** `cashflow.forecast`
- **Purpose:** Predicts future cashflow based on historical data
- **Inputs:**
  - `days` (integer, optional) - Number of days to forecast

### 5. Smart Chat
- **Operation ID:** `smart.chat`
- **Purpose:** Natural language queries about financial data
- **Inputs:**
  - `query` (string, required) - User question in plain English

---

## 🔐 Authentication

This skill uses **API Key authentication**:

- **Type:** API Key
- **Location:** HTTP Header
- **Header Name:** `X-IBM-ORCH-KEY`
- **Value:** Set in IBM Orchestrate UI (default: `demo_key`)

Make sure your backend `.env` file has:
```bash
IBM_ORCH_API_KEY=demo_key
```

---

## 🧪 Testing

### Test Locally First

Before importing to IBM, test your webhook locally:

```powershell
# Start backend
cd d:\Fintech\backend
set DEMO_MODE=1
python -m uvicorn main:app --reload

# Test webhook
curl -X POST http://localhost:8000/webhooks/ibm-orchestrate `
  -H "Content-Type: application/json" `
  -H "X-IBM-ORCH-KEY: demo_key" `
  -d '{"action": "smart.chat", "payload": {"query": "test"}}'
```

### Test with ngrok

```powershell
# Start ngrok
cd C:\ngrok
.\ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok-free.app)

# Test public URL
curl -X POST https://abc123.ngrok-free.app/webhooks/ibm-orchestrate `
  -H "Content-Type: application/json" `
  -H "X-IBM-ORCH-KEY: demo_key" `
  -d '{"action": "smart.chat", "payload": {"query": "test"}}'
```

### Test in IBM Orchestrate

After importing:
1. Go to your skill in IBM Orchestrate
2. Click "Test" or "Try it out"
3. Select "Smart Chat" action
4. Input: `{"query": "Summarize expenses"}`
5. Click "Run"
6. Should see: `{"status": "ok", "result": {...}}`

---

## 📝 Customization

### Change API Key

Edit line 10:
```json
"valuePlaceholder": "${IBM_ORCH_API_KEY}"
```

Or set directly in IBM Orchestrate UI after import.

### Add More Actions

To add more actions, follow this template:
```json
{
  "name": "Your Action Name",
  "operationId": "your.action",
  "purpose": "Description of what this does",
  "http": {
    "method": "POST",
    "path": "webhooks/ibm-orchestrate"
  },
  "payload": {
    "action": "your.action",
    "payload": {
      "param1": "${param1}"
    }
  },
  "inputs": [
    { "name": "param1", "type": "string", "required": true }
  ]
}
```

Then add the handler in `backend/main.py`:
```python
if action in {"your.action"}:
    # Your logic here
    return {"status": "ok", "result": {...}}
```

---

## 🐛 Troubleshooting

### "Invalid schema" error
- Check JSON syntax (use https://jsonlint.com/)
- Verify all required fields are present
- Ensure proper escaping of special characters

### "Connection failed" error
- Verify baseUrl is correct and accessible
- Check ngrok is still running (URL doesn't change)
- Test URL manually with curl
- Check firewall settings

### "Authentication failed" error
- Verify API key matches in IBM Orchestrate and backend
- Check header name is exactly `X-IBM-ORCH-KEY`
- Ensure backend is checking the header correctly

### "Action not found" error
- Verify action name matches webhook handler
- Check request payload format
- Review backend logs for actual error

---

## 📚 Related Files

- **Webhook Handler:** `../../backend/main.py` (lines 141-182)
- **Test Script:** `../tools/test-ibm-webhook.ps1`
- **HTTP Examples:** `../tools/ibm-webhook.http`
- **Setup Guide:** `../../IBM_WATSONX_SETUP_GUIDE.md`

---

## ✅ Quick Checklist

Before importing to IBM Orchestrate:
- [ ] Backend is running
- [ ] ngrok tunnel is active (or app is deployed)
- [ ] Public URL is accessible (test with curl)
- [ ] `baseUrl` in JSON is updated with your URL
- [ ] API key is set in backend `.env`
- [ ] All 5 actions tested locally

After importing:
- [ ] Skill appears in IBM Orchestrate
- [ ] Authentication is configured
- [ ] Test action executes successfully
- [ ] Backend logs show IBM requests
- [ ] Screenshots captured for hackathon

---

## 🏆 For Hackathon Judges

This skill definition demonstrates:
- ✅ **5 digital skills** exposed to IBM watsonx Orchestrate
- ✅ **Webhook integration** for real-time agent invocation
- ✅ **API key authentication** for secure communication
- ✅ **Production-ready** JSON schema compliant with IBM standards
- ✅ **Multi-agent orchestration** (5 actions → 6 backend agents)

**Evidence of IBM watsonx usage:**
1. This skill definition file (IBM-compliant schema)
2. Webhook endpoint in backend code
3. Test results from IBM Orchestrate UI
4. Screenshots of skill in IBM platform

---

**Need help?** See `IBM_WATSONX_SETUP_GUIDE.md` for complete step-by-step instructions.
