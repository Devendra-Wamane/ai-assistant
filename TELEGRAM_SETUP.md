# 🤖 Telegram Bot Setup Guide for AI Assistant

Transform your AI Assistant into a real Telegram bot that anyone can chat with!

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Your Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Send** `/newbot` to BotFather
3. **Choose a name** for your bot (e.g., "My AI Assistant")
4. **Choose a username** (must end with 'bot', e.g., "my_ai_assistant_bot")
5. **Copy the bot token** (looks like: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`)

### Step 2: Install Requirements

```bash
cd /home/devendra/Desktop/devops/ai-assistant

# Install Telegram bot dependencies
pip install -r telegram_requirements.txt
```

### Step 3: Configure Your Bot

```bash
# Edit telegram_bot.py and replace the token
nano telegram_bot.py

# Change this line:
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# To your actual token:
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"
```

### Step 4: Start Everything

```bash
# Terminal 1: Start your AI API
source venv/bin/activate
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Telegram Bot
source venv/bin/activate
python telegram_bot.py
```

### Step 5: Test Your Bot!

1. **Find your bot** on Telegram (search for your bot's username)
2. **Send** `/start` to begin
3. **Try questions** like:
   - "What is CI/CD?"
   - "Explain Docker containers"
   - "Help with Kubernetes"

## 🎯 Bot Features

### **Commands Available:**
- `/start` - Welcome message with quick topic buttons
- `/help` - Show help and example questions
- `/health` - Check if AI API is running
- `/clear` - Clear your chat history
- `/topics` - Show all available topics

### **Quick Topic Buttons:**
- 🔄 CI/CD Help
- 🐳 Docker Guide
- ☸️ Kubernetes Info
- ☁️ AWS Services
- 🏗️ Terraform
- 🔧 DevOps

### **Smart Features:**
- ✅ **Connection Status** - Checks if your API is running
- 🔄 **Typing Indicators** - Shows when AI is thinking
- 📱 **Long Message Support** - Splits long responses automatically
- 💾 **Chat History** - Maintains conversation context
- ❌ **Error Handling** - Graceful error messages
- 🔐 **User Isolation** - Each user has separate chat history

## 🌍 Architecture Flow

```
User Message → Telegram → Your Bot → FastAPI → AI Response → Telegram → User
```

1. **User sends message** to your Telegram bot
2. **Bot receives** message via Telegram API
3. **Bot forwards** message to your FastAPI `/chat` endpoint
4. **AI processes** and generates response
5. **Bot sends response** back to user on Telegram

## 🔧 Configuration Options

### **Change API URL** (if running on different server):
```python
AI_API_URL = "https://your-domain.com"  # For production
AI_API_URL = "http://192.168.1.100:8000"  # For local network
```

### **Environment Variables** (recommended for production):
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
export AI_API_URL="http://localhost:8000"
```

Then modify the bot:
```python
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AI_API_URL = os.getenv("AI_API_URL", "http://localhost:8000")
```

## 🚀 Production Deployment

### **Option 1: VPS with systemd**
```bash
# Create service file
sudo nano /etc/systemd/system/ai-telegram-bot.service

[Unit]
Description=AI Assistant Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/devendra/Desktop/devops/ai-assistant
Environment=PATH=/home/devendra/Desktop/devops/ai-assistant/venv/bin
ExecStart=/home/devendra/Desktop/devops/ai-assistant/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable ai-telegram-bot
sudo systemctl start ai-telegram-bot
```

### **Option 2: Docker Deployment**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt -r telegram_requirements.txt

CMD ["python", "telegram_bot.py"]
```

### **Option 3: Cloud Platforms**
- **Railway**: Connect GitHub, auto-deploy
- **Heroku**: `git push heroku main`
- **DigitalOcean Apps**: One-click deployment

## 🔐 Security Best Practices

1. **Keep your bot token secret** - Never commit to Git
2. **Use environment variables** for tokens
3. **Run bot and API on same server** for security
4. **Set up HTTPS** for production API
5. **Monitor bot logs** for errors and usage

## 🎭 Customization Ideas

### **Add Custom Commands:**
```python
async def stats_command(self, update: Update, context) -> None:
    # Show usage statistics
    await update.message.reply_text("📊 Bot Statistics: ...")

self.application.add_handler(CommandHandler("stats", self.stats_command))
```

### **Add Inline Keyboards:**
```python
keyboard = [
    [InlineKeyboardButton("📚 Documentation", url="https://your-docs.com")],
    [InlineKeyboardButton("💬 Support", url="https://t.me/your_support")]
]
```

### **Add File Uploads:**
```python
async def handle_document(self, update: Update, context) -> None:
    # Process uploaded files
    document = update.message.document
    # Send to AI for analysis
```

## 🎉 Success!

Your AI Assistant is now a real Telegram bot! Users can:
- ✅ Chat with AI anytime, anywhere
- ✅ Get instant DevOps help
- ✅ Learn about Docker, Kubernetes, AWS
- ✅ Access from any device with Telegram

**Share your bot with friends and colleagues!** 🚀

## 🆘 Troubleshooting

### **Bot doesn't respond:**
1. Check if FastAPI is running: `curl http://localhost:8000/health`
2. Check bot logs for errors
3. Verify bot token is correct

### **"Connection Error":**
- AI API is not running
- Check firewall settings
- Verify API_URL configuration

### **Messages too long:**
- Bot automatically splits long messages
- Consider summarizing responses for mobile users

Your Telegram bot is now the perfect interface for your AI Assistant! 🤖✨