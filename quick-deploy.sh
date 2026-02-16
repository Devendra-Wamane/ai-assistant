#!/bin/bash

# 🚀 AI Assistant - Quick Deploy Script
# Deploys your AI Assistant to various platforms

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AI Assistant - Quick Deploy${NC}"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: app.py not found. Run this from the ai-assistant directory${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Choose deployment option:${NC}"
echo "1. 🚂 Railway (Free, Fastest)"
echo "2. 🌊 Render (Free)"
echo "3. 🐳 DigitalOcean App Platform"
echo "4. ⚡ Fly.io"
echo "5. 🏠 Local Docker"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo -e "${BLUE}🚂 Deploying to Railway...${NC}"
        
        # Check if railway CLI is installed
        if ! command -v railway &> /dev/null; then
            echo -e "${YELLOW}📦 Installing Railway CLI...${NC}"
            curl -fsSL https://railway.app/install.sh | sh
            export PATH="$HOME/.railway/bin:$PATH"
        fi
        
        echo -e "${BLUE}🔑 Logging into Railway (browser will open)...${NC}"
        railway login
        
        echo -e "${BLUE}🚀 Initializing and deploying...${NC}"
        railway init --name ai-assistant
        railway up
        
        echo -e "${GREEN}✅ Railway deployment started!${NC}"
        echo -e "${GREEN}🌐 Check your Railway dashboard for the live URL${NC}"
        ;;
        
    2)
        echo -e "${BLUE}🌊 Setting up Render deployment...${NC}"
        echo -e "${YELLOW}📋 Manual steps required:${NC}"
        echo "1. Go to https://render.com"
        echo "2. Connect your GitHub account"
        echo "3. Create new Web Service"
        echo "4. Select this repository"
        echo "5. Use these settings:"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: uvicorn app:app --host 0.0.0.0 --port \$PORT"
        echo "6. Click Deploy"
        echo ""
        echo -e "${GREEN}✅ Render will auto-deploy on every git push!${NC}"
        ;;
        
    3)
        echo -e "${BLUE}🐳 Setting up DigitalOcean App Platform...${NC}"
        echo -e "${YELLOW}📋 Manual steps required:${NC}"
        echo "1. Go to https://cloud.digitalocean.com/apps"
        echo "2. Create New App"
        echo "3. Connect your GitHub repository"
        echo "4. Select this repository"
        echo "5. DigitalOcean will auto-detect FastAPI settings"
        echo "6. Click Deploy"
        echo ""
        echo -e "${GREEN}✅ DigitalOcean will auto-deploy on every git push!${NC}"
        ;;
        
    4)
        echo -e "${BLUE}⚡ Deploying to Fly.io...${NC}"
        
        # Check if flyctl is installed
        if ! command -v flyctl &> /dev/null; then
            echo -e "${YELLOW}📦 Installing Fly.io CLI...${NC}"
            curl -L https://fly.io/install.sh | sh
            export PATH="$HOME/.fly/bin:$PATH"
        fi
        
        echo -e "${BLUE}🔑 Logging into Fly.io...${NC}"
        flyctl auth login
        
        echo -e "${BLUE}🚀 Launching app...${NC}"
        flyctl launch --name ai-assistant
        
        echo -e "${GREEN}✅ Fly.io deployment complete!${NC}"
        echo -e "${GREEN}🌐 Your app is live at https://ai-assistant.fly.dev${NC}"
        ;;
        
    5)
        echo -e "${BLUE}🏠 Running with Local Docker...${NC}"
        
        echo -e "${BLUE}🐳 Building Docker image...${NC}"
        docker build -t ai-assistant .
        
        echo -e "${BLUE}🚀 Starting container...${NC}"
        docker run -d --name ai-assistant-local \
            --restart unless-stopped \
            -p 8000:8000 \
            ai-assistant
        
        echo -e "${GREEN}✅ Local deployment complete!${NC}"
        echo -e "${GREEN}🌐 Your AI Assistant is running at:${NC}"
        echo -e "${GREEN}   API: http://localhost:8000${NC}"
        echo -e "${GREEN}   Docs: http://localhost:8000/docs${NC}"
        echo -e "${GREEN}   Chat: http://localhost:8000${NC}"
        ;;
        
    *)
        echo -e "${RED}❌ Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Deployment process initiated!${NC}"
echo -e "${BLUE}📋 Next steps:${NC}"
echo "   • Wait for deployment to complete"
echo "   • Test your live API endpoints"
echo "   • Update Telegram bot with new URL (if using)"
echo "   • Share your AI Assistant with the world! 🌍"