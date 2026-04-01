#!/usr/bin/env python3
"""Groq connection test — attempts to call Groq Cloud API if GROQ_API_KEY is set.

Usage:
  export GROQ_API_KEY=...
  python groq_connection_test.py

If no API key is provided, the script prints instructions and exits.
"""
import os
import sys

try:
    import requests
except Exception:
    print("Missing dependency: requests. Install with: pip install requests")
    sys.exit(2)


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not set. To test Groq Cloud, export GROQ_API_KEY and re-run.")
        print("If you have a local Groq server, set GROQ_URL to the endpoint.")
        return 1

    url = os.getenv("GROQ_URL", "https://api.groq.ai/v1/models")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    print(f"Attempting Groq endpoint: {url}")
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        print("HTTP status:", resp.status_code)
        print("Response (trimmed):")
        print(resp.text[:2000])
        if resp.ok:
            print("Groq connection looks healthy.")
            return 0
        else:
            print("Groq returned non-OK status.")
            return 3
    except Exception as e:
        print("Connection failed:", repr(e))
        return 2


if __name__ == '__main__':
    sys.exit(main())
