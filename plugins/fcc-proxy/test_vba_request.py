"""Test VBA code generation with qwen3-coder via free-claude-code proxy."""
import httpx
import json
import os

os.environ["ANTHROPIC_AUTH_TOKEN"] = "freecc"

client = httpx.Client(base_url="http://127.0.0.1:8082", timeout=60.0)

# Test VBA code generation
payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 500,
    "messages": [
        {
            "role": "user",
            "content": "Write a VBA UserForm code for a stock entry form in Excel. Include fields for Item Name, Quantity, Date, and a Submit button that adds data to a sheet named 'StockLedger'. Use proper error handling with On Error statements."
        }
    ]
}

try:
    print("Sending request to qwen3-coder via proxy...")
    response = client.post(
        "/v1/messages",
        headers={
            "x-api-key": "freecc",
            "anthropic-version": "2023-06-01"
        },
        json=payload
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response:")
        print(data.get("content", [{}])[0].get("text", "No text"))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
