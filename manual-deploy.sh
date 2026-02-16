#!/bin/bash

# 🚀 Manual CI/CD Pipeline Controller
# Control your GitHub Actions workflows manually

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AI Assistant - Manual Pipeline Control${NC}"
echo "============================================"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI not found${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

echo -e "${YELLOW}🎛️  Choose pipeline action:${NC}"
echo ""
echo "1. 🧪 Run Full CI/CD Pipeline (Test + Build + Deploy)"
echo "2. 🚂 Deploy to Railway"
echo "3. 🔍 Run Tests Only"
echo "4. 🐳 Build Docker Image Only" 
echo "5. 📊 Check Pipeline Status"
echo "6. 🛑 Cancel Running Workflows"
echo ""

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo -e "${BLUE}🚀 Starting Full CI/CD Pipeline...${NC}"
        echo ""
        echo -e "${YELLOW}📋 Environment options:${NC}"
        echo "1. Production"
        echo "2. Staging"
        echo "3. Development"
        echo ""
        read -p "Select environment (1-3): " env_choice
        
        case $env_choice in
            1) environment="production" ;;
            2) environment="staging" ;;
            3) environment="development" ;;
            *) environment="production" ;;
        esac
        
        echo -e "${BLUE}🎯 Triggering CI/CD Pipeline for: $environment${NC}"
        gh workflow run "deploy.yml" \
            --field environment="$environment" \
            --field run_tests="true" \
            --field deploy_to_registry="true"
        
        echo -e "${GREEN}✅ Pipeline started!${NC}"
        echo "🔍 Monitor progress: gh run list"
        ;;
        
    2)
        echo -e "${BLUE}🚂 Deploying to Railway...${NC}"
        
        read -p "Force deploy even if no changes? (y/N): " force
        force_deploy="false"
        [[ $force =~ ^[Yy]$ ]] && force_deploy="true"
        
        gh workflow run "deploy-railway.yml" \
            --field force_deploy="$force_deploy"
        
        echo -e "${GREEN}✅ Railway deployment started!${NC}"
        echo "🌐 Check your Railway dashboard for progress"
        ;;
        
    3)
        echo -e "${BLUE}🧪 Running Tests Only...${NC}"
        
        gh workflow run "deploy.yml" \
            --field environment="development" \
            --field run_tests="true" \
            --field deploy_to_registry="false"
        
        echo -e "${GREEN}✅ Test suite started!${NC}"
        echo "🔍 Monitor progress: gh run list"
        ;;
        
    4)
        echo -e "${BLUE}🐳 Building Docker Image Only...${NC}"
        
        gh workflow run "deploy.yml" \
            --field environment="staging" \
            --field run_tests="false" \
            --field deploy_to_registry="true"
        
        echo -e "${GREEN}✅ Docker build started!${NC}"
        echo "📦 Image will be pushed to GitHub Container Registry"
        ;;
        
    5)
        echo -e "${BLUE}📊 Pipeline Status:${NC}"
        echo "==================="
        
        # Show recent workflow runs
        echo -e "${YELLOW}🏃 Recent Workflow Runs:${NC}"
        gh run list --limit 10
        
        echo ""
        echo -e "${YELLOW}⏳ Currently Running:${NC}"
        gh run list --status in_progress || echo "No workflows currently running"
        
        echo ""
        echo -e "${BLUE}💡 Commands:${NC}"
        echo "  📱 Open Actions page: gh repo view --web"
        echo "  🔍 View specific run: gh run view <run-id>"
        echo "  📜 View logs: gh run view --log"
        ;;
        
    6)
        echo -e "${BLUE}🛑 Canceling Running Workflows...${NC}"
        
        # Get running workflows
        running_runs=$(gh run list --status in_progress --json databaseId --jq '.[].databaseId')
        
        if [ -z "$running_runs" ]; then
            echo -e "${YELLOW}ℹ️  No workflows currently running${NC}"
            exit 0
        fi
        
        echo -e "${YELLOW}⚠️  Found running workflows. Cancel all? (y/N):${NC}"
        read -p "" confirm
        
        if [[ $confirm =~ ^[Yy]$ ]]; then
            echo "$running_runs" | while read -r run_id; do
                if [ ! -z "$run_id" ]; then
                    echo "Canceling run $run_id..."
                    gh run cancel "$run_id"
                fi
            done
            echo -e "${GREEN}✅ All running workflows canceled${NC}"
        else
            echo -e "${BLUE}ℹ️  No workflows canceled${NC}"
        fi
        ;;
        
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}📋 Useful Commands:${NC}"
echo "  🔍 Check status: ./manual-deploy.sh (choose option 5)"
echo "  📱 GitHub Actions: gh repo view --web"
echo "  🏃 List runs: gh run list"
echo ""
echo -e "${GREEN}🎉 Done! Your pipeline is now under manual control.${NC}"