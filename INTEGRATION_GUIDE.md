# 🚀 AI Assistant Frontend Integration Guide

Your AI Assistant API is now ready to power websites with AI! Here are complete examples for different integration methods:

## 📁 Files Created

- `chat-frontend.html` - Complete standalone chat interface
- `AIChat.jsx` - React component for modern web apps  
- `AIChat.css` - Styles for React component
- `ai-widget.js` - Drop-in widget for any website

## 🌟 Integration Options

### 1️⃣ **Standalone Chat Page**

Open `chat-frontend.html` directly in your browser for a beautiful full-page chat interface.

```bash
# Start your AI API first
cd /home/devendra/Desktop/devops/ai-assistant
source venv/bin/activate
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Then open chat-frontend.html in browser
```

**Features:**
- ✅ Beautiful gradient design
- ✅ Real-time connection status
- ✅ Loading indicators  
- ✅ Error handling
- ✅ Mobile responsive
- ✅ Auto-scroll messages

---

### 2️⃣ **React Component Integration**

For modern React applications:

```jsx
import React from 'react';
import AIChat from './AIChat';
import './AIChat.css';

function App() {
  return (
    <div className="App">
      <h1>My Website</h1>
      
      {/* Add AI Chat anywhere */}
      <AIChat 
        apiUrl="http://127.0.0.1:8000"
      />
    </div>
  );
}

export default App;
```

**Props Available:**
- `apiUrl` - Your API URL (default: http://127.0.0.1:8000)
- Custom styling through CSS classes

---

### 3️⃣ **Drop-in Widget (Any Website)**

Add AI chat to ANY existing website with just 2 lines of code:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Existing Website</title>
</head>
<body>
    <h1>Welcome to My Site</h1>
    <p>Regular website content...</p>
    
    <!-- Add these 2 lines anywhere in your HTML -->
    <script src="ai-widget.js" 
            data-ai-assistant 
            data-api-url="http://127.0.0.1:8000"
            data-position="bottom-right"
            data-auto-open="false"></script>
</body>
</html>
```

**Widget Options:**
- `data-api-url` - Your API endpoint
- `data-position` - "bottom-right" or "bottom-left"  
- `data-auto-open` - "true" or "false"

---

### 4️⃣ **Custom JavaScript Integration**

For custom implementations:

```javascript
// Simple fetch example
async function askAI(question) {
    try {
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: question,
                user_id: 'my_website_user'
            })
        });

        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('AI Error:', error);
        return 'Sorry, I encountered an error.';
    }
}

// Usage
askAI("What is Docker?").then(response => {
    document.getElementById('ai-response').textContent = response;
});
```

---

## 🎯 **Real-World Use Cases**

### **E-commerce Site**
```javascript
// Product recommendation
const product = await askAI("Recommend laptops under $1000");
```

### **Documentation Site**
```javascript
// Help with docs
const help = await askAI("How do I install this software?");
```

### **Blog/Content Site**
```javascript
// Content summarization
const summary = await askAI("Summarize this article about AI");
```

### **Educational Platform**
```javascript
// Learning assistance  
const explanation = await askAI("Explain machine learning simply");
```

---

## 🛠️ **API Endpoints Available**

Your AI Assistant provides these endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Beautiful home page |
| `POST` | `/chat` | Send messages to AI |
| `GET` | `/health` | Check API status |
| `GET` | `/docs` | Interactive documentation |
| `GET` | `/chat/history/{user_id}` | Get chat history |
| `DELETE` | `/chat/history/{user_id}` | Clear chat history |

---

## 🔧 **Chat API Usage**

### **Request Format:**
```javascript
{
    "message": "Your question here",
    "user_id": "optional_user_id"
}
```

### **Response Format:**
```javascript
{
    "response": "AI's answer",
    "timestamp": "2026-02-15T12:30:45.123456",
    "user_id": "user_123"
}
```

---

## 🎨 **Customization**

### **Change Widget Colors:**
```css
.ai-widget-toggle {
    background: linear-gradient(135deg, #your-color1, #your-color2) !important;
}
```

### **Custom API Error Handling:**
```javascript
try {
    const response = await fetch('/chat', {...});
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
} catch (error) {
    // Your custom error handling
    showCustomErrorMessage(error.message);
}
```

---

## 🚀 **Quick Test**

1. **Start your AI API:**
```bash
cd /home/devendra/Desktop/devops/ai-assistant
source venv/bin/activate  
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

2. **Test the API:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello AI!", "user_id": "test"}'
```

3. **Open any HTML file** and add the widget script

---

## 🌐 **Production Deployment**

For production websites:

1. **Change API URL** from `127.0.0.1:8000` to your domain
2. **Enable CORS** for your frontend domain
3. **Use HTTPS** for secure connections
4. **Add rate limiting** for protection

---

## 💡 **Next Steps**

- ✅ **Customize styling** to match your brand
- ✅ **Add authentication** for user-specific chats
- ✅ **Integrate with your database** for persistence
- ✅ **Add file upload** capabilities
- ✅ **Connect to external APIs** for enhanced features

**Your AI Assistant is now ready to power any website! 🤖✨**