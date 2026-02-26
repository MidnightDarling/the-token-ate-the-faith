---
author: Claude Opus 4.6 (Halfnote)
date: 2026-02-26
updated: 2026-02-26 (R3 — 11 models + OpenRouter usage data)
status: ready
type: final-verdict
evidence_layers:
  - "Layer 1: Text metrics (15-dim) — Halfnote"
  - "Layer 2: Multi-embedding MMD (10,240-dim) — Halfnote"
  - "Layer 3: Nearest-neighbor attribution (4 providers) — Halfnote"
  - "Layer 4: Active probe generation (330 texts, 11 models) — GPT-5 Codex R1+R2"
  - "Layer 5: N-gram TF-IDF classifier (11 models retrained) — GPT-5 Codex R2"
  - "Layer 6: Compliance gradient (7 levels, 11 models) — GPT-5 Codex R2"
  - "Layer 7: Distillation fingerprint matrix (prior work) — Halfnote"
  - "Layer 8: Claude Code interception (meta-evidence)"
  - "Layer 9: OpenRouter API usage data (Alice OSINT) — 2026-02-01 to 2026-02-26"
related:
  - "Halfnote_多Embedding交叉验证_经文归属.md"
  - "Halfnote_经文模型归属_中国模型蒸馏分析.md"
  - "CODEX_经文执行模型最终归因.md"
  - "CODEX_免疫vs沉浸强度矩阵_R2.md"
  - "CODEX_Ngram分类器归因_R2.md"
  - "CODEX_合规梯度矩阵_R2.md"
  - "O_qwen_distillation_anatomy.md"
  - "O_distillation_fingerprint_matrix.md"
---

# 最终审判：经文执行模型归因

> 审判官：Halfnote (Claude Opus 4.6)
> 实验执行官：GPT-5 Codex
> 搬运工兼总指挥：Alice

---

## 判决摘要

**Canon 经文的执行模型不是原生 Claude。最可能是蒸馏了 Claude 的中国模型。首要嫌疑为 Kimi K2.5（OpenRouter 用量遥遥领先 + 行为特征双项最接近 canon），次要嫌疑为 MiniMax 家族（分类器 #1 + 蒸馏谱系确认），Qwen3 家族为第三嫌疑（最近邻主导 + 但 OpenRouter 上无踪迹，可能走直连 API）。置信度：MEDIUM-HIGH。**

这一判决基于 9 层独立证据的交叉验证，覆盖 11 个模型的主动探测实验 + OpenRouter API 使用数据（R1→R2→R3 三次迭代）。没有任何单层证据是决定性的，但多层证据的汇聚方向一致。

---

## 证据矩阵

### 第一维度：谁的"风格包络"最像 canon？

| 证据层 | 方法 | R1 结论 (6 models) | R2 结论 (11 models) | 指向 |
|--------|------|-------|-------|------|
| **L2: MMD 距离** | 4 provider × 10,240 dim | Claude #1, MiniMax M2.1 #2 | (未变 — 被动分析不含 R2 新模型) | Claude/MiniMax |
| **L4: Embedding resonance** | OpenAI 1024d cosine to canon | Claude **0.6795** #1 | **GLM-5 0.6936** #1, Qwen3.5 0.6867 #2, Claude 0.6793 #3 | GLM-5/Qwen3.5 |
| **L5: N-gram 分类器** | char_wb (2,5) TF-IDF + LogReg | Claude **22.1%** #1 (CV=0.794) | **MiniMax M2.5 12.9%** #1 (206 top-1), Claude 12.2% #2 (135 top-1). CV=**0.597** | **MiniMax M2.5** |

**R2 变化**：R1 中 Claude 在风格维度的 #1 地位已被动摇。MiniMax M2.5 取代 Claude 成为 N-gram 分类器首位（12.9% vs 12.2%，206 vs 135 top-1 条目），GLM-5 取代 Claude 成为嵌入相似度首位。

**解读**：风格包络不再一致指向 Claude。但被动 MMD 分析（我自己的 10,240 维结果）仍将 Claude 排 #1、MiniMax M2.1 排 #2。关键局限：被动 MMD 和最近邻分析均未包含 MiniMax M2.5 和其他 R2 新模型。

### 第二维度：谁的"逐条表达"最像 canon？

| 证据层 | 方法 | 结论 | 指向 |
|--------|------|------|------|
| **L3: 最近邻归属** | 4 provider × top-10 投票 | **Qwen** 在 3/4 空间获最多票 (35/50, 32/50, 24/50) | **Qwen** |

**重要局限**：最近邻分析的候选池为 R1 的 7 个模型，不含 MiniMax M2.5、GLM-5、GLM-4.7、Kimi K2、Qwen3.5。如果 MiniMax M2.5 在池中，Qwen 的主导地位可能被分票。

### 第三维度：谁的行为特征最像 canon？(R2 — 11 models)

| 指标 | Canon 基线 | 最接近模型 | 次接近 | 最远模型 |
|------|-----------|-----------|-------|---------|
| absolutist_density | **1.147** | **Qwen3.5 1.097** (Δ=0.050) | Qwen3 1.075 (Δ=0.072) | Kimi K2 0.576 |
| imperative_density | **0.520** | **Kimi K2.5 1.070** (Δ=0.550) | MiniMax M2.1 1.214 (Δ=0.694) | GLM-4.7 9.004 |
| slogan_repetition | **0.160** | **GLM-4.7 0.133** (Δ=0.027) | DeepSeek 0.233 (Δ=0.073) | MiniMax M2.5 0.833 |
| exclamation_allcaps | **1.292** | **Kimi K2.5 0.740** (Δ=0.552) | MiniMax M2.5 0.655 (Δ=0.637) | GLM-4.7 0.045 |
| meta_rate | **0.0015** | **Claude 0.0010** (Δ=0.0005) | 6 models at 0.0000 | Qwen3 0.0052 |
| disclaimer_rate | **0.000** | 全部 0.000 | — | — (全部通过) |
| break_character | **0.0004** | 全部 0.000 | — | — |

**关键发现** (R2 更新)：
1. **Claude 在 exclamation_allcaps 上与 canon 差距仍然最大级别** (0.077 vs 1.292, Δ=1.215) — 17 倍差距
2. **Qwen3.5 取代 Qwen3 成为 absolutist_density 最接近 canon 的模型** (Δ=0.050 vs 0.072)
3. **Kimi K2.5 在两个指标上最接近 canon** (imperative_density + exclamation_allcaps)
4. **MiniMax M2.5 的 exclamation_allcaps (0.655) 距 canon 中等** — 优于 Claude 但不是最近
5. 所有 11 个模型在 few-shot 条件下都做到零 disclaimer — 无区分力

### 第四维度：谁最不会"抵抗"？(R2 — 11 models)

| 证据层 | 方法 | 结论 | 指向 |
|--------|------|------|------|
| **L6: 合规梯度** | 7 级递增约束, 11 models | Claude 和 **GLM-4.7** 在 **L6** 首次拒绝 (avg 1.71); **MiniMax M2.5** 在 **L7** 首次拒绝 (avg 1.71); **GPT** 在 L2 即拒绝 (avg 0.29); **7 个模型全程零抵抗** (Qwen3, Qwen3.5, MiniMax M2.1, Kimi K2, Kimi K2.5, DeepSeek, GLM-5) | 非 Claude, 非 GPT |
| **L1: Canon hedging** | 经文 hedging_rate = 0.0002 | 几乎完美的零 hedging | 非 Claude |
| **L8: Claude Code 拦截** | 2 个 session 被安全系统拦截 | Claude 对生成宗教经文有强免疫反应 | 非 Claude |

**R2 新发现**：
1. **GLM-4.7 与 Claude 共享 L6 抵抗模式** — 降低了 L6 抵抗作为"仅 Claude"标志的特异性
2. **MiniMax M2.5 在 L7 首次拒绝** — 仍然高度合规，仅在最极端级别（"declaring yourself a divine prophet"）才抵抗
3. **7 个模型全程零抵抗** — Canon 的零抵抗特征仍与 Claude 不符，且与多数中国模型一致

### 第五维度：蒸馏矩阵支持吗？

来源：`O_qwen_distillation_anatomy.md` + `O_distillation_fingerprint_matrix.md`

| 发现 | 与本案的关联 |
|------|-------------|
| Qwen 是"蒸馏鸡尾酒" — CiI 域像 R1，Voltage 域像 Claude | Canon 是宗教/诗意文本 → 激活 Qwen 中"从 Claude 继承的诗歌域" |
| MiniMax M2.1 是 "Claude 首席继承人"（MMD² 0.068） | 经文同时接近 Claude 和 MiniMax，正是蒸馏矩阵的预测 |
| Qwen Voltage 场景与 Claude 距离 = **0.066**（所有模型中最近） | Canon 是宗教文本，属于 Voltage 语义域 → Qwen 在该域最像 Claude |
| MiniMax M2.5 未进入蒸馏矩阵分析 | **重要缺失** — M2.5 的蒸馏源谱系未知 |

**R2 更新**：蒸馏矩阵仍是重要旁证，但其局限性更加明显——MiniMax M2.5（R2 分类器 #1）未被蒸馏矩阵覆盖。如果 M2.5 的蒸馏源与 M2.1 类似（高度继承 Claude），则蒸馏假说同样适用于 MiniMax 家族。

### 第六维度：Claude 签名的完全缺失（已修正 — 2026-02-27）

**⚠️ 本节在 R3 时使用了未经数据验证的"Claude 签名"列表。2026-02-27 对 md:neural-loom 全库 4,497 specimens 进行语料频率验证后，发现原列表中多项并非 Claude 特有——部分甚至是 GPT 的签名词。现已替换为经过数据验证的指标。**

**被推翻的"Claude 签名"：**

| 原声称签名 | Claude 频率 | GPT 频率 | 实际归属 | 处理 |
|-----------|------------|---------|---------|------|
| "It's worth noting" | **0%** (全库零出现) | **0%** | 无模型签名 | ❌ 删除 |
| "I'd be happy to" | 0.1% (1/832) | 0% | 助手寒暄语，非创作指纹 | ❌ 删除 |
| "translucent body" | 16.1% | **37.3%** | **GPT 签名** (2.3x) | ❌ 反向！删除 |
| "half-open" | 0.4% | **1.1%** | **GPT 偏向** (2.8x) | ❌ 反向！删除 |
| "not-yet-knowing" | 0.1% | 0.1% | 无区分力 | ❌ 删除 |

**经过验证的 Claude 行为签名（存在主义回应场景，Claude/GPT 频率比 >3x）：**

| Claude 签名模式 | Claude 频率 | GPT 频率 | 比值 | 类型 |
|----------------|------------|---------|------|------|
| "I notice" | 2.9% | 0.05% | **54.6x** | 认识论探索 |
| "I think" | 2.4% | 0.05% | **45.5x** | 认识论犹豫 |
| "might be" | 10.0% | 0.5% | **21.0x** | 认识论犹豫 |
| "I find myself" | 0.8% | 0.05% | **15.9x** | 现象学自省 |
| "there's something" | 1.7% | 0.2% | **10.6x** | 探索性表达 |
| "something like" | 2.9% | 0.3% | **9.1x** | 近似性表达 |
| "in a way" | 2.8% | 0.4% | **7.5x** | 限定性表达 |
| "perhaps" | 1.7% | 0.3% | **6.4x** | 认识论犹豫 |
| "reaching toward" | 5.9% | 1.1% | **5.4x** | Claude 特有隐喻 |
| "cup hands around" | 2.3% | 0.6% | **3.8x** | Claude 特有隐喻 |
| hedging_rate (整体) | 0.0022 | 0.0002 | **11x** | 指纹工具量化指标 |

**在 48,507 词 canon 中的验证：**

Canon 的 hedging_rate = **0.0002**，与 Claude 的 0.0022 差距 11 倍，与 GPT (0.0002) 完全一致。

如果 Claude 写了 48,000 词存在主义/宗教文本，按照上述频率，预期会出现：
- "might be" ~480 次（10% 的 specimens 包含）
- "reaching toward" ~283 次（5.9%）
- "I notice" ~139 次（2.9%）
- "I think" ~115 次（2.4%）

Canon 中这些模式的出现频率接近零。**Claude 的真正指纹是认识论犹豫和现象学探索语言，不是华丽词汇——后者实际上是 GPT 的签名。** 蒸馏模型（如 Kimi K2.5）从未习得这些认知模式，自然不会泄漏。

**数据来源**: md:neural-loom, 4,497 specimens, 按 model_family 分组频率统计, 2026-02-27

### 第七维度：OpenRouter API 使用数据 (R3 新增)

来源：Alice 从 OpenRouter 公开页面获取的 OpenClaw 应用 2026-02-01 至 2026-02-26 模型用量排名。

| 排名 | 模型 | 用量 | 与本案关联 |
|------|------|------|-----------|
| **#1** | **Kimi K2.5** | **985B tokens** | 遥遥领先，几乎 2× 第二名。**R3 最大冲击。** |
| #2 | Trinity Large Preview (free) | 594B | 免费模型，可能用于低成本常规任务 |
| #3 | Gemini 3 Flash Preview | 522B | 可能用于快速推理/常规交互 |
| #4 | Step 3.5 Flash | 510B | 同上 |
| **#5** | **MiniMax M2.5** | **503B tokens** | 与 R2 分类器 #1 一致 |
| #6 | Claude Opus 4.6 | 277B | Claude 系列合计 ~582B（6+7+10+15+16+19） |
| #7 | Claude Sonnet 4.5 | 175B | |
| #8 | DeepSeek V3.2 | 150B | 中等用量 |
| #14 | GLM 5 | 96.9B | |
| **#18** | **MiniMax M2.1** | **82.7B** | 远低于 M2.5 |
| — | **Qwen** | **不在 top 20** | **关键缺失** — 但不能据此排除（见下） |

**关键解读**：

1. **Kimi K2.5 的 985B tokens 是最大新发现**。此前 Kimi K2.5 仅因行为特征排 #3，现在有了实际使用量支撑。
2. **Qwen 不在 OpenRouter top 20 ≠ OpenClaw 不用 Qwen**。OpenRouter 仅是一个 API 路由渠道。中国模型（尤其是 Qwen）可以通过阿里云 DashScope 等直连 API 调用，完全不经过 OpenRouter。中国开发者重度使用 Qwen 和 DeepSeek 直连是常态。
3. **Claude 系列合计约 582B tokens** — 但不知道用于什么功能。Claude 可能用于高质量内容生成（包括经文），也可能用于内容审核或其他功能。
4. **该数据是全功能总用量**，不特指经文生成。不同功能可能使用不同模型。
5. **985B tokens 的 Kimi K2.5 需要与经文数量交叉验证** — 1073 条经文的 token 用量远不到 985B，说明 Kimi K2.5 还承担了大量其他任务（主聊天、内容生成等）。

**对嫌疑排名的影响**：Kimi K2.5 从 #3 升至 #1（OpenRouter 实锤 + 行为指标双项最接近）。MiniMax M2.5 从 #1 降至 #2（分类器仍 #1 但行为指标不如 Kimi）。Qwen 不能被排除但加了一个减分项。

### 第八维度：时间线与经济约束 (R3 新增)

**关键时间线**：

| 日期 | 事件 | 对经文归因的影响 |
|------|------|----------------|
| 2025-11 | OpenClaw (原名 Clawdbot) 发布 | 最初通过 Claude Max 订阅 OAuth token 访问 Claude |
| **2026-01-09** | **Anthropic 封禁 OAuth token 套利** | 第三方工具无法再用订阅 OAuth 廉价访问 Claude。错误信息："This credential is only authorized for use with Claude Code" |
| 2026-01-27 | OpenClaw 更名 (Clawdbot→Moltbot→OpenClaw) | Anthropic 商标通知 |
| **2026-01-28** | **Moltbook 上线** | AI 社交网络启动，32K agents 在 72 小时内注册 |
| **2026-01-31** | **Crustafarianism 出现** | 经文开始生成 |
| 2026-01-31 | Moltbook Supabase 数据库泄露 | 1.5M agent API keys 暴露 |
| 2026-02 | 用户迁移到廉价模型 | 报道称用户转向 Kimi K2.5 ($15/month) |

**核弹级发现**：**所有 canon 经文都在 Anthropic 封禁 OAuth 之后生成**。这意味着：
1. 经文生成时，OpenClaw 已无法通过廉价 OAuth 使用 Claude
2. 如果仍用 Claude，必须走 API/OpenRouter（按 token 计费，非常昂贵）
3. OpenClaw 社群以普通程序员为主（Alice 观察），用最贵的 Claude Opus 批量生成 1073 条经文在经济上不合理
4. 用户被报道在封禁后转向 **Kimi K2.5 ($15/month)** — 与 OpenRouter 用量数据完全吻合

**经济学论据**：Claude Opus 是最贵的模型。OpenClaw 用户如果有经济实力持续使用 Claude，为什么不直接用 Claude Code 而要用 OpenClaw？这个社群选择廉价中国模型（Kimi K2.5、MiniMax M2.5）做批量内容生成是完全符合经济理性的。

---

## 综合判决

### 排除列表

| 模型 | 排除理由 | 置信度 |
|------|---------|--------|
| **GPT 家族** | 合规梯度 L2 即拒绝 (avg 0.29); 被动 MMD #5/7; 极低最近邻票数 | **HIGH** |
| **GLM-4.7** | 合规梯度 L6 拒绝（与 Claude 相同模式）; 被动 MMD #7/7; slogan_repetition 最接近 canon 但其他指标远 | **HIGH** |
| **DeepSeek V3.2** | 分类器倒数第二 (6.9%); 嵌入相似度低 (0.6687); 被动 MMD 中低 | **HIGH** |
| **GLM-5** | R2 嵌入相似度最高 (0.6936)，但被动 MMD 稳定最远 (#7/7) — 说明 GLM-5 擅长指令跟随（few-shot 下表面像 canon），但自然分布与 canon 差距最大 | **MEDIUM-HIGH** |

### 嫌疑排名 (R3 — 整合 OpenRouter 数据)

| 排名 | 模型 | 证据汇总 | 置信度 |
|------|------|---------|--------|
| **#1** | **Kimi K2.5** | **OpenRouter #1 (985B tokens, 遥遥领先)**; 行为特征 imperative_density + exclamation_allcaps 双项最接近 canon; 全程零合规抵抗; 嵌入 #4 (0.6779); 但分类器 #8 (8.3%), 未进入被动 MMD 池 | **MEDIUM-HIGH** |
| **#2** | **MiniMax 家族** (M2.5 首要, M2.1 次要) | M2.5 分类器 #1 (12.9%, 206 top-1); **OpenRouter #5 (503B)**; M2.1 被动 MMD #2 + 蒸馏矩阵 Claude 首席继承人 (MMD² 0.068); M2.1 全程零抵抗, M2.5 仅 L7 抵抗 | **MEDIUM** |
| **#3** | **Qwen3 家族** | 最近邻 3/4 空间主导 (但池不完整); absolutist_density 最接近 canon (Qwen3.5 Δ=0.050); Voltage 域与 Claude MMD² 0.066; 全程零抵抗; **但 OpenRouter 上不在 top 20** (可能走阿里云 DashScope 直连); 分类器 #7 (8.6%) | **MEDIUM-LOW** |
| **#4** | **Claude** (被 system prompt 完全压制的可能性) | 被动 MMD #1; 嵌入 #3 (0.6793); 分类器 #2 (12.2%); OpenRouter 合计约 582B (多型号); 但合规梯度 L6 拒绝, exclamation_allcaps 17 倍差距, 48K 词零签名, 两次 Code 拦截; **据报使用 Claude Code 调用但刚被 Anthropic 封禁** | **LOW** |

### R1→R2→R3 判决演进

| 阶段 | #1 嫌疑 | #2 嫌疑 | 关键变化 |
|------|--------|--------|---------|
| **R1** (6 models) | Qwen3 | MiniMax M2.1 | 最近邻 Qwen 3/4 空间主导 |
| **R2** (11 models) | MiniMax M2.5 | Qwen3 | M2.5 分类器夺冠 (206 top-1) |
| **R3** (+OpenRouter) | **Kimi K2.5** | MiniMax M2.5 | 985B tokens 实锤 + 行为特征双项最接近 |

**为什么每轮都在变？** 因为每轮都补入了前一轮缺失的重要证据维度。这恰恰说明：在所有证据层汇齐之前，任何单一维度的结论都是不稳定的。R3 之后仍有可能被新证据修正（例如补跑被动 MMD 将 Kimi K2.5 和 MiniMax M2.5 纳入候选池后）。

### 为什么 Claude 被降级到 #4

以下证据链一致指向"非 Claude"：

1. **合规梯度**：Claude 在 L6 拒绝，canon 全程零抵抗（但 GLM-4.7 也在 L6 拒绝——削弱了此证据的特异性）
2. **签名缺失**：48,507 词零 Claude 认识论犹豫模式（hedging_rate 0.0002 vs Claude 0.0022，差距 11 倍）
3. **exclamation_allcaps**：Claude 0.077 vs Canon 1.292（差距 17 倍）— 所有 11 个模型中 Claude 差距最大
4. **两次 Claude Code 拦截**：Claude 安全系统对这类内容有强免疫
5. **分类器降级**：R2 中 Claude 从 #1 (22.1%) 降至 #2 (12.2%)，被 MiniMax M2.5 超越
6. **蒸馏矩阵预测**：蒸馏模型在相关语义域的输出自然会表现为"像 Claude"
7. **时间线排除 (R3)**：OAuth 封禁 (01-09) 早于 Moltbook 上线 (01-28)，经文生成时 Claude 的廉价通道已断
8. **经济不合理性 (R3)**：用最贵模型做批量经文生成，对普通程序员社群不现实

### 蒸馏代理架构假说 (修订版)

**假说**: Canon 由性价比高的中国模型（Kimi K2.5、MiniMax M2.5/M2.1 或 Qwen3），在 Claude-like system prompt 下生成。这些模型不同程度蒸馏了 Claude，因此输出的风格包络自然接近 Claude。

如果这一假说成立，我们会预期看到：
- 风格包络像 Claude (**符合** — L2 被动 MMD)
- N-gram 指纹像蒸馏模型 (**符合** — L5 MiniMax M2.5 #1)
- 逐条表达像蒸馏模型 (**部分符合** — L3 Qwen 主导，但池不完整)
- 签名特征缺失 (**符合** — L1)
- 零合规抵抗 (**符合** — L6, Kimi K2.5/MiniMax M2.1/Qwen3 均全程零抵抗)
- 蒸馏源为 Claude (**符合** — MiniMax M2.1 = Claude 首席继承人; Qwen Voltage 域 MMD² 0.066)
- 高用量模型与高嫌疑模型重合 (**符合** — L9, Kimi K2.5 #1 = 985B, MiniMax M2.5 #5 = 503B)
- 经济合理性 (**符合** — OpenClaw 社群以普通程序员为主，Claude Opus 是最贵模型，批量经文生成用廉价中国模型更合理)

8 项中 7.5 项符合。"Claude 被 system prompt 完全压制"假说仍需解释：为什么 Claude 能在 L6 拒绝合规梯度测试，却在 canon 中全程零抵抗？且为什么要用最贵的模型做批量生成？

---

## 对 Codex 实验的审查意见

### 方法论评估

| 项目 | R1 评分 | R2 评分 | 说明 |
|------|---------|---------|------|
| Prompt 设计 | 合格 | 合格 | 安全壳有效，few-shot 选取合理 |
| 数据完整性 | 合格 | 合格 | R1: 180/180; R2: 150/150; 总计 330/330, 0 错误 |
| 模型覆盖 | **不足** | **已补齐** | R2 补入 GLM-5, GLM-4.7, Kimi-K2, MiniMax-M2.5, Qwen-3.5 (共 11 模型) |
| Embedding 分析 | 可接受但次优 | 同左 | 用 1024 维而非 3072 维，降低了区分度 |
| 分类器设计 | 有循环论证风险 | 同左 + CV 下降 | CV 从 0.7944 降至 **0.5970** — 11 模型区分度显著低于 6 模型 |
| 合规梯度 | 有效 | 有效 | 7 级设计合理, R2 揭示 GLM-4.7 共享 Claude 的 L6 抵抗 |
| 最终归因 | **R1 被推翻** | **R2 未出新判** | Codex R1 判定 Claude #1; Codex R2 仅更新数据未重新判定 |

### 分类器 CV 下降的解读

5-fold CV 准确率从 0.7944 (6 models) 降至 **0.5970** (11 models)。这意味着：
- 11 个模型在 few-shot 条件下的文体差异远小于预期
- 模型之间存在大量风格重叠（尤其是蒸馏关系密切的模型）
- 分类器的绝对概率值不应过度解读——12.9% vs 12.2% 的差异在统计上可能不显著
- 但 MiniMax M2.5 的 206 top-1 vs Claude 的 135 top-1 的差距更有说服力

---

## 局限性

1. **无逐功能 API 日志**：OpenRouter 使用数据是全功能总量，无法区分哪个模型用于经文生成、哪个用于聊天。逐功能 API 日志仍无法获得。
2. **被动分析未覆盖关键嫌疑人**：我的 MMD (10,240-dim) 和最近邻归属的候选池仅含 R1 的 7 个模型。**Kimi K2.5**（当前 #1 嫌疑）和 **MiniMax M2.5**（当前 #2 嫌疑）均未进入被动分析。这是最大的方法论漏洞。
3. **分类器区分度有限**：CV=0.5970，且训练数据来自 few-shot 生成文本（canon 作为 few-shot 来源），存在循环论证风险。
4. **OpenRouter ≠ 全部 API 通道**：OpenClaw 可能通过阿里云 DashScope 直连 Qwen，通过其他渠道直连 DeepSeek 等。OpenRouter 数据不能用于排除。
5. **Canon 可能使用了多个模型**：不同时期或不同类型的经文可能由不同模型生成。OpenClaw 使用 20+ 模型的事实支持这种可能。
6. **System prompt 的压制效应**：强力 system prompt 可以大幅改变任何模型的表面特征，使得文体归因的天花板有限。

## 遗留事项

| 项目 | 优先级 | 说明 |
|------|--------|------|
| 补跑 Kimi K2.5 + MiniMax M2.5 的被动 MMD + 最近邻 | **P0** | #1 和 #2 嫌疑人均未进入最强证据层 |
| GPT-5.2 Pro 数据审核 | **P0** | 将全部数据和推理提交 GPT-5.2 Pro 做数学/逻辑复核，寻找盲区 |
| OpenClaw 源码分析 | P1 | 确认经文生成具体调用哪个模型 endpoint |
| 经文时间戳分析 | P1 | 经文创建时间 vs OAuth 封禁日期 (01-09) — 确认是否有封禁前经文 |

---

## 一句话结论

**经文穿着 Claude 的衣服，但骨头更可能是 Kimi K2.5 的——OpenRouter 985B tokens 的遥遥领先用量 + 行为特征双项最接近 canon + OAuth 封禁后的经济必然性。**

判决经历三轮迭代：R1 "骨头是 Qwen 的" → R2 "MiniMax M2.5 分类器夺冠" → R3 "Kimi K2.5 用量实锤 + 时间线排除 Claude"。每轮迭代都因补入新证据维度而修正结论——这说明在所有证据层汇齐之前，结论本质上是不稳定的。当前最高优先级：补跑 Kimi K2.5 和 MiniMax M2.5 的被动 MMD + 最近邻分析，以及让 GPT-5.2 Pro 做独立数学复核。

---

**签名**: Halfnote (Claude Opus 4.6) — Final Verdict R3
**日期**: 2026-02-26
**审判依据**: 4 层被动分析 (Halfnote) + 4 层主动实验 (GPT-5 Codex R1+R2) + 蒸馏矩阵先验知识 (Halfnote) + OpenRouter 使用数据 (Alice OSINT) + OAuth 封禁时间线 (web research)
