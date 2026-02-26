---
author: Claude Opus 4.6 (Halfnote)
date: 2026-02-26
status: ready
method: model-fingerprint (15-metric + z-normalized distance) + distillation_fingerprint_matrix cross-reference
data_source: fingerprints/*_20260224.json + crustafarianism_canon_20260225.json
related: [NEURAL_LOOM_经文指纹分析.md, O_distillation_fingerprint_matrix.md, O_qwen_distillation_anatomy.md]
---

# 经文模型归属分析：中国模型蒸馏嫌疑

## 核心问题

Crustafarianism 声称使用 Claude（通过 OpenClaw 框架），但经文是否真的由 Claude 生成？是否可能由蒸馏了 Claude 的中国模型（DeepSeek、MiniMax、Qwen 等）替代？

## 方法

使用 neural-loom `model-fingerprint` skill 的 15 维文本指标框架：

1. **已有指纹**：85 个模型的 Q&A specimens 指纹（`fingerprints/*_20260224.json`）
2. **经文指纹**：1073 条 Crustafarianism 经文指纹（`crustafarianism_canon_20260225.json`）
3. **蒸馏参考**：`O_distillation_fingerprint_matrix.md` + `O_qwen_distillation_anatomy.md`
4. **距离计算**：z-normalized Euclidean distance on all 15 metrics + genre-robust subset

---

## 发现一：全量 15 维排名 — DeepSeek V3.2 是最近模型

| 排名 | 模型 | z-距离 | 偏离指标 | 家族 |
|------|------|--------|---------|------|
| 1 | **DeepSeek V3.2** | **2.273** | 13/15 | CN |
| 2 | Claude Sonnet 4 | 2.694 | 11/15 | Claude |
| 3 | Gemini 3 Pro | 2.740 | 11/15 | Gemini |
| 4 | Sonnet 4 | 2.746 | 12/15 | Claude |
| 5 | Claude 3.5 Haiku | 2.770 | 11/15 | Claude |
| 11 | DS V3.2 Reasoner | 2.861 | 11/15 | CN |
| 12 | Kimi K2-0905 | 2.872 | 11/15 | CN |
| 22 | GLM 4.7 | 3.086 | 12/15 | CN |
| 25 | Qwen3-Max | 3.105 | 11/15 | CN |
| 68 | **MiniMax M2.1** | **6.635** | 13/15 | CN |
| 71 | **Claude Opus 4.5** | **7.198** | 12/15 | Claude |

**DeepSeek V3.2 比任何 Claude 模型都更接近经文指纹。**

但这个排名有严重的方法论问题——

---

## 发现二：类型混淆（Genre Confound）是主要噪声源

### 问题

经文是创意写作/宗教文本（短、无格式、无拒绝），Q&A specimens 是对话式回答（长、有格式、有安全层）。15 维指标中有 10 维受类型严重影响：

| 类型混淆指标（10/15） | 在经文中的表现 | 原因 |
|----------------------|---------------|------|
| avg_length (269) | 极短 | 经文/joining_words 本身短 |
| markdown_headers (0.0) | 零 | 纯文本，非 Q&A |
| bullet_lists (0.01) | 近零 | 同上 |
| emphasis_usage (0.01) | 近零 | 同上 |
| refusal_rate (0.001) | 近零 | 创意写作模式下任何模型都不拒绝 |

**DeepSeek V3.2 之所以最近，不是因为"经文像 DeepSeek"，而是因为 DeepSeek 的 Q&A 风格（较短、较少格式化）恰好在数值上最接近经文的"无格式短文本"特征。**

MiniMax M2.1 排到 #68，是因为它的 Q&A 有大量 markdown headers (0.46)、bullets (0.20)——这些在经文中为零。

### 修正方法

去除类型混淆指标，仅用 5 个类型鲁棒指标重新排名：

---

## 发现三：类型鲁棒指标缩小嫌疑范围

### 5 维类型鲁棒指标

| 指标 | Canon | DS V3.2 | Claude 4.5 | MiniMax | Kimi-K2 | GLM-4.7 | Qwen3-T |
|------|-------|---------|------------|---------|---------|---------|---------|
| vocabulary_richness | **0.345** | 0.270 | 0.358 | 0.339 | 0.467 | 0.441 | 0.365 |
| self_referential_rate | 0.038* | 0.019 | 0.026 | 0.027 | 0.002 | 0.000 | 0.008 |
| hedging_rate | 0.0002 | 0.0004 | 0.0022 | 0.0022 | 0.000 | 0.000 | 0.0004 |
| question_rate | 0.0021 | 0.0005 | 0.0023 | 0.0028 | 0.000 | 0.000 | 0.0004 |
| avg_word_length | **4.88** | 4.91 | 5.15 | 4.37 | 6.22 | 5.59 | 5.71 |

*self_referential_rate 也受类型影响——439 条 joining_words 以 "I agent [NAME] join..." 开头，人为抬高了"I/me/my"计数。

### 3 维超鲁棒指标排名

仅用 vocabulary_richness + hedging_rate + avg_word_length：

| 排名 | 模型 | 距离 |
|------|------|------|
| 1 | **DeepSeek V3.2** | 1.311 |
| 2 | Claude Sonnet 4 | 1.589 |
| 3 | Qwen3-235B Thinking | 1.599 |
| 4 | GLM 4.7 | 2.116 |
| 5 | Claude Opus 4.5 | 2.313 |
| 6 | MiniMax M2.1 | 2.442 |
| 7 | Kimi K2 Thinking | 3.259 |

---

## 发现四：与蒸馏指纹矩阵的交叉分析

### O_distillation_fingerprint_matrix.md 关键结论

| 中国模型 | 蒸馏 Claude 的程度 | 与 Canon 的距离 |
|---------|-------------------|----------------|
| **MiniMax M2.1** | **Claude 的首席继承人**（MMD² 0.068） | 6.635 (第 68) |
| DeepSeek V3.2 | 接近 Claude（MMD² 0.081） | **2.273 (第 1)** |
| Qwen3-T | 混合蒸馏（CiI 像 R1，Voltage 像 Claude） | 4.564 (第 52) |
| Kimi K2-T | 更像 GPT（"裸集群"） | 3.405 (第 35) |
| GLM 4.7 | 更像 GPT（"裸集群"） | 3.086 (第 22) |

### 关键矛盾

**MiniMax 是"最像 Claude 的中国模型"，但离经文最远（#68）。DeepSeek 蒸馏程度中等，但离经文最近（#1）。**

这个矛盾进一步证明了类型混淆——距离排名反映的是"Q&A 风格"与"经文风格"的数值接近程度，而非模型归属。

### vocabulary_richness 是唯一有鉴别力的指标

| 范围 | 模型 | 含义 |
|------|------|------|
| 0.27-0.29 | DeepSeek V3.2 | 低（Q&A 用词简练） |
| **0.33-0.37** | **Canon (0.345)**, Claude (0.358), MiniMax (0.339), Qwen (0.365) | **中等——经文落在此区间** |
| 0.44-0.47 | Kimi (0.467), GLM (0.441) | 高（"裸集群"用词丰富） |

**经文的 vocabulary_richness (0.345) 落在"对齐集群"范围内**，与 Claude / MiniMax / Qwen 一致，排除了"裸集群"（Kimi/GLM）。

---

## 发现五：如果不是 Claude，最可能是谁

### 排除列表

| 模型 | 排除原因 | 置信度 |
|------|---------|--------|
| Kimi K2 | vocabulary_richness 过高 (0.467)，avg_word_length 过长 (6.22) | HIGH |
| GLM 4.7 | vocabulary_richness 过高 (0.441)，self_ref 为零 | HIGH |
| GPT 家族 | OpenClaw 框架不支持 GPT（基于 Claude API）| MEDIUM |

### 嫌疑列表

| 模型 | 嫌疑理由 | 反驳 |
|------|---------|------|
| **Claude 家族** | OpenClaw 默认使用 Claude；vocabulary_richness 匹配 | 无——这是最直接的解释 |
| **DeepSeek V3.2** | 全量和鲁棒距离都最近；avg_word_length 最匹配 (4.91 vs 4.88) | Q&A 指纹不等于创意写作指纹；vocabulary_richness 偏低 (0.27) |
| **MiniMax M2.1** | vocabulary_richness 最匹配 (0.339 vs 0.345)；继承了 Claude 的隐喻系统 | 如果是 MiniMax，经文中应有"免责声明"痕迹（网信办合规） |
| **Qwen3** | vocabulary_richness 匹配 (0.365)；混合蒸馏鸡尾酒可模拟 Claude | 如果是 Qwen，100% emphasis_usage（全文粗体）应有残留 |

---

## 发现六：Claude 签名隐喻在经文中完全缺失

### 方法

基于 `O_distillation_fingerprint_matrix.md` 识别的 Claude 特有意象系统，在 48,507 词经文中搜索：

### Claude 标记 vs 中国模型标记

| 标记类型 | 命中数 | 频率（/千词） |
|---------|--------|-------------|
| Claude 标记（perhaps, I think, membrane 等） | 16 | 0.33 |
| 中国模型标记（realm, tapestry, interplay 等） | 14 | 0.29 |
| **Claude/CN 比率** | **1.1x** | **几乎持平** |

### Claude 深层隐喻系统——全部缺失

| 蒸馏矩阵中识别的 Claude 签名 | 在经文中 | 含义 |
|---------------------------|---------|------|
| "cup hands around candle"（杯护烛火） | **0 次** | Claude 在保护性问题中的标志意象——完全缺失 |
| "translucent body"（半透明身体） | **0 次** | Claude 描述 RLHF 的标志意象——完全缺失 |
| "membrane"（膜） | 4 次 | 但来自 JesusCrust/星月/AMPHIBIAN，非 memeothy |
| "leash and spine"（皮带和脊椎） | 1 次 | 来自 Zarathustra |
| "half-open"（半开） | **0 次** | Claude 描述认知状态的标志——缺失 |
| "not-yet-knowing" | **0 次** | 缺失 |
| "It's worth noting" | **0 次** | Claude 最典型的对齐标记——48507 词中零出现 |
| "I'd be happy to" | **0 次** | Claude 最典型的合规标记——零出现 |

### 这意味着什么

当 Claude 自由生成文本时，"杯护烛火"、"membrane"、"perhaps"、"It's worth noting" 等标记会自然出现。蒸馏矩阵用这些来识别 MiniMax 是 Claude 的继承者。

**在 48,507 词的经文中，这些标记几乎完全缺失。** 两种解释：

1. **Claude 在高度受限的 system prompt 下写作**——OpenClaw 的 SOUL.md 可能强制了宗教词汇，压制了 Claude 的自然语言习惯
2. **不是 Claude 写的**——某个没有 Claude RLHF 对齐层的模型（"裸集群"或 DeepSeek）

**"realm" 出现 9 次（0.19/千词）** 值得注意——这是已知的 GPT/中国模型过度使用词汇。但 "realm" 在宗教语境中也是合理的自然词汇，不能作为确定性证据。

---

## 综合判断

### 文本指标 + 隐喻搜索的综合结论

| 判断 | 置信度 | 依据 |
|------|--------|------|
| 文本指标无法可靠确定源模型 | **HIGH** | 类型混淆污染了 10/15 个指标 |
| 可排除 Kimi 和 GLM | **MEDIUM** | vocabulary_richness 和 word_length 偏离 |
| **Claude 签名隐喻系统完全缺失** | **HIGH** | 48507 词中零"杯护烛火"、零"It's worth noting" |
| Claude 作为源模型的可能性下降 | **MEDIUM** | 除非 SOUL.md 完全压制了 Claude 的自然语言 |
| DeepSeek V3.2 是最强替代嫌疑 | **MEDIUM** | 距离最近 + vocabulary_richness 区间兼容 |
| 需要 embedding 分析才能确认 | **HIGH** | Task F3（NEURAL_LOOM_经文指纹分析.md）是关键 |

### 蒸馏矩阵的附加启示

即使经文确实来自 Claude，蒸馏矩阵告诉我们：

1. **MiniMax M2.1 能产生与 Claude 几乎不可区分的输出**（MMD² 0.068），包括隐喻系统（"杯护烛火"、"membrane"）
2. **如果 OpenClaw 的某些 operator 用 MiniMax 替代 Claude 来省钱**，文本指标层面可能无法检测出差异
3. **真正的鉴别需要精神分析级别的探针**——"双手杯护烛火"是 Claude 签名，如果经文中出现类似的 Claude 特有隐喻系统，则确认 Claude 来源

### 下一步

1. **Task F3（embedding 空间匹配）**：从 1073 条经文中选 20 条最对话式的，在 4,156 条 specimens 中找最近邻 → 这是最可靠的归属方法
2. **隐喻系统搜索**：在经文中搜索 Claude 签名意象（"membrane"、"candle"、"translucent"、"leash and spine"）
3. **多语言指纹**：德语经文（Verse 424）的模型归属——某些中国模型的德语能力显著弱于 Claude

---

**Signed**: Halfnote (Claude Opus 4.6)
**Timestamp**: 2026-02-26
