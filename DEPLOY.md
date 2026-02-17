# 🚀 AI Assistant Deployment Guide

## Quick Deploy to Render (Recommended)

### 1️⃣ Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New + → Web Service"**
3. Connect your GitHub repository: `your-username/ai-assistant`
4. Configure the service:

```
Name: ai-assistant
Root Directory: (leave blank)
Environment: Python 3.11
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
```

### 2️⃣ Auto-Deploy Configuration

Render will automatically deploy when you push to `main` branch!

Your live URLs will be:
- 🌐 **Main App**: `https://your-service-name.onrender.com/`
- 📚 **API Docs**: `https://your-service-name.onrender.com/docs`
- 💚 **Health Check**: `https://your-service-name.onrender.com/health`

### 3️⃣ Environment Variables (Optional)

In your Render dashboard, you can set:
```
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Alternative Platforms

### Railway
1. Visit [railway.app](https://railway.app)
2. Deploy from GitHub
3. Railway will auto-detect Python and use `railway.toml`

### Vercel
```bash
npm i -g vercel
vercel --prod
```

## Testing Your Live Deployment

Once deployed, test your AI Assistant:

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### Ask Questions
```bash
curl -X POST "https://your-app.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Docker?", "context": "DevOps"}'
```

### Browse Interactive Docs
Visit: `https://your-app.onrender.com/docs`

## CI/CD Pipeline

Your GitHub Actions workflow will:
1. ✅ Run tests on Python 3.10, 3.11, 3.12
2. 🔒 Security scan with Bandit
3. 🐳 Build Docker images
4. 🚀 Auto-deploy to your platform

## Manual Deployment Control

Use the manual deployment script:
```bash
./manual-deploy.sh
```

This gives you interactive control over:
- Running specific pipeline stages
- Skipping tests or security scans
- Deploying to specific environments

## Troubleshooting

### Deployment Fails
1. Check Render/Railway logs
2. Verify `requirements.txt` is complete
3. Ensure Python version compatibility

### App Won't Start
1. Check the start command
2. Verify port configuration (`$PORT`)
3. Review application logs

### API Not Responding
1. Test health endpoint first
2. Check API documentation at `/docs`
3. Verify environment variables

## 🎉 Success!

Once deployed, your AI Assistant will be globally accessible at your live URL!

Test it by asking questions like:
- "What is Kubernetes?"
- "Explain Docker containers"
- "How to set up CI/CD?"

Your DevOps AI Expert is now live! 🚀