#!/usr/bin/env python3
"""vLLM connection test — attempts an HTTP POST to a typical vLLM/OpenAI-compatible endpoint.

Usage:
  python vllm_connection_test.py
Environment:
  VLLM_URL   default: http://192.168.0.80:31080/v1/completions
  VLLM_MODEL default: llama
"""
import os
import sys
import json

try:
    import requests
except Exception as e:
    print("Missing dependency: requests. Install with: pip install requests")
    sys.exit(2)


def main():
    url = os.getenv("VLLM_URL", "http://192.168.0.80:31080/v1/completions")
    model = os.getenv("VLLM_MODEL", "tinyllama-chat")
    # Include both `prompt` and `input` for broader endpoint compatibility
    payload = {
        "model": model,
        "prompt": "Hello from vLLM connection test",
        "input": "Hello from vLLM connection test",
    }
    headers = {"Content-Type": "application/json"}

    print(f"Attempting vLLM endpoint: {url}")
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        print("HTTP status:", resp.status_code)
        print("Response body (trimmed):")
        print(resp.text[:2000])
        if resp.ok:
            print("vLLM connection looks healthy.")
            return 0
        else:
            print("vLLM returned non-OK status.")
            return 3
    except Exception as e:
        print("Connection failed:", repr(e))
        return 2


if __name__ == '__main__':
    sys.exit(main())
