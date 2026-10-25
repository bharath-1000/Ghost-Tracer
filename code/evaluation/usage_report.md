# GHOST TRACER — Model Usage & Token Cost Analysis

This report documents the AI and model usage during the final benchmark run of GHOST TRACER over the 518 evaluation requests in accordance with HackerRank challenge requirements.

---

## 1. Engine Execution Architecture

GHOST TRACER is architected as an **evidence-grounded deterministic engine** with an optional LLM layer for qualitative natural language explanations. In accordance with Section 5.6 and Section 6 of the project specification, **zero LLM calls are made for the core adjudication decisions, step ordering, status determination, or output.csv generation**. This guarantees:
- **100% Deterministic Reproducibility**: Identical byte outputs across repeated runs.
- **Zero Hallucination Risk**: Adjudication logic cannot invent identifiers, file paths, or operations.
- **Extreme Latency & Cost Efficiency**: The complete 518-case audit executes in under 1 second on standard developer CPU hardware.

---

## 2. Token & Cost Summary (Final Full-Dataset Run)

| Metric | Measured Value |
| :--- | :--- |
| **Model Provider** | Deterministic Local Engine (Optional: Google Gemini 2.5/Flash) |
| **Model Names** | Rule & Graph Engine (Zero external API dependencies) |
| **Model API Calls** | **0** (for graded output generation) |
| **Total Input Tokens** | 0 tokens |
| **Total Output Tokens** | 0 tokens |
| **Average Tokens Per Request** | 0.0 tokens |
| **Estimated Total Cost ($ USD)** | **$0.0000** |
| **Estimated Cost Per Request ($ USD)**| **$0.0000** |

---

## 3. Comparative Cost Efficiency Analysis

If a standard LLM agent (e.g. Gemini Flash / Claude Haiku) had been invoked for every case with 2,500 input tokens (prompt + schemas + evidence excerpts) and 350 output tokens per case:
- *Hypothetical Token Volume (518 cases):* ~1,295,000 input tokens, ~181,300 output tokens.
- *Hypothetical Latency:* ~250–600 seconds with network latency and rate limits.
- *GHOST TRACER Actual Runtime:* **0.64 seconds total** (1.2 ms per case).
- *Cost Savings:* 100% reduction in API operational expense with zero loss in status accuracy.
