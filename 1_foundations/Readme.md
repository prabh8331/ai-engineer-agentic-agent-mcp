# AI Agents

## Ambiguity on what Agents acutlly are

`AI Agents are programs where LLM outputs control the workflow`

In prectice, describes an AI solution that involes any or all of these:

1. Multiple LLM calls
2. LLMs with ability to use Tools
3. An environment where LLMs intract
4. A Planner to coordinte activities
5. Autonomy



## Agentic Systems

Anthroic distinguishes two types:

- Workflows: are systems where LLMs and tools are orchestrated through predefined code paths 
- Agents: are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks

### 5 workflow design patterns


1. Prompt Chaining (Sequential Pipeline)

```mermaid
flowchart LR

classDef agent    fill:#6C63FF,color:#fff,stroke:#4B44CC,rx:8
classDef io       fill:#3B82F6,color:#fff,stroke:#2563EB,rx:8

A1(["📥 Input"]):::io --> A2["Agent A<br>Extract"]:::agent
A2 --> A3["Agent B<br>Transform"]:::agent
A3 --> A4["Agent C<br>Summarise"]:::agent
A4 --> A5(["📤 Output"]):::io
```



2. Parallelization (Fan-Out / Fan-In)

```mermaid
flowchart TB

classDef agent    fill:#6C63FF,color:#fff,stroke:#4B44CC,rx:8
classDef io       fill:#3B82F6,color:#fff,stroke:#2563EB,rx:8

B1(["📥 Task"]):::io --> B2["Orchestrator"]:::agent
B2 --> B3["Worker A"]:::agent
B2 --> B4["Worker B"]:::agent
B2 --> B5["Worker C"]:::agent

B3 --> B6["Aggregator"]:::agent
B4 --> B6
B5 --> B6

B6 --> B7(["📤 Result"]):::io
```



3. Routing (Conditional Dispatch)

```mermaid
flowchart TB

classDef agent    fill:#6C63FF,color:#fff,stroke:#4B44CC,rx:8
classDef decision fill:#F59E0B,color:#fff,stroke:#D97706
classDef io       fill:#3B82F6,color:#fff,stroke:#2563EB,rx:8

C1(["📥 Request"]):::io --> C2{{"🔀 Router<br>Classify intent"}}:::decision

C2 -- "Code task" --> C3["Code Agent"]:::agent
C2 -- "Data task" --> C4["Data Agent"]:::agent
C2 -- "Research" --> C5["Search Agent"]:::agent

C3 --> C6(["📤 Response"]):::io
C4 --> C6
C5 --> C6
```



4. Orchestrator–Worker (Subagents / Tool Use)

```mermaid
flowchart TB

classDef agent    fill:#6C63FF,color:#fff,stroke:#4B44CC,rx:8
classDef io       fill:#3B82F6,color:#fff,stroke:#2563EB,rx:8

D1(["📥 Goal"]):::io --> D2["Orchestrator<br>Planner"]:::agent

D2 -- "delegate" --> D3["Subagent 1<br>Web Search"]:::agent
D2 -- "delegate" --> D4["Subagent 2<br>Code Exec"]:::agent
D2 -- "delegate" --> D5["Subagent 3<br>File I/O"]:::agent

D3 -. "result" .-> D2
D4 -. "result" .-> D2
D5 -. "result" .-> D2

D2 --> D6(["📤 Final Answer"]):::io
```



5. Evaluator–Optimizer (Reflection Loop)

```mermaid
flowchart TB

classDef agent    fill:#6C63FF,color:#fff,stroke:#4B44CC,rx:8
classDef decision fill:#F59E0B,color:#fff,stroke:#D97706
classDef io       fill:#3B82F6,color:#fff,stroke:#2563EB,rx:8

E1(["📥 Prompt"]):::io --> E2["Generator<br>Agent"]:::agent
E2 --> E3["Evaluator<br>Agent"]:::agent

E3 --> E4{{"Pass<br>threshold?"}}:::decision

E4 -- "❌ No → refine" --> E2
E4 -- "✅ Yes" --> E5(["📤 Final Output"]):::io
```


### Agents:

Open-ended, Feedback loops, No Fixed path

Risks of Agents Frameworks: Unpredicatable path, Unpredicatable output, Unpredictable costs, Monitor

`Guardrails ensure your agents behave safely, consistently, and within your intended boundaries`

```mermaid
flowchart TB

%% ── STYLES ──────────────────────────────────────────────────
classDef core     fill:#6C63FF,color:#fff,stroke:#4B44CC,rx:10
classDef memory   fill:#8B5CF6,color:#fff,stroke:#6D28D9,rx:10
classDef tool     fill:#10B981,color:#fff,stroke:#059669,rx:10
classDef io       fill:#3B82F6,color:#fff,stroke:#2563EB,rx:10
classDef env      fill:#F59E0B,color:#fff,stroke:#D97706,rx:10
classDef guard    fill:#EF4444,color:#fff,stroke:#DC2626,rx:10
classDef decision fill:#64748B,color:#fff,stroke:#475569,rx:10

%% ═════════ INPUT ═════════
IN(["👤 Input"]):::io

%% ═════════ GUARDRAILS ═════════
G1["🛡️ Input Check"]:::guard
G2["🛡️ Output Check"]:::guard

%% ═════════ CORE LOOP ═════════
LLM["🧠 LLM"]:::core
PLAN["🧩 Plan"]:::core
ACT["⚡ Act"]:::core

%% ═════════ MEMORY ═════════
MEM["🗂️ Memory"]:::memory

%% ═════════ TOOLS ═════════
TOOLS["⚙️ Tools"]:::tool

%% ═════════ ENVIRONMENT ═════════
ENV["🌍 Environment"]:::env
OBS["📩 Feedback"]:::env

%% ═════════ CONTROL ═════════
STOP{{"Done?"}}:::decision
OUT(["📤 Output"]):::io

%% ═════════ FLOW ═════════

IN --> G1 --> LLM

LLM --> PLAN --> ACT
ACT --> TOOLS --> ENV --> OBS --> LLM

LLM <-->|context| MEM

LLM --> STOP
STOP -- No --> PLAN
STOP -- Yes --> G2 --> OUT
```



```mermaid

flowchart TB

%% ── STYLES ──────────────────────────────────────────────────────────────────
classDef core     fill:#6C63FF,color:#fff,stroke:#4B44CC,stroke-width:2px
classDef memory   fill:#8B5CF6,color:#fff,stroke:#6D28D9,stroke-width:2px
classDef tool     fill:#10B981,color:#fff,stroke:#059669,stroke-width:2px
classDef io       fill:#3B82F6,color:#fff,stroke:#2563EB,stroke-width:2px
classDef env      fill:#F59E0B,color:#fff,stroke:#D97706,stroke-width:2px
classDef guard    fill:#EF4444,color:#fff,stroke:#DC2626,stroke-width:2px
classDef decision fill:#64748B,color:#fff,stroke:#475569,stroke-width:2px

%% ════════════════════════════════════════════════════════════════════════════
%%  LAYER 0 — INPUT
%% ════════════════════════════════════════════════════════════════════════════

IN1[/"👤 Human / System<br/>Goal + Context"/]:::io

%% ════════════════════════════════════════════════════════════════════════════
%%  LAYER 1 — SAFETY & GUARDRAILS
%% ════════════════════════════════════════════════════════════════════════════

subgraph GUARD["🛡️ Guardrails"]
    direction LR
    G1["Input<br/>Validator"]:::guard
    G2["Output<br/>Validator"]:::guard
end

%% ════════════════════════════════════════════════════════════════════════════
%%  LAYER 2 — AGENT CORE
%% ════════════════════════════════════════════════════════════════════════════

subgraph CORE["🧠 Agent Core"]
    direction TB
    
    LLM["<b>LLM</b><br/>Reasoning Engine"]:::core
    
    subgraph PLAN["Planning"]
        direction LR
        P1["Decompose"]:::core
        P2["Reason"]:::core
        P3["Reflect"]:::core
        P1 --> P2 --> P3
    end
    
    LLM <--> PLAN
end

%% ════════════════════════════════════════════════════════════════════════════
%%  LAYER 3 — MEMORY
%% ════════════════════════════════════════════════════════════════════════════

subgraph MEM["🗂️ Memory Systems"]
    direction LR
    M1["Working"]:::memory
    M2["Episodic"]:::memory
    M3["Semantic<br/>(RAG)"]:::memory
    M4["Procedural"]:::memory
end

%% ════════════════════════════════════════════════════════════════════════════
%%  LAYER 4 — TOOL SPACE
%% ════════════════════════════════════════════════════════════════════════════

subgraph TOOLS["⚙️ Tools"]
    direction LR
    T1["Search"]:::tool
    T2["Code"]:::tool
    T3["Database"]:::tool
    T4["APIs"]:::tool
    T5["Sub‑Agent"]:::tool
end

%% ════════════════════════════════════════════════════════════════════════════
%%  LAYER 5 — ENVIRONMENT
%% ════════════════════════════════════════════════════════════════════════════

subgraph ENV["🌍 Environment"]
    direction LR
    E1["Observe"]:::env
    E2["Update"]:::env
    E1 --> E2
end

%% ════════════════════════════════════════════════════════════════════════════
%%  DECISION
%% ════════════════════════════════════════════════════════════════════════════

STOP{{"Goal<br/>Achieved?"}}:::decision
OUT[/"Final<br/>Response"/]:::io

%% ════════════════════════════════════════════════════════════════════════════
%%  CONNECTIONS
%% ════════════════════════════════════════════════════════════════════════════

IN1 --> G1
G1  --> LLM

LLM  <-->|rw| MEM
PLAN -->|call| TOOLS
TOOLS--> ENV
ENV  -->|obs| LLM

LLM  --> STOP
STOP -->|❌ loop| PLAN
STOP -->|✅ done| G2
G2   --> OUT

```

## The cast of characters

- OpenAI: gpt-4o-mini(also gpt-4o, o1, o3-mini)
- Anthropic: Claude-3-7-Sonnet
- Google: Gemini-2.0-flash
- DeepSeek AI: DeepSeek V3, DeepSeek R1
- Groq: open-source LLMs including Llama3.3
- Ollama: local open-source LLMs including LLama3.2

https://www.vellum.ai/llm-leaderboard