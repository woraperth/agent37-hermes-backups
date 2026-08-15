---
name: comparing-llms
description: "Use when user asks which of two LLMs is better."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [model-comparison, benchmarks, artificial-analysis, open-weights, llm, frontier-models]

---

# Comparing LLMs via published data

## When to Use

Trigger on "which of these LLMs is better?" — "Is GPT-OSS 120B or DeepSeek V4 better?", "Which is stronger, X or Claude?", "Should I use model A or B for coding?". This answers from **published benchmarks and comparison sites** rather than running benchmarks yourself (for that, see the separate `evaluating-llms-harness` skill).

## The "better" question is almost never binary

Ask/assume what the user prioritizes, then frame the answer across these four axes. A direct "X is better" is usually wrong — open-weight/local models trade capability for cost and control:

1. **Raw capability / intelligence** — the only axis where a clear ranking usually exists.
2. **Speed / latency** — output tokens/sec, especially in high-effort reasoning modes.
3. **Cost & self-hostability** — API $/1M tokens AND whether weights are open (can you run it locally, for free, privately?).
4. **Context window & features** — context length, tool use, structured output, reasoning modes.

Open-weights models (e.g. GPT-OSS-120B, Llama, Qwen) win on axes 2–4; hosted frontier models (DeepSeek, GPT-5-class, Claude) typically win axis 1. Name both sides honestly, then recommend by the user's priority.

## Workflow

1. **Check the Artificial Analysis Intelligence Index** as the primary cross-model capability metric. It normalizes aptitude to a single number; numbers differ by mode (e.g. "Reasoning, High Effort" vs "Max Effort"), so quote the mode. This is the most consistent single source for "which is smarter".
2. **Pull direct head-to-head comparisons** from `artificialanalysis.ai/models/comparisons/<model-a>-vs-<model-b>` — they compare intelligence index, price, speed, and context window in one page.
3. **Corroborate** with vendor/blog side-by-sides (Spheron, Magica `magica.com/blog/compare/...`, SiliconFlow `siliconflow.com/models/compare/...`, BenchLM `benchlm.ai/compare/...`) and r/LocalLLaMA aggregated-benchmark threads (often the most detailed per-benchmark tables: MMLU-Pro, GPQA Diamond, AIME, SWE-bench).
4. **Keep research bounded.** Two to four searches is enough; this is a Q&A, not a research report. When you have the capability gap + a corroborating source + price/speed/weights, you're done. If the user interjects "stop" or equivalent, drop tool calls immediately and answer with what you have.
5. **Answer with a short verdict + the deciding axes + a "depends on your priority" recommendation.** Careful not to confuse a newer model name with an older one (e.g. DeepSeek V4 vs V3/R1 — confirm which generation is being asked about).

## Pitfalls

- Don't mislabel model generations: DeepSeek V4 (2026, 1M ctx, trillion-scale/32B active) is a different tier from V3/R1 (2025). GPT-OSS-120B beats DeepSeek-R1 on several benchmarks but loses decisively to V4 — the quoted opponent changes the answer.
- Intelligence Index and other aggregated numbers are effort/mode-sensitive — always state the mode you're quoting, and compare like-for-like.
- Free/open-weights does not mean weak — an open model can beat an older hosted model while losing to the current frontier generation. Call out which specific model the user actually wanted to compare against.
- Speed figures (tok/s) depend heavily on the inference engine (vLLM vs TensorRT-LLM vs SGLang) and hardware — mention that variance rather than treating a number as absolute.
