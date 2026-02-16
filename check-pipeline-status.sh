#!/bin/bash

# 🔍 CI/CD Pipeline Status Checker
# This script helps monitor GitHub Actions workflow status

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 AI Assistant CI/CD Pipeline Status${NC}"
echo "=================================="

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Get current branch and latest commit
BRANCH=$(git branch --show-current)
COMMIT=$(git rev-parse --short HEAD)
REMOTE_URL=$(git config --get remote.origin.url)

echo -e "📍 Branch: ${YELLOW}$BRANCH${NC}"
echo -e "🔗 Commit: ${YELLOW}$COMMIT${NC}"
echo -e "🌐 Remote: ${BLUE}$REMOTE_URL${NC}"
echo ""

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    echo "   Run 'git status' to see what needs to be committed"
    echo ""
fi

# Check GitHub Actions status (if gh CLI is available)
if command -v gh &> /dev/null; then
    echo -e "${BLUE}🤖 Recent GitHub Actions Runs:${NC}"
    echo "--------------------------------"
    
    # Get recent workflow runs
    gh run list --limit 5 --json status,conclusion,createdAt,displayTitle,url | \
    jq -r '.[] | "\(.status) | \(.conclusion // "running") | \(.displayTitle) | \(.url)"' | \
    while IFS='|' read -r status conclusion title url; do
        case $conclusion in
            "success")
                echo -e "✅ $title"
                ;;
            "failure")
                echo -e "${RED}❌ $title${NC}"
                echo -e "   🔗 View: $url"
                ;;
            "cancelled")
                echo -e "${YELLOW}⏹️  $title (cancelled)${NC}"
                ;;
            "running")
                echo -e "${BLUE}⏳ $title (running...)${NC}"
                ;;
            *)
                echo -e "🔄 $title ($conclusion)"
                ;;
        esac
    done
else
    echo -e "${YELLOW}💡 Install GitHub CLI for workflow status: ${NC}https://cli.github.com/"
fi

echo ""
echo -e "${BLUE}📋 Quick Commands:${NC}"
echo "  📊 Check workflows: gh run list"
echo "  🔍 View latest run: gh run view"
echo "  📱 Open Actions page: gh repo view --web"
echo "  🚀 Trigger deployment: git push origin main"

echo ""
echo -e "${GREEN}✅ Status check complete!${NC}"