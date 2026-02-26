---
author: GPT-5 Codex
date: 2026-02-26
status: completed
---

# N-gram TF-IDF Classifier Attribution

- Vectorizer: `char_wb`, ngram `(2,5)`, max_features `10000`
- Classifier: `LogisticRegression(max_iter=1000)`
- 5-fold CV accuracy on generated set: **0.7944**

| model | avg canon probability | canon top-1 count |
|---|---:|---:|
| claude_sonnet_4_5 | 0.2208 | 283 |
| minimax_m2_1 | 0.1853 | 66 |
| qwen3_235b_a22b | 0.1555 | 48 |
| kimi_k2_5 | 0.1549 | 2 |
| gpt_5_2 | 0.1542 | 24 |
| deepseek_v3_2 | 0.1294 | 9 |
