#!/bin/bash
# Quick Start Guide for 4_lab4.py
# ===============================

# Make sure you're in the right directory
cd /mnt/synserver/workspaces/Learning/AI/ai-engineer-agentic-agent-mcp/2_openai

# Run the agent with your virtual environment:
/home/archworker1/Project_venvs_py/ai-agent-mcp/bin/python 4_lab4.py

# Or activate the venv and run directly:
# source /home/archworker1/Project_venvs_py/ai-agent-mcp/bin/activate
# python 4_lab4.py

# ===============================
# IMPORTANT SETUP NOTES:
# ===============================

# 1. Python Interpreter already configured via .vscode/settings.json
#    Default: /home/archworker1/Project_venvs_py/ai-agent-mcp/bin/python

# 2. Jupyter Kernel already installed:
#    Name: ai-agent-mcp
#    Use this when running notebooks

# 3. Dependencies installed with UV:
#    UV_PROJECT_ENVIRONMENT=/home/archworker1/Project_venvs_py/ai-agent-mcp uv sync

# 4. Phoenix Tracing Configuration:
#    - gRPC Endpoint: 192.168.0.111:30317 (from .env)
#    - Phoenix UI: http://192.168.0.111:30606
#    - View traces there after running the agent

# ===============================
# WHAT THE SCRIPT DOES:
# ===============================

# 1. Loads GROQ_API_KEY and TAVILY_API_KEY from .env
# 2. Sets up OpenTelemetry tracing to Phoenix (matching lab1test.ipynb pattern)
# 3. Creates a LangChain agent with:
#    - Groq LLM (llama-3.3-70b-versatile)
#    - Tavily web search tool
# 4. Runs 3 example queries concurrently
# 5. All execution is traced and sent to Phoenix

# ===============================
# TRACE PATTERNS (from lab1test.ipynb):
# ===============================

# The tracing setup matches 1_lab1test.ipynb exactly:
#
#   provider = TracerProvider()
#   provider.add_span_processor(
#       BatchSpanProcessor(
#           OTLPSpanExporter(endpoint=PHOENIX_OTLP_GRPC, insecure=True)
#       )
#   )
#   otel_trace.set_tracer_provider(provider)
#
# Each async call creates a span that appears in Phoenix dashboard
