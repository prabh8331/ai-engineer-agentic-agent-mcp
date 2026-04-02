"""
Async LangGraph Agent with Groq + Tavily + Phoenix OpenTelemetry Tracing
==========================================================================

This lab demonstrates:
1. LangGraph ReAct agent (modern replacement for deprecated LangChain agents)
2. Groq LLM (fast inference via OpenAI-compatible endpoint)
3. Tavily Search via langchain-tavily (modern package)
4. OpenTelemetry tracing with Phoenix visualization
5. Async concurrent execution

Migration from deprecated APIs:
- LangChain agents → LangGraph ReAct agent
- TavilySearchResults → langchain_tavily.TavilySearchResults
- Chain.arun() → ainvoke()

Reference: See 1_lab1test.ipynb for Phoenix/tracing patterns
"""

import os
import asyncio
from typing import Any
from dotenv import load_dotenv

# ============================================================================
# 1. DEPENDENCIES
# ============================================================================
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch  # Modern package (correct import)
from langgraph.prebuilt import create_react_agent  # Modern agent
from langchain_core.tools import tool

# OpenTelemetry + Phoenix tracing (matching lab1test.ipynb pattern)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace as otel_trace

# ============================================================================
# 2. ENVIRONMENT SETUP
# ============================================================================

load_dotenv(override=True)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

# Phoenix configuration (same as lab1test.ipynb)
PHOENIX_OTLP_GRPC = os.environ.get("PHOENIX_OTLP_GRPC", "192.168.0.111:30317")
PHOENIX_UI = os.environ.get("PHOENIX_UI", "http://192.168.0.111:30606")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not set in .env")
if not TAVILY_API_KEY:
    raise ValueError("❌ TAVILY_API_KEY not set in .env")

print(f"✓ GROQ_API_KEY loaded")
print(f"✓ TAVILY_API_KEY loaded")

# ============================================================================
# 3. OPENTELEMETRY TRACING SETUP (Phoenix pattern from lab1test.ipynb)
# ============================================================================


def setup_tracing():
    """
    Configure OpenTelemetry -> Phoenix over gRPC (insecure, no TLS).
    
    This follows the exact pattern from 1_lab1test.ipynb:
    - OTLPSpanExporter sends to Phoenix gRPC endpoint
    - BatchSpanProcessor batches spans before sending
    - Global tracer provider for instrumentation
    """
    provider = TracerProvider()
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=PHOENIX_OTLP_GRPC, insecure=True)
        )
    )
    otel_trace.set_tracer_provider(provider)
    print(f"✓ OpenTelemetry configured")
    print(f"  → gRPC: {PHOENIX_OTLP_GRPC}")
    print(f"  → UI: {PHOENIX_UI}")
    return otel_trace.get_tracer(__name__)


# ============================================================================
# 4. TOOLS SETUP
# ============================================================================


def create_tools():
    """
    Create tools for the agent.
    Using langchain_tavily (modern) instead of deprecated TavilySearchResults.
    """
    
    # Tavily search tool from langchain_tavily
    tavily_search = TavilySearch(
        max_results=5
    )
    print("✓ Tavily search tool initialized (langchain_tavily - modern package)")
    
    tools = [tavily_search]
    return tools


# ============================================================================
# 5. AGENT SETUP (LangGraph - modern replacement)
# ============================================================================


def create_agent(tools: list):
    """
    Create LangGraph ReAct agent (modern replacement for deprecated LangChain agents).
    
    This uses:
    - Groq LLM (llama-3.3-70b-versatile)
    - LangGraph's pre-built ReAct agent (handles tool calling automatically)
    - Tavily search tool from langchain_tavily
    """
    
    # LLM: Groq with OpenAI-compatible client
    llm = ChatOpenAI(
        model="llama-3.3-70b-versatile",
        openai_api_key=GROQ_API_KEY,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0.7,
    )
    print("✓ Groq LLM initialized")
    
    # Create LangGraph ReAct agent (modern approach)
    agent = create_react_agent(
        llm,
        tools,
        debug=False
    )
    print("✓ LangGraph ReAct agent initialized (modern, no deprecation)")
    
    return agent


# ============================================================================
# 6. ASYNC AGENT RUNNER
# ============================================================================


async def run_single_query(agent, query: str, tracer) -> str:
    """
    Run agent on a single query with OpenTelemetry tracing.
    Uses ainvoke() (modern) instead of deprecated arun().
    """
    span_name = f"query: {query[:50]}"
    with tracer.start_as_current_span(span_name):
        print(f"\n🔍 Query: {query}")
        try:
            # Use ainvoke (modern) instead of deprecated arun
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]},
                config={"recursion_limit": 10}
            )
            
            # Extract the final output from LangGraph result
            final_message = result["messages"][-1]
            output = final_message.content
            
            print(f"✓ Got result ({len(str(output))} chars)")
            return output
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"✗ {error_msg}")
            return error_msg


async def run_multiple_queries(agent, queries: list[str], tracer) -> list[str]:
    """
    Run multiple queries concurrently with parent trace span.
    All child spans report to the parent in Phoenix.
    """
    with tracer.start_as_current_span("multi_query_search"):
        print(f"\n📦 Running {len(queries)} queries concurrently...")
        tasks = [run_single_query(agent, q, tracer) for q in queries]
        results = await asyncio.gather(*tasks)
        return results


# ============================================================================
# 7. MAIN ENTRY POINT
# ============================================================================


async def main():
    """Main async runner"""
    
    print("=" * 80)
    print("🚀 LangGraph ReAct Agent: Groq + Tavily + Phoenix OpenTelemetry Tracing")
    print("=" * 80)
    print()
    
    # Setup tracing (connects to Phoenix)
    print("📡 Setting up tracing...")
    tracer = setup_tracing()
    print()
    
    # Create tools
    print("🔧 Creating tools...")
    tools = create_tools()
    print()
    
    # Create agent
    print("📦 Initializing agent...")
    agent = create_agent(tools)
    print()
    
    # Example queries to demonstrate concurrent execution
    queries = [
        "What are the latest developments in AI agents in 2026?",
        "Compare CrewAI vs LangGraph vs AutoGen frameworks",
        "What open-source frameworks are popular for multi-agent systems?",
    ]
    
    # Run queries concurrently (all traced to Phoenix)
    print("🎯 Running queries...\n")
    results = await run_multiple_queries(agent, queries, tracer)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 RESULTS SUMMARY")
    print("=" * 80)
    for i, (query, result) in enumerate(zip(queries, results), 1):
        print(f"\n[Query {i}] {query}")
        # Show first 300 chars for better visibility
        result_preview = result[:300] + "..." if len(result) > 300 else result
        print(f"[Result] {result_preview}")
    
    print("\n" + "=" * 80)
    print(f"✅ All queries completed!")
    print(f"📈 View traces in Phoenix: {PHOENIX_UI}")
    print("=" * 80)


# ============================================================================
# 8. QUICK TEST MODE (uncomment to use)
# ============================================================================


async def quick_test():
    """Quick single-query test for debugging"""
    print("🧪 Quick test mode (single query)\n")
    
    tracer = setup_tracing()
    tools = create_tools()
    agent = create_agent(tools)
    
    query = "Explain LangGraph agent patterns in one paragraph"
    result = await run_single_query(agent, query, tracer)
    
    print(f"\n✅ Test complete")
    print(f"Check Phoenix: {PHOENIX_UI}")


# ============================================================================

if __name__ == "__main__":
    # Choose one:
    asyncio.run(main())              # Full multi-query demo with tracing
    # asyncio.run(quick_test())       # Single quick query test
