# AI Assistant API

A powerful AI Assistant API built with FastAPI, featuring containerization with Docker and automated CI/CD deployment.

## 🚀 Features

- **FastAPI Framework**: High-performance, easy-to-use, fast to code
- **Interactive API Documentation**: Automatic OpenAPI/Swagger documentation
- **Docker Support**: Containerized application with multi-stage builds
- **CI/CD Pipeline**: GitHub Actions workflow for testing and deployment
- **Health Checks**: Built-in health monitoring endpoints
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **Logging**: Comprehensive logging configuration
- **Security**: Security scanning and best practices

## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Git

## 🛠️ Local Development

### 1. Clone the repository
```bash
git clone <repository-url>
cd ai-assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker Deployment

### Build and run with Docker
```bash
# Build the image
docker build -t ai-assistant .

# Run the container
docker run -p 8000:8000 ai-assistant
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📊 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API information |
| GET | `/health` | Health check endpoint |
| POST | `/chat` | Chat with AI assistant |
| GET | `/chat/history/{user_id}` | Get user's chat history |
| DELETE | `/chat/history/{user_id}` | Clear user's chat history |

### Example Usage

#### Chat with Assistant
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Hello, how are you?",
       "user_id": "user123"
     }'
```

#### Health Check
```bash
curl http://localhost:8000/health
```

## 🧪 Testing

### Run tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest -v

# Run with coverage
pip install pytest-cov
pytest --cov=app tests/
```

## 🚀 Deployment

### GitHub Actions CI/CD

The project includes a comprehensive GitHub Actions workflow that:

1. **Tests**: Runs tests on multiple Python versions
2. **Security Scanning**: Scans for security vulnerabilities
3. **Build & Push**: Builds Docker images and pushes to registry
4. **Deploy**: Deploys to staging and production environments
5. **Health Checks**: Verifies deployment success
6. **Notifications**: Sends deployment status notifications

### Environment Variables

Create a `.env` file for local development:

```env
# Application
ENVIRONMENT=development
LOG_LEVEL=info
API_HOST=0.0.0.0
API_PORT=8000

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://postgres:password123@localhost:5432/ai_assistant

# Redis (if using Redis)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
```

### Production Deployment

1. **Set up secrets in GitHub**:
   - `PRODUCTION_URL`: Your production API URL
   - Add any additional secrets needed for deployment

2. **Configure deployment targets**:
   - Update the deployment steps in `.github/workflows/deploy.yml`
   - Add your specific deployment commands (kubectl, helm, etc.)

## 📁 Project Structure

```
ai-assistant/
│
├── app.py                     # Main FastAPI application
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Multi-service Docker setup
├── .github/
│   └── workflows/
│       └── deploy.yml         # CI/CD pipeline
├── README.md                  # Project documentation
├── .env                       # Environment variables (create locally)
├── .gitignore                 # Git ignore rules
└── tests/                     # Test files (create as needed)
    ├── __init__.py
    ├── test_main.py
    └── test_endpoints.py
```

## 🔧 Configuration

### FastAPI Configuration

The application is configured with:
- **Title**: AI Assistant API
- **Version**: 1.0.0
- **Docs URL**: `/docs`
- **ReDoc URL**: `/redoc`
- **CORS**: Enabled for all origins (configure for production)

### Docker Configuration

- **Base Image**: Python 3.11 slim
- **Port**: 8000
- **Health Check**: Included
- **Non-root user**: Security best practice
- **Multi-stage build ready**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](http://localhost:8000/docs)
2. Search existing [issues](../../issues)
3. Create a new [issue](../../issues/new) if needed

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

**Made with ❤️ using FastAPI**