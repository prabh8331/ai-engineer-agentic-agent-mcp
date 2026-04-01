#!/usr/bin/env python3
"""
Standalone debug script: Groq + OpenAI Agents SDK → Phoenix traces over OTLP/HTTP.

Usage:
    export GROQ_API_KEY=gsk_...
    python 2_openai/debug_phoenix_trace.py

Or with a .env file in the project root (python-dotenv is loaded automatically).
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv(override=True)

# ── 1. Check prerequisites ──────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not set. Add it to .env or export it.", file=sys.stderr)
    sys.exit(1)

PHOENIX_OTLP_GRPC = os.environ.get("PHOENIX_OTLP_GRPC", "192.168.0.111:30317")   # NO http:// for gRPC
PHOENIX_UI        = os.environ.get("PHOENIX_UI",        "http://192.168.0.111:30606")
ENDPOINT          = PHOENIX_OTLP_GRPC

print(f"Phoenix UI         : {PHOENIX_UI}")
print(f"OTLP gRPC endpoint : {ENDPOINT}")
print()

# ── 2. Quick reachability check ─────────────────────────────────────────────
import urllib.request, urllib.error
def check(url: str, label: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=4) as r:
            print(f"[OK ] {label} → HTTP {r.status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[OK ] {label} → HTTP {e.code} (endpoint reachable)")
        return True
    except Exception as e:
        print(f"[ERR] {label} → {e}")
        return False

health_ok = check(f"{PHOENIX_UI}/healthz", "Phoenix health")
# gRPC port check — HTTP GET will get a gRPC/HTTP2 response (non-200 is fine, refused is bad)
otlp_ok   = check(f"http://{ENDPOINT}", "OTLP gRPC port")

if not health_ok:
    print("\nPhoenix pod is not reachable. Check: kubectl get pods -n phoenix")
    sys.exit(1)
if not otlp_ok:
    print("\nOTLP gRPC port not reachable; traces will fail. Check NodePort 30317 is open.")
    # continue anyway — let the SDK retry and show the real error

print()

# ── 3. Configure OTLP/HTTP tracing ──────────────────────────────────────────
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry import trace as otel_trace
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor

provider = TracerProvider()

# Primary: Phoenix over OTLP/gRPC — endpoint is host:port, insecure=True for plain gRPC
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=ENDPOINT, insecure=True))
)

# Secondary: print spans to stdout so you can verify instrumentation locally
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

otel_trace.set_tracer_provider(provider)
OpenAIAgentsInstrumentor().instrument(tracer_provider=provider)

print(f"Tracing configured → gRPC {ENDPOINT} + stdout.\n")

# ── 4. Build Groq-backed agent ───────────────────────────────────────────────
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, trace

groq_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

model = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=groq_client,
)

agent = Agent(
    name="groq-debug-agent",
    instructions="You are a helpful assistant.",
    model=model,
)

# ── 5. Run one traced call ───────────────────────────────────────────────────
async def main():
    prompt = "Tell a one-liner joke about distributed tracing."
    print(f"Prompt: {prompt}\n")

    with trace("debug-groq-joke"):
        result = await Runner.run(agent, prompt)

    print("Response:")
    print(result.final_output)

    # Flush spans before exit
    provider.force_flush(timeout_millis=10_000)
    print(f"\nDone. Check traces at: {PHOENIX_UI}")

asyncio.run(main())
