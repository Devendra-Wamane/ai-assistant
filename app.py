from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="AI Assistant API",
    description="A powerful AI Assistant API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    user_id: str

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str

# In-memory storage for demo (use database in production)
conversation_history = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Assistant API</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                line-height: 1.6;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                text-align: center;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .version {
                font-size: 1.2em;
                opacity: 0.8;
                margin: 20px 0;
            }
            .links {
                margin-top: 30px;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                margin: 10px;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            .btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .feature {
                margin: 20px 0;
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Assistant API</h1>
            <div class="version">Version 1.0.0</div>
            
            <div class="feature">
                <h3>🚀 Welcome to Your Intelligent API</h3>
                <p>A powerful FastAPI-based AI Assistant ready to help you with conversations, queries, and more!</p>
            </div>
            
            <div class="links">
                <a href="/docs" class="btn">📚 Interactive Docs</a>
                <a href="/redoc" class="btn">📖 ReDoc</a>
                <a href="/health" class="btn">❤️ Health Check</a>
            </div>
            
            <div class="feature">
                <h3>✨ Features</h3>
                <p>• Chat conversations with history<br>
                • RESTful API endpoints<br>
                • Real-time health monitoring<br>
                • Interactive documentation</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="AI Assistant API is running",
        version="1.0.0"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(message: ChatMessage):
    """
    Chat with the AI Assistant
    """
    try:
        # Initialize conversation history for user
        if message.user_id not in conversation_history:
            conversation_history[message.user_id] = []
        
        # Add user message to history
        conversation_history[message.user_id].append({
            "role": "user", 
            "content": message.message
        })
        
        # Simple response logic (replace with actual AI model)
        response_text = generate_ai_response(message.message)
        
        # Add AI response to history
        conversation_history[message.user_id].append({
            "role": "assistant", 
            "content": response_text
        })
        
        from datetime import datetime
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat(),
            user_id=message.user_id
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/chat/history/{user_id}")
async def get_chat_history(user_id: str):
    """Get chat history for a user"""
    if user_id not in conversation_history:
        return {"history": []}
    
    return {"history": conversation_history[user_id]}

@app.delete("/chat/history/{user_id}")
async def clear_chat_history(user_id: str):
    """Clear chat history for a user"""
    if user_id in conversation_history:
        del conversation_history[user_id]
    
    return {"message": f"Chat history cleared for user {user_id}"}

def generate_ai_response(message: str) -> str:
    """
    Enhanced AI response with comprehensive DevOps and technical knowledge
    """
    message_lower = message.lower()
    
    # Greetings
    if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello! I'm your AI Assistant specializing in DevOps, Cloud, and Software Development. I can help you with CI/CD, Docker, Kubernetes, AWS, Terraform, and much more. What would you like to learn about?"
    
    # CI/CD Topics
    elif any(word in message_lower for word in ["cicd", "ci/cd", "ci cd", "continuous integration", "continuous deployment"]):
        return """🚀 **CI/CD (Continuous Integration/Continuous Deployment)** is a DevOps practice that automates the software development lifecycle:

**🔄 Continuous Integration (CI):**
- Developers frequently merge code changes into a central repository
- Automated builds and tests run on every commit
- Early detection of integration issues
- Tools: Jenkins, GitHub Actions, GitLab CI, CircleCI

**🚀 Continuous Deployment (CD):**
- Automated deployment of tested code to production
- Reduces manual intervention and human errors
- Faster time-to-market for features
- Rollback capabilities for quick recovery

**📋 Typical CI/CD Pipeline:**
1. **Code Commit** → Developer pushes code
2. **Build** → Compile/package the application
3. **Test** → Run unit, integration, and security tests
4. **Deploy to Staging** → Test in production-like environment
5. **Deploy to Production** → Release to users
6. **Monitor** → Track application performance

**🛠️ Popular CI/CD Tools:**
- GitHub Actions (Free, integrated with GitHub)
- Jenkins (Open-source, highly configurable)
- GitLab CI/CD (Built into GitLab)
- Azure DevOps (Microsoft ecosystem)
- AWS CodePipeline (AWS native)

**💡 Benefits:**
- Faster delivery cycles
- Improved code quality
- Reduced deployment risks
- Better collaboration
- Automated testing and security

Would you like me to explain any specific part of CI/CD in more detail?"""
    
    # Docker Topics
    elif any(word in message_lower for word in ["docker", "container", "dockerfile", "containerization"]):
        return """🐳 **Docker** is a containerization platform that packages applications with their dependencies:

**📦 What are Containers?**
- Lightweight, standalone packages that include everything needed to run an application
- Share the host OS kernel (unlike VMs)
- Consistent across different environments

**🔧 Key Docker Components:**
- **Docker Engine**: Runtime that manages containers
- **Dockerfile**: Text file with instructions to build images
- **Docker Image**: Read-only template for creating containers
- **Docker Hub**: Public registry for sharing images

**📋 Common Docker Commands:**
```bash
docker build -t myapp .          # Build image
docker run -p 8000:8000 myapp    # Run container
docker ps                        # List running containers
docker images                    # List available images
docker stop <container_id>       # Stop container
```

**🚀 Benefits:**
- Environment consistency
- Easy deployment and scaling
- Resource efficiency
- Version control for infrastructure
- Microservices architecture support

Need help with Dockerfile creation or Docker commands?"""
    
    # Kubernetes Topics
    elif any(word in message_lower for word in ["kubernetes", "k8s", "kubectl", "pods", "cluster"]):
        return """☸️ **Kubernetes (K8s)** is a container orchestration platform for automating deployment, scaling, and management:

**🎯 Core Concepts:**
- **Pod**: Smallest deployable unit (one or more containers)
- **Service**: Stable network endpoint for pods
- **Deployment**: Manages replica sets and rolling updates
- **Namespace**: Virtual clusters within a physical cluster
- **ConfigMap**: Configuration data for applications
- **Secret**: Sensitive data like passwords and tokens

**🏗️ Architecture:**
- **Master Node**: Control plane (API server, scheduler, controller)
- **Worker Nodes**: Run application workloads
- **etcd**: Distributed key-value store for cluster data

**📋 Essential kubectl Commands:**
```bash
kubectl get pods                 # List all pods
kubectl apply -f deployment.yaml # Apply configuration
kubectl scale deployment myapp --replicas=5
kubectl logs <pod-name>         # View pod logs
kubectl exec -it <pod> -- /bin/bash  # Shell into pod
```

**💪 Benefits:**
- Auto-scaling based on demand
- Self-healing (restarts failed containers)
- Rolling updates with zero downtime
- Load balancing and service discovery
- Multi-cloud and hybrid cloud support

Want to learn about specific Kubernetes resources or deployment strategies?"""
    
    # AWS Topics
    elif any(word in message_lower for word in ["aws", "amazon", "cloud", "ec2", "s3", "lambda"]):
        return """☁️ **AWS (Amazon Web Services)** is a comprehensive cloud platform offering 200+ services:

**🔥 Core Services:**
- **EC2**: Virtual servers in the cloud
- **S3**: Object storage service
- **RDS**: Managed relational databases
- **Lambda**: Serverless compute functions
- **VPC**: Virtual private cloud networking
- **IAM**: Identity and Access Management
- **CloudFormation**: Infrastructure as Code

**🏗️ Service Categories:**
- **Compute**: EC2, Lambda, ECS, EKS
- **Storage**: S3, EBS, EFS
- **Database**: RDS, DynamoDB, ElastiCache
- **Networking**: VPC, CloudFront, Route 53
- **Security**: IAM, WAF, Shield, GuardDuty

**💰 Pricing Models:**
- **On-Demand**: Pay for what you use
- **Reserved Instances**: 1-3 year commitments for discounts
- **Spot Instances**: Bid for unused capacity
- **Savings Plans**: Flexible pricing for compute usage

**📋 Getting Started:**
1. Create AWS account
2. Set up billing alerts
3. Configure IAM users and roles
4. Launch your first EC2 instance
5. Learn AWS CLI and SDKs

Which AWS service would you like to explore further?"""
    
    # Terraform Topics
    elif any(word in message_lower for word in ["terraform", "infrastructure as code", "iac", "hcl"]):
        return """🏗️ **Terraform** is an Infrastructure as Code (IaC) tool for building, changing, and versioning infrastructure:

**📝 Key Features:**
- **Declarative**: Describe desired state, not steps
- **Multi-Cloud**: Works with AWS, Azure, GCP, and 1000+ providers
- **State Management**: Tracks resource state
- **Plan & Apply**: Preview changes before execution
- **Modules**: Reusable infrastructure components

**🔧 Core Commands:**
```bash
terraform init      # Initialize working directory
terraform plan      # Create execution plan
terraform apply     # Execute the plan
terraform destroy   # Destroy infrastructure
terraform validate  # Validate configuration
terraform fmt       # Format code
```

**📋 Basic Structure:**
```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "web" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  
  tags = {
    Name = "HelloWorld"
  }
}
```

**💡 Benefits:**
- Version-controlled infrastructure
- Consistent environments
- Reduced human errors
- Cost optimization through automation
- Team collaboration on infrastructure

Need help writing Terraform configurations for specific resources?"""
    
    # DevOps Topics
    elif any(word in message_lower for word in ["devops", "automation", "monitoring", "deployment"]):
        return """🔄 **DevOps** is a culture and practice that combines Development and Operations teams:

**🎯 Core Principles:**
- **Collaboration**: Break down silos between dev and ops
- **Automation**: Automate repetitive tasks
- **Monitoring**: Continuous feedback and improvement
- **Speed**: Faster delivery without sacrificing quality

**🛠️ DevOps Toolchain:**
- **Version Control**: Git, GitHub, GitLab
- **CI/CD**: Jenkins, GitHub Actions, GitLab CI
- **Containerization**: Docker, Podman
- **Orchestration**: Kubernetes, Docker Swarm
- **Infrastructure**: Terraform, Ansible, Pulumi
- **Monitoring**: Prometheus, Grafana, ELK Stack
- **Cloud**: AWS, Azure, GCP

**📈 DevOps Lifecycle:**
1. **Plan** → Requirements and project planning
2. **Code** → Development and version control
3. **Build** → Compile and package
4. **Test** → Automated testing
5. **Release** → Deployment preparation
6. **Deploy** → Production deployment
7. **Operate** → Monitor and maintain
8. **Monitor** → Feedback and improvement

**💪 Benefits:**
- Faster time-to-market
- Improved collaboration
- Higher deployment frequency
- Lower failure rates
- Faster recovery times

Which DevOps practice would you like to dive deeper into?"""
    
    # Programming Topics
    elif any(word in message_lower for word in ["python", "javascript", "react", "node", "programming", "code"]):
        return """💻 **Programming & Development** - I can help with various programming topics:

**🐍 Python:**
- FastAPI, Django, Flask web frameworks
- Data science with pandas, numpy
- Automation and scripting
- DevOps tools and AWS SDKs

**🌐 JavaScript/Web:**
- React, Vue.js, Angular frameworks
- Node.js for backend development
- API development and integration
- Modern ES6+ features

**☁️ Cloud Development:**
- AWS Lambda functions
- Serverless architecture
- API Gateway integration
- Database connectivity

**🔧 DevOps Programming:**
- Infrastructure as Code scripts
- CI/CD pipeline configurations
- Automation scripts
- Monitoring and alerting tools

**📋 Best Practices:**
- Version control with Git
- Code testing and quality
- Documentation
- Security considerations
- Performance optimization

What specific programming topic or technology would you like to explore?"""
    
    # Farewell
    elif any(word in message_lower for word in ["bye", "goodbye", "see you", "thanks", "thank you"]):
        return "You're welcome! Happy to help with your DevOps journey. Feel free to ask anytime about CI/CD, Docker, Kubernetes, AWS, or any other tech topics. Good luck with your projects! 🚀"
    
    # Help
    elif "help" in message_lower:
        return """🤖 **I'm your DevOps & Cloud AI Assistant!** I can help you with:

**🔧 DevOps & CI/CD:**
- Jenkins, GitHub Actions, GitLab CI
- Pipeline design and best practices
- Automation strategies

**🐳 Containerization:**
- Docker fundamentals and advanced topics
- Kubernetes orchestration
- Container security and optimization

**☁️ Cloud Platforms:**
- AWS services and architecture
- Azure and GCP basics
- Multi-cloud strategies

**🏗️ Infrastructure as Code:**
- Terraform configurations
- Ansible playbooks
- CloudFormation templates

**💻 Programming:**
- Python, JavaScript, and web development
- API development and integration
- Automation scripting

**📊 Monitoring & Security:**
- Application monitoring
- Security best practices
- Performance optimization

Just ask me anything like:
- "How do I set up a CI/CD pipeline?"
- "Explain Docker vs Kubernetes"
- "Show me AWS Lambda examples"
- "Create a Terraform script for EC2"

What would you like to learn about?"""
    
    # Default enhanced response
    else:
        return f"""I understand you're asking about: "{message}"

While I'm designed to be most helpful with DevOps, Cloud, and Development topics, I'll do my best to assist you!

🔍 **For better answers, try asking about:**
- CI/CD pipelines and automation
- Docker and containerization  
- Kubernetes orchestration
- AWS, Azure, or cloud services
- Infrastructure as Code (Terraform)
- Programming (Python, JavaScript)
- DevOps best practices

📝 **Example questions:**
- "How do I deploy with Docker?"
- "What is Kubernetes used for?"
- "Show me a CI/CD pipeline example"
- "Explain AWS services"

Feel free to rephrase your question or ask about any DevOps/Cloud topic!"""

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )