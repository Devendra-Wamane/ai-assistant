#!/bin/bash

# 🚂 Railway Auto-Setup Script
# This will set up automatic deployment to get you a real public URL

set -e

echo "🚂 Setting up Railway Auto-Deployment..."
echo "======================================="

# Check if railway CLI is available
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
    export PATH="$HOME/.railway/bin:$PATH"
fi

echo "🔑 Please login to Railway..."
railway login

echo "🚀 Creating and deploying your AI Assistant..."

# Initialize Railway project
railway init --name "ai-assistant-$(date +%s)"

# Set environment variables
railway variables set PORT=8000
railway variables set ENVIRONMENT=production

# Deploy the application
echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "🎉 SUCCESS! Your AI Assistant is being deployed!"
echo ""
echo "📋 What happens now:"
echo "   1. Railway is building your Docker container"
echo "   2. Your app will be deployed to a public URL"
echo "   3. Check your Railway dashboard for the live URL"
echo ""
echo "🔗 Next steps:"
echo "   1. Go to: https://railway.app/dashboard"
echo "   2. Find your 'ai-assistant' project"
echo "   3. Click on it to see your live URL"
echo ""
echo "⚡ Future deployments:"
echo "   • Just push to GitHub: git push origin main"
echo "   • GitHub Actions will auto-deploy to Railway"
echo "   • Your URL stays the same!"
echo ""
echo "🌐 Your AI Assistant will be live at: https://[your-app].railway.app"