# Model Landscape — May 2026

> **Hardware baseline:** CPU-only, 8GB RAM (3.8GB free), Windows. No GPU.

---

## 1. Cloud Providers — Large Context / Coding Models

### Free Tier (Working Now)

| Provider | Model | Context | Speed | Notes |
|----------|-------|---------|-------|-------|
| **Groq** | Llama 3.3 70B | 32K | ~300 t/s | Primary driver, 6K tok/min limit |
| **Groq** | Qwen 3 32B | 32K | ~300 t/s | Fast debug/explore |
| **Google AI Studio** | Gemini 2.5 Flash | **1M** | ~2s | 1,500 req/day, free, no CC |
| **OpenRouter** | Nemotron 3 Super 120B | **1M** | moderate | Opus-tier quality, works reliably |
| **OpenRouter** | GPT-OSS 120B | ? | moderate | Sonnet-tier, works |
| **OpenRouter** | Ring 2.6 1T | ? | moderate | Massive model, works |
| **OpenRouter** | Quasar Alpha | **1M** | moderate | Stealth release, 55% Aider |
| **Cerebras** | Llama variants | — | very fast | 1M tokens/day free |
| **Mistral** | All Mistral models | 32K | moderate | 1B tok/month free, 2 RPM |

### Free Tier (Rate-Limited / Unstable)

| Provider | Model | Context | Status |
|----------|-------|---------|--------|
| OpenRouter | Llama 3.3 70B (free) | 32K | ⏳ 429 rate-limited |
| OpenRouter | Qwen3 Coder 480B (free) | ? | ⏳ 429 rate-limited |
| OpenRouter | Gemma 4 26B (free) | 262K | ⏳ 429 rate-limited |
| SambaNova | Llama/Qwen variants | varies | Requires email signup |

### Paid (Configured, Keys Set)

| Provider | Model | Context | Cost (per 1M in) | Best For |
|----------|-------|---------|-----------------|----------|
| **Anthropic** | Claude 4 Sonnet | 200K | $3.00 | Precision refactoring |
| **Anthropic** | Claude Opus 4.6 | **1M** | $5.00 | Complex architecture |
| **OpenAI** | GPT-4o / GPT-4.1 | 128K | $2.00 | General coding |
| **Google Vertex** | Gemini 2.5 Pro | **1M** | $1.25 | Long-context reasoning |

### Key Findings — Cloud
- **Best free large-context:** Gemini 2.5 Flash (1M ctx, 1,500 req/day free) — ideal for full-codebase analysis
- **Best free coding quality (free):** Groq Llama 3.3 70B — fastest inference, but 32K context only
- **Best free massive context:** Nemotron 3 Super 120B via OpenRouter (1M ctx, free)
- **Best paid value:** Gemini 2.5 Pro ($1.25/M in) for 1M context on a budget; Claude Opus 4.6 for top quality

---

## 2. Ollama Local Models — CPU-only, 8GB RAM

### Already Installed

| Model | Size | RAM Use | Speed | Verdict |
|-------|------|---------|-------|---------|
| **qwen2.5-coder:7b** | 4.7 GB | ~7 GB | ~5-8 t/s | Barely fits, usable for batch |
| **qwen2.5-coder:1.5b** | 986 MB | ~2 GB | ~10-15 t/s | Comfortable fit, decent quality |

### Recommended to Add

| Model | Pull Command | Size | RAM | Speed | Best For |
|-------|-------------|------|-----|-------|----------|
| **Qwen3 1.7B** (Q4) | `ollama pull qwen3:1.7b` | ~1.3 GB | ~3 GB | 10-15 t/s | Best quality-to-RAM ratio, reasoning + coding |
| **Phi-4-mini 3.8B** (Q4) | `ollama pull phi-4-mini:3.8b` | ~2.5 GB | ~5 GB | 6-10 t/s | Best coding on CPU, beats most 7Bs |
| **Llama 3.2 3B** (Q4) | `ollama pull llama3.2:3b` | ~2.2 GB | ~4 GB | 8-12 t/s | Solid general-purpose, strong community |
| **Qwen3-Coder-Next** | `ollama pull qwen3-coder-next` | ~2 GB | ~8 GB | varies | MoE: 80B total / 3B active, coding specialist |

### Not Recommended (on 8GB CPU-only)

| Model | Reason |
|-------|--------|
| Llama 3.1 8B | Needs 16GB RAM for comfortable use |
| DeepSeek R1 14B | Needs 16GB RAM minimum |
| Qwen2.5-Coder 14B/32B | Needs 16-32GB RAM |
| CodeGemma 7B | Redundant vs qwen2.5-coder:7b |
| StarCoder2 15B | Needs 16GB RAM |

### Optimization Tips for 8GB CPU-only

```
# Prevent OOM from parallel sessions
$env:OLLAMA_NUM_PARALLEL=1
# Quantize KV cache
$env:OLLAMA_KV_CACHE_TYPE="q8_0"
# Keep context ≤4K tokens
# Use Q4_K_M quantization (Ollama default)
```

---

## 3. Combined Recommendations

### Current Setup (Optimal for This Hardware)

| Tier | Model | Role | Status |
|------|-------|------|--------|
| **Cloud primary** | Groq Llama 3.3 70B | Daily VBA coding | ✅ Working |
| **Cloud long-context** | Gemini 2.5 Flash (1M) | Full-codebase analysis | ✅ Working |
| **Cloud free backup** | Nemotron 120B (OpenRouter) | Heavy reasoning | ✅ Working |
| **Local fast** | qwen2.5-coder:1.5b | Quick offline edits | ✅ Installed |
| **Local quality** | qwen2.5-coder:7b | Offline VBA work | ✅ Installed |
| **Local CPU reasoning** | qwen3:1.7b | Best CPU reasoning model, 1.4GB | ✅ Installed |
| **Local CPU coding** | phi4-mini:3.8b-q4_K_M | Best CPU coding, 2.5GB | ✅ Installed |

### Suggested Additions (none — all installed)

### If RAM Upgrade to 16GB (Future)

| Model | Why |
|-------|-----|
| DeepSeek R1 14B | Chain-of-thought debugging |
| Qwen2.5-Coder 14B | Stronger offline coding |
| GPT-OSS 20B | OpenAI open-source, all-around |

---

## 4. Landscape Summary

```
CLOUD (free, fast) ─── Groq Llama 3.3 70B ←─── Primary driver
                      Gemini 2.5 Flash       ←─── 1M ctx, full codebase
                      Nemotron 120B           ←─── Free Opus-tier backup

LOCAL (offline)  ──── qwen2.5-coder:7b       ←─── Quality offline
                      qwen2.5-coder:1.5b     ←─── Fast offline
                      [add] qwen3:1.7b        ←─── Best CPU reasoning
                      [add] phi-4-mini:3.8b   ←─── Best CPU coding

PAID (keys set)  ──── Claude 4 Sonnet        ←─── Precision work
                      GPT-4o                 ←─── General coding
```

**Bottom line:** Your current Groq + Gemini + Nemotron cloud stack covers 95% of needs. Locally, qwen2.5-coder:7b handles offline VBA work. Adding qwen3:1.7b (~986 MB) or phi-4-mini:3.8b (~2.5 GB) would give you better CPU-friendly options without exceeding 8GB RAM.
