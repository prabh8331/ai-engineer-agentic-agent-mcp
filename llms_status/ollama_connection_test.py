#!/usr/bin/env python3
"""Ollama connection test — posts to the local Ollama HTTP API (default port 11434).

Usage:
  python ollama_connection_test.py
Environment:
  OLLAMA_URL default: http://127.0.0.1:11434/api/generate
  OLLAMA_MODEL default: llama
"""
import os
import sys

try:
    import requests
except Exception:
    print("Missing dependency: requests. Install with: pip install requests")
    sys.exit(2)


def main():
    url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
    model = os.getenv("OLLAMA_MODEL", "llama")
    payload = {"model": model, "prompt": "Hello from Ollama connection test"}
    headers = {"Content-Type": "application/json"}

    print(f"Attempting Ollama endpoint: {url}")
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        print("HTTP status:", resp.status_code)
        print("Response (trimmed):")
        print(resp.text[:2000])
        if resp.ok:
            print("Ollama connection looks healthy.")
            return 0
        else:
            print("Ollama returned non-OK status.")
            return 3
    except Exception as e:
        print("Connection failed:", repr(e))
        return 2


if __name__ == '__main__':
    sys.exit(main())
