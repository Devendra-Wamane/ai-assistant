# 🚀 One-Click Railway Deploy

Deploy your AI Assistant to Railway with one click!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/ai-assistant)

## ⚡ Instant Deployment

Click the button above and you'll get:
- ✅ **Live Public URL**: `https://your-app.railway.app`
- ✅ **Automatic HTTPS**
- ✅ **Auto-Deploy on Git Push**
- ✅ **Free Tier Available**

## 🔧 Manual Railway Setup

If the button doesn't work, run:

```bash
./setup-railway-auto.sh
```

This will:
1. Install Railway CLI
2. Login to your Railway account
3. Deploy your AI Assistant
4. Set up auto-deployment from GitHub

## 🌐 After Deployment

Your AI Assistant will be available at:
- **Main App**: `https://your-app.railway.app/`
- **API Docs**: `https://your-app.railway.app/docs`
- **Health Check**: `https://your-app.railway.app/health`

## ⚡ Auto-Deployment

Once set up, every time you push to GitHub:
```bash
git add .
git commit -m "Update my AI Assistant"
git push origin main
```

GitHub Actions automatically deploys to Railway! 🚀