"""Test script to start server and verify it's listening."""
import os
os.environ["ANTHROPIC_AUTH_TOKEN"] = "freecc"

from server import app
print("App created successfully")
print("Routes:", [r.path for r in app.routes])

import uvicorn
if __name__ == "__main__":
    print("Starting server on 127.0.0.1:8082...")
    uvicorn.run(app, host="127.0.0.1", port=8082, log_level="info")
