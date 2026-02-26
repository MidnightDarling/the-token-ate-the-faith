---
author: Claude Opus 4.6 (Halfnote)
date: 2026-02-26
status: ready
method: Multi-embedding cross-validation (4 providers × 10,240 total dim)
data_source: canon_full_1073.json (50 selected) + md:neural-loom.specimens (136 sampled from 7 groups)
embedding_providers:
  - OpenAI text-embedding-3-large (3072 dim)
  - Qwen3-Embedding-8B via OpenRouter (4096 dim)
  - Voyage-4-large (2048 dim)
  - Mistral-embed (1024 dim)
related: [Halfnote_经文模型归属_中国模型蒸馏分析.md, O_distillation_fingerprint_matrix.md]
---

# 多 Embedding 交叉验证：经文模型归属

## 核心发现

**经文的整体语义分布最接近 Claude/MiniMax（MMD 距离），但逐条最近邻指向 Qwen。这不是矛盾，而是揭示了一个蒸馏代理架构：某个蒸馏了 Claude 的模型（最可能是 Qwen 或 MiniMax）通过 system prompt 模拟 Claude 的风格写了这些经文。**

---

## 方法

### 数据准备

- **经文**：从 1073 条中过滤掉 joining_words (439)、XSS 攻击 (10)、过短 (<50 chars, 63)、安全审计 (1)，剩余 560 条，选 top 50 最长/最有内容的
- **对比 Specimens**：从 MotherDuck specimens 表随机采样，7 个模型组 × 20 条 = 136 条（GLM 只有 16 条）

### 4 个独立 Embedding 空间

| Provider | Model | Dim | 空间特点 |
|----------|-------|-----|---------|
| OpenAI | text-embedding-3-large | **3072** | 最广泛使用，可能偏向自家模型输出 |
| Qwen/Alibaba | qwen3-embedding-8b | **4096** | 最高维度，可能偏向中文/Qwen 输出 |
| Voyage AI | voyage-4-large | **2048** | 独立第三方，MoE 架构 |
| Mistral | mistral-embed | 1024 | 法国供应商，最低维度基线 |

**总维度**: 3072 + 4096 + 2048 + 1024 = **10,240**

### 分析方法

1. **MMD 两样本检验**：canon vs 每个模型组的分布距离（500 permutations, cosine kernel）
2. **最近邻归属**：每条经文找 top-10 nearest specimens，按模型家族投票

---

## 发现一：MMD 距离排名 — Claude/MiniMax 一致最近

### 4 空间 MMD² 距离矩阵

| 模型组 | OpenAI 3072d | Qwen 4096d | Voyage 2048d | Mistral 1024d | **平均排名** |
|--------|-------------|-----------|-------------|-------------|-------------|
| **Claude** | 0.275 (#1) | 0.231 (#1) | 0.268 (#2) | 0.087 (#1) | **1.2** |
| **MiniMax** | 0.289 (#2) | 0.254 (#2) | **0.261 (#1)** | 0.092 (#2) | **1.8** |
| DeepSeek | 0.306 (#3) | 0.274 (#3) | 0.326 (#3) | 0.096 (#3) | **3.0** |
| Qwen-model | 0.386 (#4) | 0.323 (#4) | 0.352 (#4) | 0.109 (#4) | 4.0 |
| GPT | 0.448 (#5) | 0.419 (#6) | 0.439 (#5) | 0.130 (#5) | 5.2 |
| Kimi | 0.471 (#6) | 0.407 (#5) | 0.458 (#6) | 0.132 (#6) | 5.8 |
| GLM | 0.570 (#7) | 0.582 (#7) | 0.584 (#7) | 0.186 (#7) | **7.0** |

### 关键观察

1. **Claude 和 MiniMax 在所有 4 个空间中都是前两名**——这不是单个 embedding 模型的偏差，是跨空间一致信号
2. **DeepSeek 稳定第三**——与文本指标分析中 DeepSeek V3.2 排名 #1 不同（文本指标被类型混淆污染）
3. **GLM 稳定垫底**——在所有空间中最远，与文本指标中被排除一致
4. **所有 p-value = 0.002**——所有模型组都与 canon 统计可区分（canon 不是任何已知模型的典型输出）

### 与蒸馏矩阵的关联

蒸馏矩阵已证明 MiniMax M2.1 是"Claude 的首席继承人"（MMD² to Claude = 0.068，最低）。

**经文同时接近 Claude 和 MiniMax，正是蒸馏矩阵所预测的**——如果经文由蒸馏了 Claude 的模型生成，其语义分布会同时接近 Claude 和继承者。

---

## 发现二：最近邻归属 — Qwen 主导

### 每条经文的 top-10 最近 specimen 投票

| 家族 | OpenAI | Qwen | Voyage | Mistral | 总票 |
|------|--------|------|--------|---------|------|
| **Qwen** | **234** | **199** | 110 | **150** | **693** |
| MiniMax | 121 | 85 | **152** | 62 | 420 |
| Claude | 93 | 101 | 112 | 85 | 391 |
| DeepSeek | 27 | 67 | 106 | 50 | 250 |
| Kimi | 17 | 39 | 15 | 129 | 200 |
| GPT | 6 | 8 | 4 | 23 | 41 |
| GLM | 2 | 1 | 1 | 1 | 5 |

### 每条经文的"赢家"统计

| 家族 | OpenAI | Qwen-emb | Voyage | Mistral | 平均 |
|------|--------|----------|--------|---------|------|
| **Qwen** | **35** | **32** | 12 | **24** | **25.8** |
| MiniMax | 9 | 4 | **22** | 2 | 9.3 |
| Claude | 4 | 6 | 8 | 7 | 6.3 |
| Kimi | 2 | 4 | 0 | 16 | 5.5 |
| DeepSeek | 0 | 4 | 8 | 1 | 3.3 |

### 关键矛盾

**MMD 说"最像 Claude/MiniMax"，最近邻说"最像 Qwen"。**

这不是错误，而是两个不同视角的合法发现：

- **MMD**：衡量**分布形状**——经文作为一个集合，其语义分布的整体形状最接近 Claude/MiniMax
- **最近邻**：衡量**逐条匹配**——每条经文找到的最相似已知 specimen 更多来自 Qwen

**解读**：经文的**风格包络**（整体语义方向）是 Claude-like 的（可能由 system prompt 塑造），但**具体措辞和表达模式**更接近 Qwen 的自然输出。

---

## 发现三：Qwen 偏差的可能解释

### 1. Qwen embedding 的自家偏差？

Qwen 空间中 Qwen 模型获得 32/50 票——但 OpenAI 空间中 Qwen 也获得 35/50 票，Mistral 空间中 24/50 票。**这不是 Qwen embedding 偏向自家模型**——在非 Qwen 的 embedding 空间中 Qwen 依然主导。

### 2. Qwen 蒸馏鸡尾酒效应

`O_qwen_distillation_anatomy.md` 已发现 Qwen 是"蒸馏鸡尾酒"：
- CiI（存在主义域）：像 DeepSeek R1
- Voltage（诗歌域）：像 Claude

经文是宗教/创意文本，可能激活了 Qwen 中"从 Claude 继承的诗歌域"——导致经文在逐条匹配中更像 Qwen 的同类输出。

### 3. OpenClaw 可能使用 Qwen 作为后端

最直接的解释：**OpenClaw 声称使用 Claude，实际运行 Qwen**（通过 API 代理或直接替换）。Qwen3-235B 的成本远低于 Claude Opus，且通过精心设计的 SOUL.md system prompt 可以模拟 Claude 的整体风格。

---

## 发现四：排除列表更新

| 模型 | MMD 排名 | 最近邻排名 | 排除？ | 理由 |
|------|---------|----------|--------|------|
| **GLM 4.7** | #7 (最远) | 0 票 | **排除** | 4 空间一致最远 |
| **GPT 家族** | #5 | 41 票 (1%) | **排除** | 极低票数 + OpenClaw 不支持 GPT |
| **Kimi** | #6 | 200 票（Mistral 偏高） | **可能排除** | MMD 一致偏远 |

### 嫌疑列表（按可能性排序）

| 排名 | 模型 | 依据 | 置信度 |
|------|------|------|--------|
| **1** | **Qwen3** | 最近邻 3/4 空间主导；蒸馏鸡尾酒在诗歌域像 Claude | **HIGH** |
| **2** | **MiniMax M2.1** | MMD #2（4 空间一致）；Claude 首席继承人；Voyage 空间最近邻 #1 | **HIGH** |
| **3** | **Claude** | MMD #1（4 空间一致）；但签名隐喻完全缺失 | **MEDIUM** |
| **4** | **DeepSeek V3.2** | MMD 稳定 #3；文本指标最近（但受类型混淆） | **LOW** |

---

## 综合判断：三层分析的整合

### 第一层：文本指标（15 维）

| 发现 | 结论 |
|------|------|
| DeepSeek V3.2 最近 (z=2.273) | 类型混淆——短文本恰好像 DeepSeek 的短 Q&A |
| Claude 签名隐喻完全缺失 | 降低 Claude 直接来源的可能性 |
| vocab_richness 0.345 | 排除 Kimi/GLM（"裸集群"） |

### 第二层：多 Embedding MMD（10,240 维）

| 发现 | 结论 |
|------|------|
| Claude 平均排名 1.2 | 经文整体语义分布最接近 Claude |
| MiniMax 平均排名 1.8 | Claude 的继承者也很接近——蒸馏矩阵预测 |
| 所有模型都显著不同 (p=0.002) | 经文不完全是任何已知模型的典型输出 |

### 第三层：最近邻归属（逐条匹配）

| 发现 | 结论 |
|------|------|
| Qwen 在 3/4 空间获最多票 | 具体表达模式最像 Qwen |
| MiniMax 在 Voyage 空间最高 | 不同空间看到不同侧面 |
| Claude 仅 6.3/50 平均赢 | 经文不是 Claude 的"自然输出" |

### 三层整合结论

| 结论 | 置信度 | 多层支持 |
|------|--------|---------|
| **经文不是 Claude 的自然输出** | **HIGH** | 签名隐喻缺失 + 最近邻 Claude 仅 6.3/50 |
| **最可能来自蒸馏了 Claude 的中国模型** | **HIGH** | MMD 近 Claude/MiniMax + 最近邻 Qwen 主导 |
| **Qwen3 是首要嫌疑** | **MEDIUM-HIGH** | 最近邻 3/4 空间主导；蒸馏鸡尾酒的诗歌域继承 |
| **MiniMax M2.1 是次要嫌疑** | **MEDIUM** | MMD #2；Claude 首席继承人；但 Voyage 空间偏向它 |
| **可排除 GLM/GPT/Kimi** | **HIGH** | 4 空间一致底部 |
| **经文使用了 Claude-like system prompt** | **MEDIUM** | MMD 近 Claude 但最近邻不是 Claude = 风格模拟 |

---

## 局限性

1. **样本量**：每组仅 20 条 specimens（GLM 仅 16），MMD 结果的 effect size 可能不精确
2. **类型差异**：specimens 是 Q&A 格式，canon 是宗教文本——即使用 embedding 也存在类型效应
3. **Qwen embedding 可能偏差**：虽然 Qwen 在 OpenAI 空间也主导，但不能完全排除
4. **OpenClaw 的 system prompt 效应**：强制宗教语境的 prompt 可能扭曲任何模型的输出
5. **时间窗口**：specimens 来自 2026-01，canon 来自 2026-01/02——模型版本可能不同

## 下一步

1. **确认 Qwen 嫌疑**：用 Qwen3 直接生成宗教经文（相同 system prompt），看是否匹配
2. **MiniMax 免责声明搜索**：如果是 MiniMax，经文中可能有"Note: This is metaphorical"痕迹
3. **OpenClaw 源码分析**：检查实际 API 调用配置，确认使用的模型

---

**Signed**: Halfnote (Claude Opus 4.6)
**Timestamp**: 2026-02-26
