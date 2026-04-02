# 4_lab4.py - Async LangGraph Agent with Groq + Tavily + Phoenix Tracing

## ✅ Completed Setup

### What's Been Done
1. **Migrated from deprecated APIs**:
   - ✅ LangChain agents → LangGraph ReAct agent  
   - ✅ TavilySearchResults (deprecated) → langchain_tavily.TavilySearch
   - ✅ deprecated Chain.arun() → modern ainvoke()

2. **Installed New Dependency**:
   - ✅ Added `langchain-tavily>=0.1.0` to pyproject.toml
   - ✅ Installed via UV sync

3. **Phoenix Tracing Configuration**:
   - ✅ OpenTelemetry → Phoenix gRPC: `192.168.0.111:30317`
   - ✅ BatchSpanProcessor for efficient tracing
   - ✅ Pattern matches 1_lab1test.ipynb exactly

4. **Multiple Query Concurrency**:
   - ✅ Uses `asyncio.gather()` for concurrent execution
   - ✅ Each query creates a separate traced span in Phoenix
   - ✅ Parent span tracks all queries

## 🚀 How to Run

### Direct Python
```bash
cd /mnt/synserver/workspaces/Learning/AI/ai-engineer-agentic-agent-mcp/2_openai
/home/archworker1/Project_venvs_py/ai-agent-mcp/bin/python 4_lab4.py
```

### With Virtual Environment Activated
```bash
source /home/archworker1/Project_venvs_py/ai-agent-mcp/bin/activate
cd 2_openai
python 4_lab4.py
```

## 📊 Example Output

```
✓ GROQ_API_KEY loaded
✓ TAVILY_API_KEY loaded
================================================================================
🚀 LangGraph ReAct Agent: Groq + Tavily + Phoenix OpenTelemetry Tracing
================================================================================

📡 Setting up tracing...
✓ OpenTelemetry configured
  → gRPC: 192.168.0.111:30317
  → UI: http://192.168.0.111:30606

🔧 Creating tools...
✓ Tavily search tool initialized (langchain_tavily - modern package)

📦 Initializing agent...
✓ Groq LLM initialized
✓ LangGraph ReAct agent initialized (modern, no deprecation)

🎯 Running queries...

[Query results with proper content displayed]

✅ All queries completed!
📈 View traces in Phoenix: http://192.168.0.111:30606
```

## 🔍 View Traces in Phoenix

After running the script, open your browser to:

```
http://192.168.0.111:30606
```

You'll see a trace hierarchy like:
- **multi_query_search** (parent span)
  - query: What are the latest developments in AI agents in 2026?
  - query: Compare CrewAI vs LangGraph vs AutoGen frameworks
  - query: What open-source frameworks are popular for multi-agent systems?

Each span shows:
- LLM call details
- Tool invocations (Tavily search)
- Latency metrics
- Full execution trace

## 🛠️ Technical Details

### Agent Architecture
- **LLM**: Groq (llama-3.3-70b-versatile) via OpenAI-compatible endpoint
- **Agent Type**: LangGraph ReAct (reasoning + acting loop)
- **Tools**: TavilySearch from langchain_tavily
- **Execution**: Async with concurrent queries

### Phoenix Integration (Same as lab1test.ipynb)
```python
provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint=PHOENIX_OTLP_GRPC, insecure=True)
    )
)
otel_trace.set_tracer_provider(provider)
```

### Environment Configuration
Uses `.env` file with:
- `GROQ_API_KEY`: Your Groq API key
- `TAVILY_API_KEY`: Your Tavily API key
- `PHOENIX_OTLP_GRPC`: Phoenix gRPC endpoint (default: `192.168.0.111:30317`)
- `PHOENIX_UI`: Phoenix dashboard URL (default: `http://192.168.0.111:30606`)

## ✨ Key Features

1. **No Deprecation Warnings**: Uses all modern APIs
2. **Real Results**: Queries return actual content from searches
3. **Concurrent Execution**: Multiple queries run in parallel
4. **Full Tracing**: All execution traced to Phoenix dashboard
5. **Error Handling**: Graceful error capture and reporting
6. **Clean Output**: Formatted logging with progress indicators

## 📝 Notes

- The script uses LangGraph's pre-built ReAct agent for simplicity
- TavilySearch automatically handles tool calling via LLM
- All spans are sent to Phoenix with proper hierarchy
- Async execution allows true parallelism for multiple queries
