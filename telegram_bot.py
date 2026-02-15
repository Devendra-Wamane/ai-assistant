#!/usr/bin/env python3
"""
Telegram Bot for AI Assistant
Connects Telegram users to your FastAPI AI Assistant
"""

import asyncio
import logging
import aiohttp
import json
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = "8512310648:AAGqpJG1uvHgJJlW9cn5YswqOBwqPO8C000"  # Your real bot token
AI_API_URL = "http://localhost:8000"  # Your FastAPI URL

class AIAssistantTelegramBot:
    def __init__(self, token: str, api_url: str):
        self.token = token
        self.api_url = api_url
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all bot command and message handlers"""
        
        # Commands
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("health", self.health_command))
        self.application.add_handler(CommandHandler("clear", self.clear_history))
        self.application.add_handler(CommandHandler("topics", self.show_topics))
        
        # Callback queries for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Messages (AI chat)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context) -> None:
        """Handle /start command"""
        user = update.effective_user
        welcome_text = f"""
🤖 **Welcome to AI Assistant Bot!** 

Hello {user.first_name}! I'm your personal DevOps & Cloud expert assistant.

🚀 **What I can help you with:**
• CI/CD pipelines and automation
• Docker and containerization
• Kubernetes orchestration  
• AWS, Azure, and cloud services
• Infrastructure as Code (Terraform)
• DevOps best practices
• Programming and development

💬 **How to use:**
Just send me any message and I'll help you learn!

Try asking: "What is Docker?" or "Explain CI/CD"
        """
        
        # Create inline keyboard with quick topics
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
                InlineKeyboardButton("🏗️ Terraform", callback_data="topic_terraform"),
                InlineKeyboardButton("🔧 DevOps", callback_data="topic_devops"),
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="help"),
                InlineKeyboardButton("📊 API Health", callback_data="health"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def help_command(self, update: Update, context) -> None:
        """Handle /help command"""
        help_text = """
🤖 **AI Assistant Bot Commands:**

**Basic Commands:**
/start - Welcome message and quick topics
/help - Show this help message
/health - Check AI API status
/clear - Clear your chat history
/topics - Show all available topics

**How to Chat:**
Just type your question! No special commands needed.

**Example Questions:**
• "What is CI/CD pipeline?"
• "How to use Docker containers?"
• "Explain Kubernetes architecture"
• "Show me AWS services"
• "Help with Terraform"

**Quick Topics:**
Use the buttons below for instant help on popular topics!
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 CI/CD Help", callback_data="topic_cicd")],
            [InlineKeyboardButton("🐳 Docker Guide", callback_data="topic_docker")],
            [InlineKeyboardButton("☸️ Kubernetes Info", callback_data="topic_k8s")],
            [InlineKeyboardButton("☁️ AWS Services", callback_data="topic_aws")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def health_command(self, update: Update, context) -> None:
        """Check AI API health"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/health") as response:
                    if response.status == 200:
                        health_data = await response.json()
                        status_text = f"""
✅ **AI Assistant API Status**

🟢 **Status**: {health_data.get('status', 'Unknown')}
📝 **Message**: {health_data.get('message', 'No message')}
🔢 **Version**: {health_data.get('version', 'Unknown')}
🌐 **API URL**: {self.api_url}
⏰ **Response Time**: Fast
                        """
                    else:
                        status_text = f"❌ API returned status code: {response.status}"
        except Exception as e:
            status_text = f"""
❌ **AI Assistant API - Connection Failed**

🔴 **Status**: Offline
🌐 **API URL**: {self.api_url}
❌ **Error**: {str(e)}

Please check if your FastAPI server is running!
            """
        
        await update.message.reply_text(status_text, parse_mode='Markdown')

    async def clear_history(self, update: Update, context) -> None:
        """Clear user's chat history"""
        user_id = str(update.effective_user.id)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(f"{self.api_url}/chat/history/{user_id}") as response:
                    if response.status == 200:
                        await update.message.reply_text("🗑️ Your chat history has been cleared!")
                    else:
                        await update.message.reply_text("❌ Failed to clear history. Please try again.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error clearing history: {str(e)}")

    async def show_topics(self, update: Update, context) -> None:
        """Show all available topics"""
        topics_text = """
📚 **Available Topics & Examples:**

🔄 **CI/CD & DevOps:**
• "What is CI/CD?"
• "Jenkins vs GitHub Actions"
• "DevOps best practices"

🐳 **Docker & Containers:**
• "Explain Docker containers"
• "Dockerfile best practices"
• "Docker vs Virtual Machines"

☸️ **Kubernetes:**
• "Kubernetes architecture"
• "How to deploy on K8s"
• "Kubernetes vs Docker Swarm"

☁️ **Cloud Platforms:**
• "AWS services overview"
• "Azure vs AWS vs GCP"
• "Cloud migration strategies"

🏗️ **Infrastructure as Code:**
• "What is Terraform?"
• "Ansible vs Terraform"
• "IaC best practices"

💻 **Programming:**
• "Python for DevOps"
• "API development"
• "Automation scripting"

Just ask me about any of these topics!
        """
        await update.message.reply_text(topics_text, parse_mode='Markdown')

    async def handle_callback(self, update: Update, context) -> None:
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        # Topic callbacks
        topic_questions = {
            "topic_cicd": "What is CI/CD and how does it work?",
            "topic_docker": "Explain Docker and containerization",
            "topic_k8s": "What is Kubernetes and how does it work?",
            "topic_aws": "Show me AWS services and cloud computing",
            "topic_terraform": "What is Terraform and Infrastructure as Code?",
            "topic_devops": "Explain DevOps culture and practices",
        }
        
        if callback_data in topic_questions:
            question = topic_questions[callback_data]
            await query.edit_message_text(f"🤔 You asked: *{question}*", parse_mode='Markdown')
            
            # Send the question to AI
            user_id = str(update.effective_user.id)
            ai_response = await self.get_ai_response(question, user_id)
            await context.bot.send_message(chat_id=query.from_user.id, text=ai_response, parse_mode='Markdown')
        
        elif callback_data == "help":
            await self.help_command(update, context)
        elif callback_data == "health":
            await self.health_command(update, context)

    async def handle_message(self, update: Update, context) -> None:
        """Handle user messages and send to AI"""
        user_message = update.message.text
        user_id = str(update.effective_user.id)
        user_name = update.effective_user.first_name or "User"
        
        # Log the message
        logger.info(f"Message from {user_name} (ID: {user_id}): {user_message}")
        
        # Send typing action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Get AI response
            ai_response = await self.get_ai_response(user_message, user_id)
            
            # Send response (split if too long for Telegram)
            await self.send_long_message(update, ai_response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            error_msg = """
❌ **Sorry, I encountered an error!**

This might be because:
• The AI API server is not running
• There's a network connection issue
• The API is overloaded

Try again in a moment, or use /health to check API status.
            """
            await update.message.reply_text(error_msg, parse_mode='Markdown')

    async def get_ai_response(self, message: str, user_id: str) -> str:
        """Get response from AI Assistant API"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "message": message,
                    "user_id": f"telegram_{user_id}"
                }
                
                async with session.post(
                    f"{self.api_url}/chat",
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', 'No response from AI')
                    else:
                        return f"❌ API Error: Status {response.status}"
                        
        except aiohttp.ClientError as e:
            return f"❌ Connection Error: {str(e)}\n\nMake sure your AI API is running at {self.api_url}"
        except Exception as e:
            return f"❌ Unexpected Error: {str(e)}"

    async def send_long_message(self, update: Update, message: str) -> None:
        """Send long messages by splitting them if necessary"""
        max_length = 4096  # Telegram's message limit
        
        if len(message) <= max_length:
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            # Split message into chunks
            chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await update.message.reply_text(chunk, parse_mode='Markdown')
                else:
                    await update.message.reply_text(f"*...continued:*\n\n{chunk}", parse_mode='Markdown')

    async def run(self):
        """Start the bot"""
        logger.info("Starting AI Assistant Telegram Bot...")
        
        # Check API health before starting
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/health") as response:
                    if response.status == 200:
                        logger.info("✅ AI API is healthy and ready!")
                    else:
                        logger.warning(f"⚠️ AI API returned status {response.status}")
        except Exception as e:
            logger.error(f"❌ Cannot connect to AI API: {e}")
            logger.error("Make sure your FastAPI server is running!")
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("🤖 Bot is running! Send /start to begin chatting.")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()


def main():
    """Main function to run the bot"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set your Telegram bot token!")
        print("1. Message @BotFather on Telegram")
        print("2. Create a new bot with /newbot")
        print("3. Copy the token and replace YOUR_BOT_TOKEN_HERE")
        return
    
    # Create and run bot
    bot = AIAssistantTelegramBot(TELEGRAM_BOT_TOKEN, AI_API_URL)
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")


if __name__ == "__main__":
    main()