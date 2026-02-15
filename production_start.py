#!/usr/bin/env python3
"""
Production-ready startup script for 24/7 operation
"""
import uvicorn
import os
from app import app

if __name__ == "__main__":
    # Production configuration
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        workers=4,  # Multiple workers for better performance
        loop="uvloop",  # High-performance event loop
        http="httptools",  # High-performance HTTP parser
        log_level="info",
        access_log=True,
        reload=False,  # Disable reload in production
        proxy_headers=True,  # For reverse proxy support
        forwarded_allow_ips="*"
    )