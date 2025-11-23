# Vercel Deployment Guide for FinAgent Pro

## Quick Fix for 404 Error

The 404 error happens because:
1. Vercel needs SPA routing configuration (✅ fixed with `vercel.json`)
2. Production settings may differ from project settings

## Vercel Configuration Steps

### 1. Project Settings (in Vercel Dashboard)

Navigate to: **Settings > Build & Development**

```
Root Directory: frontend
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### 2. Environment Variables (in Vercel Dashboard)

Navigate to: **Settings > Environment Variables**

Add these variables for all environments (Production, Preview, Development):

```
VITE_API_BASE_URL=https://your-backend-url.com
```

**Note:** You need to deploy your FastAPI backend separately (see Backend Deployment below).

### 3. SPA Routing Configuration

✅ Already created: `frontend/vercel.json`

This file ensures all routes redirect to `index.html` for client-side routing.

### 4. Fix Production Override Warning

The warning "Configuration Settings in the current Production deployment differ from your current Project Settings" means:

**Solution:**
1. Click **"Production Overrides"** in the warning banner
2. Click **"Use Project Settings"** to sync them
3. Or manually redeploy with correct settings

## Backend Deployment Options

Since Vercel doesn't support Python/FastAPI backends well, deploy backend separately:

### Option 1: Render.com (Recommended - Free Tier Available)
```bash
# 1. Create account on render.com
# 2. New Web Service > Connect GitHub repo
# 3. Settings:
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Environment: Python 3
```

### Option 2: Railway.app
```bash
# 1. Create account on railway.app
# 2. New Project > Deploy from GitHub
# 3. Add environment variables
# 4. Railway auto-detects Python and requirements.txt
```

### Option 3: Heroku
```bash
# Create Procfile in backend/:
web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4

# Deploy:
heroku create finagent-api
git subtree push --prefix backend heroku main
```

### Option 4: Azure App Service (Enterprise)
```bash
az webapp up --name finagent-api --runtime "PYTHON:3.11" --sku B1
```

## Testing Locally Before Deploy

### Frontend:
```bash
cd frontend
npm run build
npm run preview
# Open http://localhost:4173
```

### Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# Open http://localhost:8000/docs
```

## After Deployment Checklist

- [ ] Backend deployed and accessible at public URL
- [ ] `VITE_API_BASE_URL` set in Vercel environment variables
- [ ] Vercel project settings match: Root=frontend, Build=npm run build, Output=dist
- [ ] Redeploy frontend on Vercel (Settings > Deployments > Redeploy)
- [ ] Test all routes work (no 404 on refresh)
- [ ] Test API calls reach backend
- [ ] Check browser console for CORS errors
- [ ] Verify DEMO_MODE works if enabled

## CORS Configuration

If you get CORS errors after deployment, update backend `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting

### Still getting 404?
1. Check Vercel deployment logs for build errors
2. Verify `dist` folder was created in build
3. Ensure `vercel.json` is in frontend folder
4. Clear Vercel cache: Settings > Advanced > Clear Cache

### API calls failing?
1. Verify `VITE_API_BASE_URL` environment variable is set
2. Check backend is running and accessible
3. Check browser Network tab for actual error
4. Verify CORS settings on backend

### Build fails?
1. Check Vercel build logs for specific error
2. Test build locally: `npm run build`
3. Verify Node.js version (should be 18 or 20)
4. Check for TypeScript errors

## Quick Commands

```bash
# Push changes and trigger Vercel deploy
git add .
git commit -m "Add Vercel config"
git push origin main

# Force redeploy on Vercel (no code changes needed)
# Use Vercel dashboard: Deployments > ... > Redeploy

# Test production build locally
cd frontend && npm run build && npm run preview
```

## Need Help?

- Vercel logs: Check deployment logs in Vercel dashboard
- Backend logs: Check your backend hosting provider's logs
- Browser console: Press F12 and check Console and Network tabs
