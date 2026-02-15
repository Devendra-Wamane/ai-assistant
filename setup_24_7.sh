#!/bin/bash

# AI Assistant 24/7 Setup Script
echo "🚀 Setting up AI Assistant for 24/7 operation..."

# Create systemd service
echo "📋 Installing systemd service..."
sudo cp ai-assistant.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ai-assistant
sudo systemctl start ai-assistant

echo "✅ Service installed and started!"
echo ""
echo "🔧 Service Management Commands:"
echo "  Start:   sudo systemctl start ai-assistant"
echo "  Stop:    sudo systemctl stop ai-assistant"
echo "  Restart: sudo systemctl restart ai-assistant"
echo "  Status:  sudo systemctl status ai-assistant"
echo "  Logs:    sudo journalctl -u ai-assistant -f"
echo ""
echo "🌐 Your AI Assistant is now running 24/7 at:"
echo "  http://localhost:8000"
echo "  http://your-server-ip:8000"
echo ""
echo "🎯 Next steps for production:"
echo "  1. Configure reverse proxy (Nginx/Apache)"
echo "  2. Set up SSL certificates"
echo "  3. Configure domain name"
echo "  4. Set up monitoring and alerts"