"""Simple test client for free-claude-code server."""
import os
os.environ["ANTHROPIC_AUTH_TOKEN"] = "freecc"

import httpx
import time

# Wait for server to start
time.sleep(3)

try:
    # Test /health endpoint
    response = httpx.get("http://127.0.0.1:8082/health", timeout=5)
    print(f"Health check: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Health check failed: {e}")

try:
    # Test /v1/models endpoint
    headers = {"x-api-key": "freecc"}
    response = httpx.get("http://127.0.0.1:8082/v1/models", headers=headers, timeout=5)
    print(f"Models: {response.status_code} - {response.text[:200]}")
except Exception as e:
    print(f"Models check failed: {e}")
