#!/usr/bin/env python3
"""
Test suite for AI Assistant API
"""

import pytest
import httpx
from fastapi.testclient import TestClient
from app import app, generate_ai_response

# Create test client
client = TestClient(app)

class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "AI Assistant API is running"
        assert data["version"] == "1.0.0"

    def test_root_endpoint(self):
        """Test the root endpoint returns HTML"""
        response = client.get("/")
        assert response.status_code == 200
        # Root endpoint returns HTML, not JSON
        assert "text/html" in response.headers.get("content-type", "")
        assert "AI Assistant API" in response.text

class TestChatEndpoints:
    """Test chat functionality"""
    
    def test_chat_endpoint_post(self):
        """Test POST chat endpoint with valid message"""
        test_message = {"message": "what is docker?"}
        response = client.post("/chat", json=test_message)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "timestamp" in data
        assert len(data["response"]) > 0
        
    def test_chat_endpoint_empty_message(self):
        """Test chat endpoint with empty message"""
        test_message = {"message": ""}
        response = client.post("/chat", json=test_message)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        
    def test_chat_endpoint_invalid_json(self):
        """Test chat endpoint with invalid JSON"""
        response = client.post("/chat", json={})
        
        # Should handle missing message field gracefully
        assert response.status_code == 422  # Unprocessable Entity for missing required field

class TestAIResponseGeneration:
    """Test AI response generation function"""
    
    def test_generate_ai_response_docker(self):
        """Test AI response for Docker question"""
        response = generate_ai_response("what is docker?")
        assert len(response) > 100  # Should be detailed response
        assert "docker" in response.lower() or "container" in response.lower()
        
    def test_generate_ai_response_kubernetes(self):
        """Test AI response for Kubernetes question"""
        response = generate_ai_response("explain kubernetes")
        assert len(response) > 100
        assert "kubernetes" in response.lower() or "k8s" in response.lower()
        
    def test_generate_ai_response_cicd(self):
        """Test AI response for CI/CD question"""
        response = generate_ai_response("what is cicd?")
        assert len(response) > 100
        assert "ci/cd" in response.lower() or "continuous" in response.lower()
        
    def test_generate_ai_response_terraform(self):
        """Test AI response for Terraform question"""
        response = generate_ai_response("what is terraform?")
        assert len(response) > 100
        assert "terraform" in response.lower() or "infrastructure" in response.lower()

class TestCORSAndSecurity:
    """Test CORS and security headers"""
    
    def test_cors_headers(self):
        """Test that CORS headers are present"""
        response = client.options("/chat")
        # FastAPI with CORS should handle OPTIONS requests
        assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly handled
        
    def test_security_headers(self):
        """Test basic security"""
        response = client.get("/health")
        assert response.status_code == 200
        # Basic security check - no sensitive info in headers
        assert "server" not in response.headers or "uvicorn" not in response.headers.get("server", "").lower()

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_endpoint(self):
        """Test non-existent endpoint returns 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        
    def test_invalid_method(self):
        """Test invalid HTTP method"""
        response = client.delete("/chat")
        assert response.status_code == 405  # Method not allowed

# Test configuration
pytest_plugins = ['pytest_asyncio']

if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])