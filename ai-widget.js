// AI Assistant Integration Library
// Drop-in solution for any website

class AIAssistantWidget {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || 'http://127.0.0.1:8000';
        this.userId = options.userId || 'widget_user_' + Date.now();
        this.theme = options.theme || 'default';
        this.position = options.position || 'bottom-right';
        this.autoOpen = options.autoOpen || false;
        
        this.isOpen = false;
        this.isMinimized = !this.autoOpen;
        
        this.createWidget();
        this.injectStyles();
        this.setupEventListeners();
        this.checkConnection();
    }

    createWidget() {
        // Create widget container
        this.widget = document.createElement('div');
        this.widget.className = `ai-widget ${this.position}`;
        this.widget.innerHTML = `
            <div class="ai-widget-toggle" id="aiWidgetToggle">
                <div class="ai-widget-icon">🤖</div>
                <div class="ai-widget-notification" id="aiNotification" style="display: none;">1</div>
            </div>
            
            <div class="ai-widget-chat" id="aiWidgetChat" ${this.isMinimized ? 'style="display: none;"' : ''}>
                <div class="ai-widget-header">
                    <h3>AI Assistant</h3>
                    <div class="ai-widget-controls">
                        <button class="ai-widget-minimize" id="aiMinimize">−</button>
                        <button class="ai-widget-close" id="aiClose">×</button>
                    </div>
                </div>
                
                <div class="ai-widget-messages" id="aiWidgetMessages">
                    <div class="ai-message">
                        <div class="message-content">👋 Hi! I'm here to help. What can I do for you?</div>
                        <div class="message-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                </div>
                
                <div class="ai-widget-input">
                    <input type="text" id="aiWidgetInput" placeholder="Ask me anything..." maxlength="500">
                    <button id="aiWidgetSend">Send</button>
                </div>
                
                <div class="ai-widget-status">
                    <span id="aiWidgetStatus">🔴 Connecting...</span>
                </div>
            </div>
        `;

        document.body.appendChild(this.widget);
        
        // Store references
        this.elements = {
            toggle: document.getElementById('aiWidgetToggle'),
            chat: document.getElementById('aiWidgetChat'),
            messages: document.getElementById('aiWidgetMessages'),
            input: document.getElementById('aiWidgetInput'),
            send: document.getElementById('aiWidgetSend'),
            minimize: document.getElementById('aiMinimize'),
            close: document.getElementById('aiClose'),
            status: document.getElementById('aiWidgetStatus'),
            notification: document.getElementById('aiNotification')
        };
    }

    injectStyles() {
        const styles = `
            .ai-widget {
                position: fixed;
                z-index: 10000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .ai-widget.bottom-right {
                bottom: 20px;
                right: 20px;
            }
            
            .ai-widget.bottom-left {
                bottom: 20px;
                left: 20px;
            }
            
            .ai-widget-toggle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                transition: all 0.3s ease;
                position: relative;
            }
            
            .ai-widget-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 25px rgba(0,0,0,0.2);
            }
            
            .ai-widget-icon {
                font-size: 24px;
                color: white;
            }
            
            .ai-widget-notification {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #ff4444;
                color: white;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                font-size: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .ai-widget-chat {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .ai-widget-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .ai-widget-header h3 {
                margin: 0;
                font-size: 16px;
            }
            
            .ai-widget-controls {
                display: flex;
                gap: 5px;
            }
            
            .ai-widget-controls button {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .ai-widget-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            .ai-message, .user-message {
                max-width: 80%;
                padding: 10px 12px;
                border-radius: 15px;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .ai-message {
                background: #f0f0f0;
                align-self: flex-start;
                border-bottom-left-radius: 5px;
            }
            
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                align-self: flex-end;
                border-bottom-right-radius: 5px;
            }
            
            .message-time {
                font-size: 11px;
                opacity: 0.7;
                margin-top: 5px;
            }
            
            .ai-widget-input {
                padding: 15px;
                border-top: 1px solid #eee;
                display: flex;
                gap: 10px;
            }
            
            .ai-widget-input input {
                flex: 1;
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 10px 15px;
                outline: none;
                font-size: 14px;
            }
            
            .ai-widget-input button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
            }
            
            .ai-widget-status {
                padding: 8px 15px;
                font-size: 12px;
                background: #f8f8f8;
                border-top: 1px solid #eee;
                text-align: center;
            }
            
            @media (max-width: 480px) {
                .ai-widget-chat {
                    width: calc(100vw - 40px);
                    right: -10px;
                }
            }
        `;

        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    setupEventListeners() {
        // Toggle chat
        this.elements.toggle.addEventListener('click', () => {
            this.toggleChat();
        });

        // Minimize
        this.elements.minimize.addEventListener('click', () => {
            this.minimizeChat();
        });

        // Close
        this.elements.close.addEventListener('click', () => {
            this.closeChat();
        });

        // Send message
        this.elements.send.addEventListener('click', () => {
            this.sendMessage();
        });

        // Enter key
        this.elements.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    toggleChat() {
        if (this.isMinimized) {
            this.showChat();
        } else {
            this.minimizeChat();
        }
    }

    showChat() {
        this.elements.chat.style.display = 'flex';
        this.isMinimized = false;
        this.elements.notification.style.display = 'none';
        this.elements.input.focus();
    }

    minimizeChat() {
        this.elements.chat.style.display = 'none';
        this.isMinimized = true;
    }

    closeChat() {
        this.minimizeChat();
    }

    async checkConnection() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (response.ok) {
                this.elements.status.innerHTML = '🟢 Connected';
                return true;
            }
        } catch (error) {
            this.elements.status.innerHTML = '🔴 Disconnected';
            return false;
        }
    }

    async sendMessage() {
        const message = this.elements.input.value.trim();
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        this.elements.input.value = '';
        
        // Show typing indicator
        this.addTypingIndicator();

        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: this.userId
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            // Add AI response
            this.addMessage(data.response, 'ai');

            // Show notification if chat is minimized
            if (this.isMinimized) {
                this.elements.notification.style.display = 'flex';
            }

        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'ai');
        }
    }

    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        messageDiv.innerHTML = `
            <div class="message-content">${this.escapeHtml(content)}</div>
            <div class="message-time">${new Date().toLocaleTimeString()}</div>
        `;
        
        this.elements.messages.appendChild(messageDiv);
        this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
    }

    addTypingIndicator() {
        this.typingIndicator = document.createElement('div');
        this.typingIndicator.className = 'ai-message typing';
        this.typingIndicator.innerHTML = '<div class="message-content">AI is typing...</div>';
        this.elements.messages.appendChild(this.typingIndicator);
        this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
    }

    removeTypingIndicator() {
        if (this.typingIndicator && this.typingIndicator.parentNode) {
            this.typingIndicator.parentNode.removeChild(this.typingIndicator);
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Auto-initialize if script is loaded with data attributes
document.addEventListener('DOMContentLoaded', () => {
    const script = document.querySelector('script[data-ai-assistant]');
    if (script) {
        const apiUrl = script.getAttribute('data-api-url') || 'http://127.0.0.1:8000';
        const position = script.getAttribute('data-position') || 'bottom-right';
        const autoOpen = script.getAttribute('data-auto-open') === 'true';
        
        new AIAssistantWidget({
            apiUrl,
            position,
            autoOpen
        });
    }
});

// Export for manual initialization
if (typeof window !== 'undefined') {
    window.AIAssistantWidget = AIAssistantWidget;
}