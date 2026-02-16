# 🤖 AI Assistant - DevOps Expert Bot

A comprehensive AI Assistant API and Telegram Bot specializing in DevOps knowledge, built with FastAPI and featuring multiple interfaces for maximum accessibility.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Security](https://img.shields.io/badge/Security-Scanned-green.svg)
![Tests](https://img.shields.io/badge/Tests-13%2F13-success.svg)

## ✨ Features

### 🚀 **Core API**
- **FastAPI Framework**: High-performance async API with automatic OpenAPI docs
- **DevOps AI Expert**: Specialized knowledge in Docker, Kubernetes, CI/CD, Terraform, AWS
- **Multiple Response Formats**: JSON API responses and HTML pages
- **Interactive Documentation**: Swagger UI at `/docs` and ReDoc at `/redoc`
- **Health Monitoring**: Built-in health checks and status endpoints

### 🤖 **Telegram Bot Integration**
- **Real-time Messaging**: Instant DevOps assistance via Telegram
- **Command Support**: `/start`, `/help`, `/test` commands
- **Smart Buttons**: Quick access to common DevOps topics  
- **Error Handling**: Graceful error management with user-friendly messages
- **24/7 Availability**: Always-on bot for continuous support

### 🌐 **Web Interfaces**
- **Frontend Chat Page**: Standalone HTML/CSS/JS chat interface
- **React Components**: Reusable React chat components
- **Website Integration**: Easy embedding in existing websites
- **Mobile Responsive**: Works perfectly on all devices

### 🔒 **Security & Quality**
- **Vulnerability-Free**: All dependencies updated to secure versions
- **Security Scanning**: Automated vulnerability checks in CI/CD
- **Comprehensive Testing**: 13 test cases covering all functionality
- **CORS Support**: Secure cross-origin resource sharing
- **Input Validation**: Pydantic models for request/response validation

### 🚀 **DevOps Ready**
- **Docker Support**: Multi-stage builds with security best practices
- **GitHub Actions CI/CD**: Automated testing, security scanning, and deployment
- **Environment Configs**: Support for dev/staging/production environments
- **Health Checks**: Kubernetes-ready health endpoints
- **Logging**: Structured logging for monitoring and debugging

## 📋 Prerequisites

- **Python 3.10+** (FastAPI 0.129.0 requirement)
- **Docker & Docker Compose** (for containerization)  
- **Git** (for version control)
- **Telegram Account** (for bot features)

## 🛠️ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/ai-assistant.git
cd ai-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the API
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**🎉 Your AI Assistant is now running!**
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Chat Interface**: http://localhost:8000 (try asking "what is docker?")

### 3. Set Up Telegram Bot (Optional)
```bash
# Get your bot token from @BotFather on Telegram
# Edit telegram_bot.py and replace YOUR_TOKEN_HERE

# Install telegram dependencies
pip install -r telegram_requirements.txt

# Start the bot
python telegram_bot.py
```

## 🔥 AI Assistant Capabilities

Our AI specializes in DevOps and provides expert-level responses on:

### 🐳 **Containerization**
- **Docker**: Images, containers, Dockerfile best practices, multi-stage builds
- **Kubernetes**: Deployments, services, ingress, monitoring, security
- **Container Security**: Image scanning, runtime security, best practices

### 🔄 **CI/CD & Automation**
- **Pipeline Design**: GitHub Actions, Jenkins, GitLab CI, Azure DevOps
- **Build Strategies**: Blue-green deployments, rolling updates, canary releases
- **Infrastructure as Code**: Terraform, CloudFormation, ARM templates

### ☁️ **Cloud Platforms**  
- **AWS**: EC2, ECS, EKS, Lambda, S3, RDS, networking, security
- **Azure**: AKS, App Service, Functions, storage, networking
- **GCP**: GKE, Cloud Run, Cloud Functions, storage, networking

### 📊 **Monitoring & Operations**
- **Observability**: Prometheus, Grafana, ELK stack, APM tools
- **Log Management**: Centralized logging, log analysis, alerting
- **Incident Response**: SRE practices, troubleshooting, post-mortems

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| **GET** | `/` | Interactive HTML chat interface | Browser-friendly |
| **GET** | `/health` | Health check with status | `{"status": "healthy"}` |
| **POST** | `/chat` | Send message to AI assistant | DevOps Q&A |

### Chat API Example

**Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "explain kubernetes deployment strategies",
       "user_id": "devops-user"
     }'
```

**Response:**
```json
{
  "response": "Kubernetes offers several deployment strategies for updating applications:\n\n🔵 **Rolling Updates (Default)**\n- Gradually replaces old pods with new ones...",
  "timestamp": "2024-02-16T10:30:00Z",
  "user_id": "devops-user"
}
```

## 🤖 Telegram Bot Setup

### Step 1: Create Bot with BotFather
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`  
3. Choose name: `Your DevOps AI Assistant`
4. Choose username: `your_devops_ai_bot`
5. Copy the token provided

### Step 2: Configure & Start
```bash
# Update token in telegram_bot.py
TELEGRAM_BOT_TOKEN = "YOUR_ACTUAL_TOKEN_HERE"

# Start your API server first
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Start the Telegram bot  
python telegram_bot.py
```

### Step 3: Test Your Bot
- Find your bot on Telegram: `@your_devops_ai_bot`
- Send `/start` to begin
- Ask: `"what is docker?"` or `"explain kubernetes"`
- Use quick buttons for common topics!

## 🧪 Testing

Our comprehensive test suite covers all functionality:

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app test_app.py

# Test specific functionality
pytest test_app.py::TestAIResponseGeneration -v
```

**Test Coverage:**
- ✅ Health & status endpoints
- ✅ Chat functionality & AI responses  
- ✅ Error handling & validation
- ✅ CORS & security headers
- ✅ DevOps knowledge (Docker, Kubernetes, CI/CD, Terraform)

## 🐳 Docker Deployment

### Single Container
```bash
# Build image
docker build -t ai-assistant .

# Run container  
docker run -p 8000:8000 ai-assistant
```

### Docker Compose (Full Stack)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f ai-assistant

# Scale services
docker-compose up --scale ai-assistant=3 -d
```

## 🚀 Production Deployment

### GitHub Actions CI/CD

Our workflow automatically:
1. **🧪 Tests**: Runs 13 comprehensive tests on Python 3.10, 3.11, 3.12
2. **🔒 Security**: Scans dependencies for vulnerabilities  
3. **🐳 Build**: Creates optimized Docker images
4. **🚀 Deploy**: Deploys to staging/production
5. **✅ Verify**: Health checks confirm deployment success

### Environment Configuration

```bash
# .env file for local development
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-assistant
  template:
    spec:
      containers:
      - name: ai-assistant
        image: your-registry/ai-assistant:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
```

### 🚀 **Quick Production Deployment**

**Option 1: Use Our Deployment Script**
```bash
# Make script executable
chmod +x deploy-production.sh

# Deploy latest version
./deploy-production.sh

# Deploy specific version
./deploy-production.sh --image ghcr.io/your-username/ai-assistant:v1.0.0
```

**Option 2: Manual Docker Deployment**
```bash
# Pull and run latest image
docker pull ghcr.io/your-username/ai-assistant:latest
docker run -d --name ai-assistant-prod \
  --restart unless-stopped \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  ghcr.io/your-username/ai-assistant:latest
```

**Option 3: CI/CD Auto-Deployment**
```bash
# Just push to main branch - CI/CD handles the rest!
git push origin main

# GitHub Actions will:
# ✅ Run tests → 🔒 Security scan → 🐳 Build → 📦 Push → 🚀 Deploy
```

## 🌐 Website Integration

### HTML/JavaScript Integration
```html
<!-- Add to your website -->
<div id="ai-chat"></div>
<script>
async function askAI(question) {
  const response = await fetch('http://your-api.com/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: question })
  });
  return await response.json();
}
</script>
```

### React Component
```jsx
import { AIChat } from './components/AIChat';

function App() {
  return (
    <div>
      <h1>DevOps Help Desk</h1>
      <AIChat apiUrl="http://your-api.com" />
    </div>
  );
}
```

## � CI/CD Pipeline

Our automated CI/CD pipeline follows DevOps best practices:

```
┌──────────────┐
│   Developer  │
└──────┬───────┘
       │ git push
       ▼
┌───────────────────────┐
│     GitHub Repo       │
└────────┬──────────────┘
         │ triggers
         ▼
┌───────────────────────┐
│   GitHub Actions CI   │
│ 🧪 Install deps      │
│ 🧪 Run 13 tests      │
│ 🔒 Security scan     │
│ 🐳 Build Docker      │
│ 📦 Push to registry  │
└────────┬──────────────┘
         │ auto-deploy
         ▼
┌───────────────────────┐
│   Docker Registry     │
│   (GitHub Packages)   │
└────────┬──────────────┘
         │ pull & run
         ▼
┌───────────────────────┐
│     Production        │
│   🖥️ EC2 / VPS / VM   │
│   🏥 Health checks    │
│   🔄 Auto-restart     │
└───────────────────────┘
```

**🎯 Pipeline Stages:**
1. **🧪 Test**: Python 3.10-3.12, 13 comprehensive tests
2. **🔒 Security**: Dependency vulnerability scanning  
3. **🐳 Build**: Multi-arch Docker images (AMD64/ARM64)
4. **📦 Registry**: Push to GitHub Container Registry
5. **🚀 Deploy**: Automated deployment with health checks

## 📁 Project Structure

```
ai-assistant/
├── 🐍 app.py                     # Main FastAPI application
├── 📋 requirements.txt           # Python dependencies  
├── 🤖 telegram_bot.py           # Telegram bot implementation
├── 📋 telegram_requirements.txt  # Telegram bot dependencies
├── 🧪 test_app.py               # Comprehensive test suite
├── 🐳 Dockerfile               # Docker configuration
├── 🐳 docker-compose.yml       # Multi-service setup
├── 🌐 chat-frontend.html       # Standalone chat interface
├── ⚛️ AIChat.jsx               # React chat component  
├── 🎨 AIChat.css               # Styling for components
├── 📜 ai-widget.js             # Embeddable widget
├── 🚀 deploy-production.sh     # Production deployment script
├── ⚙️ .github/workflows/       # CI/CD automation
│   └── deploy.yml
├── 📚 README.md                # This documentation
└── 🔧 .env.example             # Environment template
```

## 🛡️ Security Features

### ✅ **Dependency Security**
- All dependencies updated to latest secure versions
- Automated vulnerability scanning in CI/CD
- Regular security audits with `pip-audit`

### ✅ **Application Security**  
- Input validation with Pydantic models
- CORS properly configured for production
- No sensitive data in logs or responses
- Rate limiting ready (easily configurable)

### ✅ **Container Security**
- Non-root user in Docker container
- Minimal base image (Python slim)
- Health checks for container orchestration
- Security-scanned base images

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes and add tests
4. **Run** tests: `pytest -v`
5. **Commit** changes: `git commit -m 'Add amazing feature'`
6. **Push** to branch: `git push origin feature/amazing-feature`  
7. **Create** a Pull Request

### Development Guidelines
- ✅ Add tests for new features
- ✅ Update documentation  
- ✅ Follow PEP 8 style guidelines
- ✅ Ensure security best practices

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Help

### 🔍 **Getting Help**
1. **Documentation**: Check `/docs` endpoint for API reference
2. **Issues**: Search [existing issues](../../issues) first
3. **New Issue**: Create [detailed issue](../../issues/new) if needed
4. **Telegram**: Test the bot for immediate DevOps help!

### 🐛 **Reporting Bugs**
Please include:
- Operating system and Python version
- Complete error messages and stack traces  
- Steps to reproduce the issue
- Expected vs actual behavior

### 💡 **Feature Requests**
We're always looking to improve! Suggest:
- New DevOps topics to cover
- Integration improvements  
- UI/UX enhancements
- Performance optimizations

## 🔗 Useful Resources

- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🤖 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🐳 [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- ☸️ [Kubernetes Documentation](https://kubernetes.io/docs/)
- 🔄 [GitHub Actions Guide](https://docs.github.com/en/actions)

---

## 🎯 **Ready to Get Started?**

1. **🚀 Quick Start**: `git clone` → `pip install` → `uvicorn app:app`
2. **🤖 Try Telegram Bot**: Get token from @BotFather → Configure → Launch  
3. **🌐 Web Integration**: Add to your website with our ready-to-use components
4. **🔧 Customize**: Extend with your own DevOps knowledge and integrations

**Made with ❤️ for the DevOps Community**

*Your AI-powered DevOps assistant is just one command away!* 🚀
*Your AI-powered DevOps assistant is just one command away!* 🚀