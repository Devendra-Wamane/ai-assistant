import React, { useState, useEffect, useRef } from 'react';
import './AIChat.css';

const AIChat = ({ apiUrl = 'http://127.0.0.1:8000' }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: '👋 Hello! I\'m your AI Assistant. How can I help you today?',
      type: 'ai',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const userId = useRef(`react_user_${Date.now()}`);

  // Check API connection on component mount
  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const checkConnection = async () => {
    try {
      const response = await fetch(`${apiUrl}/health`);
      if (response.ok) {
        setIsConnected(true);
        setError(null);
      } else {
        throw new Error('Health check failed');
      }
    } catch (error) {
      setIsConnected(false);
      setError('Cannot connect to AI Assistant API');
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !isConnected || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage.trim(),
      type: 'user',
      timestamp: new Date()
    };

    // Add user message
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.text,
          user_id: userId.current
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        text: data.response,
        type: 'ai',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message. Please try again.');
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        type: 'ai',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="ai-chat-container">
      {/* Header */}
      <div className="ai-chat-header">
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        </div>
        <h2>🤖 AI Assistant</h2>
        <p>React-powered chat interface</p>
      </div>

      {/* Messages */}
      <div className="ai-chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.type}-message ${message.isError ? 'error' : ''}`}
          >
            <div className="message-content">{message.text}</div>
            <div className="message-timestamp">
              {formatTime(message.timestamp)}
            </div>
          </div>
        ))}
        
        {/* Loading indicator */}
        {isLoading && (
          <div className="message ai-message loading">
            <div className="loading-dots">
              <span>AI is thinking</span>
              <div className="dots">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Error display */}
      {error && (
        <div className="error-banner">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {/* Input */}
      <div className="ai-chat-input">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
          disabled={!isConnected || isLoading}
          maxLength={1000}
        />
        <button
          onClick={sendMessage}
          disabled={!inputMessage.trim() || !isConnected || isLoading}
        >
          {isLoading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
};

export default AIChat;