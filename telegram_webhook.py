#!/usr/bin/env python3
"""
Telegram Bot Webhook Version for Production
More efficient for high-traffic bots
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import aiohttp
import logging
import os
from typing import Dict, Any
import asyncio
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
AI_API_URL = os.getenv("AI_API_URL", "http://localhost:8000")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-domain.com/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your_webhook_secret")

# FastAPI app for webhook
webhook_app = FastAPI(title="AI Assistant Telegram Webhook")

# Telegram bot instance
bot = Bot(token=TELEGRAM_BOT_TOKEN)
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

class WebhookBot:
    def __init__(self):
        self.bot = bot
        self.application = application

    async def get_ai_response(self, message: str, user_id: str) -> str:
        """Get response from AI Assistant API"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "message": message,
                    "user_id": f"telegram_webhook_{user_id}"
                }
                
                async with session.post(
                    f"{AI_API_URL}/chat",
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', 'No response from AI')
                    else:
                        return f"❌ AI API Error: Status {response.status}"
                        
        except asyncio.TimeoutError:
            return "❌ AI response timeout. Please try again."
        except aiohttp.ClientError as e:
            return f"❌ Connection Error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected Error: {str(e)}"

    async def send_long_message(self, chat_id: int, message: str) -> None:
        """Send long messages by splitting them if necessary"""
        max_length = 4096
        
        if len(message) <= max_length:
            await self.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        else:
            chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await self.bot.send_message(chat_id=chat_id, text=chunk, parse_mode='Markdown')
                else:
                    await self.bot.send_message(chat_id=chat_id, text=f"*...continued:*\n\n{chunk}", parse_mode='Markdown')

    async def handle_start(self, update: Update) -> None:
        """Handle /start command"""
        user = update.effective_user
        welcome_text = f"""
🤖 **Welcome to AI Assistant Bot!** 

Hello {user.first_name}! I'm your DevOps & Cloud expert.

🚀 **Ask me about:**
• CI/CD & DevOps practices
• Docker & Kubernetes
• AWS & Cloud services  
• Terraform & Infrastructure
• Programming & Automation

💬 Just send any message to start chatting!
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔄 CI/CD", callback_data="topic_cicd"),
                InlineKeyboardButton("🐳 Docker", callback_data="topic_docker"),
            ],
            [
                InlineKeyboardButton("☸️ Kubernetes", callback_data="topic_k8s"),
                InlineKeyboardButton("☁️ AWS", callback_data="topic_aws"),
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="help"),
                InlineKeyboardButton("📊 Status", callback_data="health"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_message(self, update: Update) -> None:
        """Handle regular text messages"""
        if not update.message or not update.message.text:
            return
            
        user_message = update.message.text
        user_id = str(update.effective_user.id)
        chat_id = update.effective_chat.id
        
        # Send typing action
        await self.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        try:
            # Get AI response
            ai_response = await self.get_ai_response(user_message, user_id)
            
            # Send response
            await self.send_long_message(chat_id, ai_response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            error_msg = "❌ Sorry, I encountered an error. Please try again!"
            await self.bot.send_message(chat_id=chat_id, text=error_msg)

    async def handle_callback(self, update: Update) -> None:
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        chat_id = query.message.chat_id
        
        topic_questions = {
            "topic_cicd": "What is CI/CD and how does it work?",
            "topic_docker": "Explain Docker and containerization",
            "topic_k8s": "What is Kubernetes and how does it work?",
            "topic_aws": "Show me AWS services and cloud computing",
            "help": "help",
            "health": None  # Special case for health check
        }
        
        if callback_data == "health":
            # Health check
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{AI_API_URL}/health") as response:
                        if response.status == 200:
                            await self.bot.send_message(chat_id=chat_id, text="✅ AI API is healthy and ready!")
                        else:
                            await self.bot.send_message(chat_id=chat_id, text=f"❌ AI API returned status {response.status}")
            except Exception as e:
                await self.bot.send_message(chat_id=chat_id, text=f"❌ Cannot connect to AI API: {str(e)}")
        
        elif callback_data in topic_questions:
            question = topic_questions[callback_data]
            user_id = str(query.from_user.id)
            
            # Send typing action
            await self.bot.send_chat_action(chat_id=chat_id, action="typing")
            
            # Get AI response
            ai_response = await self.get_ai_response(question, user_id)
            await self.send_long_message(chat_id, ai_response)

    async def process_update(self, update_data: Dict[Any, Any]) -> None:
        """Process incoming webhook update"""
        try:
            update = Update.de_json(update_data, self.bot)
            
            if update.message:
                if update.message.text and update.message.text.startswith('/start'):
                    await self.handle_start(update)
                elif update.message.text and not update.message.text.startswith('/'):
                    await self.handle_message(update)
            elif update.callback_query:
                await self.handle_callback(update)
                
        except Exception as e:
            logger.error(f"Error processing update: {e}")

# Global webhook bot instance
webhook_bot = WebhookBot()

# Webhook endpoints
@webhook_app.post("/webhook")
async def webhook_endpoint(request: Request):
    """Handle incoming webhook from Telegram"""
    try:
        # Verify webhook secret (optional but recommended)
        webhook_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if WEBHOOK_SECRET != "your_webhook_secret" and webhook_secret != WEBHOOK_SECRET:
            raise HTTPException(status_code=403, detail="Invalid webhook secret")
        
        # Process the update
        update_data = await request.json()
        await webhook_bot.process_update(update_data)
        
        return JSONResponse(content={"status": "ok"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@webhook_app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Assistant Telegram Bot Webhook Server",
        "status": "running",
        "webhook_url": "/webhook"
    }

@webhook_app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if we can reach the AI API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{AI_API_URL}/health", timeout=5) as response:
                ai_healthy = response.status == 200
    except:
        ai_healthy = False
    
    return {
        "webhook_status": "healthy",
        "ai_api_status": "healthy" if ai_healthy else "unhealthy",
        "ai_api_url": AI_API_URL
    }

@webhook_app.post("/setup-webhook")
async def setup_webhook():
    """Setup webhook with Telegram (call this once)"""
    if WEBHOOK_URL == "https://your-domain.com/webhook":
        return {"error": "Please set WEBHOOK_URL environment variable"}
    
    try:
        webhook_info = await bot.set_webhook(
            url=WEBHOOK_URL,
            secret_token=WEBHOOK_SECRET if WEBHOOK_SECRET != "your_webhook_secret" else None
        )
        return {"status": "webhook_set", "info": str(webhook_info)}
    except Exception as e:
        return {"error": str(e)}

@webhook_app.get("/webhook-info")
async def get_webhook_info():
    """Get current webhook information"""
    try:
        webhook_info = await bot.get_webhook_info()
        return {
            "url": webhook_info.url,
            "has_custom_certificate": webhook_info.has_custom_certificate,
            "pending_update_count": webhook_info.pending_update_count,
            "last_error_date": webhook_info.last_error_date,
            "last_error_message": webhook_info.last_error_message,
            "max_connections": webhook_info.max_connections,
            "allowed_updates": webhook_info.allowed_updates
        }
    except Exception as e:
        return {"error": str(e)}

# For production deployment
if __name__ == "__main__":
    import uvicorn
    
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set TELEGRAM_BOT_TOKEN environment variable!")
        exit(1)
    
    print("🚀 Starting Telegram Webhook Server...")
    print(f"📡 Webhook URL: {WEBHOOK_URL}")
    print(f"🤖 AI API URL: {AI_API_URL}")
    
    # Run the webhook server
    uvicorn.run(
        "telegram_webhook:webhook_app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=False
    )