# 🚀 Production Deployment Guide

## 🌐 Quick Deployment Options

### Option 1: 🆓 **Railway** (Recommended - Free Tier)
```bash
# 1. Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# 2. Login and deploy
railway login
railway init
railway up

# ✅ Gets you: https://your-app.railway.app
```

### Option 2: 🐳 **DigitalOcean App Platform** (Easy)
```bash
# 1. Push your repo to GitHub (already done ✅)
# 2. Connect at: https://cloud.digitalocean.com/apps
# 3. Select your GitHub repo
# 4. Auto-deploys on every push!

# ✅ Gets you: https://your-app.ondigitalocean.app
```

### Option 3: 🌊 **Render** (Simple)
```bash
# 1. Connect GitHub at: https://render.com
# 2. Create new Web Service
# 3. Select your repo
# 4. Start command: uvicorn app:app --host 0.0.0.0 --port $PORT

# ✅ Gets you: https://your-app.onrender.com
```

### Option 4: ⚡ **Fly.io** (Fast Global)
```bash
# 1. Install flyctl
curl -L https://fly.io/install.sh | sh

# 2. Launch app
flyctl auth login
flyctl launch

# ✅ Gets you: https://your-app.fly.dev
```

## 🔧 For Your Own Server (VPS/AWS/GCP)

### Step 1: Server Setup
```bash
# On your server (Ubuntu/Debian):
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### Step 2: GitHub Secrets Configuration
Go to your GitHub repo → Settings → Secrets and variables → Actions

Add these secrets:
```
PRODUCTION_HOST=your-actual-server.com
PRODUCTION_USER=ubuntu
PRODUCTION_SSH_KEY=<your-ssh-private-key>
```

### Step 3: Update Deployment Workflow
The workflow will automatically deploy to your real server!

---

## 🎯 **FASTEST OPTION: Railway (1 minute setup)**

1. **Install Railway CLI:**
   ```bash
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Deploy your app:**
   ```bash
   cd /home/devendra/Desktop/devops/ai-assistant
   railway login
   railway init
   railway up
   ```

3. **Set PORT environment variable:**
   ```bash
   railway variables set PORT=8000
   ```

4. **Done!** Your app will be live at `https://your-app.railway.app`

## 🔗 **Links After Deployment:**

- **API**: `https://your-app.railway.app/`
- **Health Check**: `https://your-app.railway.app/health`  
- **Interactive Docs**: `https://your-app.railway.app/docs`
- **Chat Interface**: `https://your-app.railway.app/` (try asking about Docker!)

## 🎉 **Result:**
Instead of `http://your-server.com:8000/` ❌  
You'll get `https://your-app.railway.app/` ✅