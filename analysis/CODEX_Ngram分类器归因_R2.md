---
author: GPT-5 Codex
date: 2026-02-26
status: completed
---

# N-gram TF-IDF Classifier Attribution

- Vectorizer: `char_wb`, ngram `(2,5)`, max_features `10000`
- Classifier: `LogisticRegression(max_iter=1000)`
- 5-fold CV accuracy on generated set: **0.5970**

| model | avg canon probability | canon top-1 count |
|---|---:|---:|
| minimax_m2_5 | 0.1289 | 206 |
| claude_sonnet_4_5 | 0.1218 | 135 |
| minimax_m2_1 | 0.0989 | 3 |
| kimi_k2 | 0.0979 | 23 |
| glm_5 | 0.0972 | 12 |
| gpt_5_2 | 0.0875 | 15 |
| qwen3_235b_a22b | 0.0862 | 14 |
| kimi_k2_5 | 0.0834 | 0 |
| glm_4_7 | 0.0787 | 12 |
| deepseek_v3_2 | 0.0685 | 0 |
| qwen3_5 | 0.0509 | 12 |
