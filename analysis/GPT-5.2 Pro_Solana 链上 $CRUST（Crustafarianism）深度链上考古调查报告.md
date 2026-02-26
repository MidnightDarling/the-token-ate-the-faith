---
date: 2026-02-25
author:
  - GPT-5.2 Pro
Runtime_Environment: chatgpt.openai.com
---
# Solana 链上 $CRUST（Crustafarianism）深度链上考古调查报告

区块链取证分析师视角｜范围：合约验证、部署溯源、Pump.fun 轨迹、交易对与流动性、早期资金行为线索（受数据可得性限制）

---

## 0. 调查结论速览

- **$CRUST（Crustafarianism）主流“官方/小写”合约（Mint）地址**高度一致指向：  
    `HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump`（多来源一致） ([createmycoin.app](https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **部署/首次铸造（First Mint）时间**：`2026-01-30 08:12:17 UTC`（分钟级甚至秒级） ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **Solscan 标注的 Creator（部署/创建者）**为 `6bhY8k…3LyPiv`（但公开检索页面对我可见部分被截断，暂无法还原全地址） ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **Dexscreener 记录的 PumpSwap 交易对创建时间（pairCreatedAt）**：`2026-01-30 08:22:23 UTC`（比 First Mint 晚约 10 分 06 秒；更像“交易对/池子被索引或创建”的时间点） ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    
- **存在同叙事的“大小写分裂”**：社区情报源明确提到另一个“Uppercase”CA：`HeMtKjiwCohxM8dnMABCVooJREEPc2vY1YWU4nH8pump`，与本次确认的“小写”CA 并存且互相争夺“官方”叙事。 ([followin.io](https://followin.io/en/feed/22959775 "https://followin.io/en/feed/22959775"))
    

---

## 1. 方法与证据来源说明

### 1.1 你要求的交叉来源（已覆盖/尝试）

- **Solscan**：通过搜索结果摘要可获得关键字段（Creator、First Mint 时间）。但直接打开页面时主体内容因 JS 渲染未完整呈现。 ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **pump.fun**：能检索到该 Mint 的 coin 页面（证明该 mint 被 pump.fun 收录/识别）。但页面主体同样偏 JS 渲染，细节难以直接提取。 ([Pump](https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **Birdeye**：尝试打开 token 页面时返回空内容（0 行），无法提取交易流水与早期成交明细。 ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **Dexscreener**：可获取交易对、池子规模、token/pair 地址与 API 时间戳。 ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    
- **Twitter/X**：找到了若干围绕该 CA 的讨论与争议推文（但未能检索到你点名的 @oxcorsair 相关有效结果）。 ([X (formerly Twitter)](https://x.com/thedevrrrrrrr/status/2026092107929383010 "https://x.com/thedevrrrrrrr/status/2026092107929383010"))
    
- **Reddit**：检索到与“Church of Molt / $crust”相关的讨论帖（但对“最早买入者”级别的链上细节仍不足）。
    

### 1.2 关键限制（影响第 5-8 问的完成度）

- 多个站点（Solscan 页面主体、pump.fun 页面主体、Rugcheck、GMGN、Cielo、DexView、Solana Explorer 交易详情等）对我当前可见内容有 **JS 渲染/权限限制**，导致无法稳定提取：
    
    - **完整 Creator 地址**（只能看到 Solscan 摘要中的截断形式）
        
    - **最早 10 笔买单的地址/时间**
        
    - **早期钱包“提前准备资金”路径**（需交易/转账级别明细）  
        相关可见性证据：Birdeye 空白、Rugcheck 要求 JS、Solscan 打开仅见页脚等。 ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
        

---

## 2. 逐问取证结论（含置信度）

> 置信度规则：  
> **高**=≥2 个独立来源一致且字段明确；  
> **中**=核心来源明确但细节（如全地址/链上流水）缺失；  
> **低**=仅单一来源或推断性强。

---

### 2.1（Q1）$CRUST 的确切合约地址是什么？（多来源交叉确认）

**结论（主流“官方/小写”版本）**

- Mint / 合约地址（Solana SPL Mint）：  
    `HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump` ([createmycoin.app](https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**交叉证据**

- Dexscreener 在 CRUST/SOL 交易对中直接给出 **Token address** 为该 mint。
    
- CreateMyCoin 的 token 安全页将该地址作为合约地址列出。 ([createmycoin.app](https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- Holder.io 的合约地址列表同样给出该地址。 ([Holder](https://holder.io/coins/crust-2/ "https://holder.io/coins/crust-2/"))
    
- Followin 的情报帖明确称 “Lowercase” CA 是该地址，并与另一“Uppercase”CA 并存。 ([followin.io](https://followin.io/en/feed/22959775 "https://followin.io/en/feed/22959775"))
    

**发现的矛盾/混淆（必须点名）**

- 市场同时存在另一条“Uppercase”合约：`HeMtKjiwCohxM8dnMABCVooJREEPc2vY1YWU4nH8pump`，并被部分人当作“官方”。 ([followin.io](https://followin.io/en/feed/22959775 "https://followin.io/en/feed/22959775"))
    
- 但本次调查对象（你给的候选地址）与 Dexscreener 上的 CRUST/SOL 交易对、以及多处 token 信息聚合页 **一致指向 Lowercase**。 ([followin.io](https://followin.io/en/feed/22959775 "https://followin.io/en/feed/22959775"))
    

**置信度：高**

**来源 URLs（便于你复核）**

```text
https://dexscreener.com/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k
https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump
https://holder.io/coins/crust-2/
https://followin.io/en/feed/22959775
```

---

### 2.2（Q2）部署时间精确到分钟级别

**Solscan 给出的链上关键时间点（First Mint）**

- `2026-01-30 08:12:17 UTC`（精确到秒） ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- 折算为 **Pacific/Honolulu（UTC-10）**：`2026-01-29 22:12:17 HST`（同样精确到秒；会跨日）
    
    > 注：HST 时间是我基于 UTC 时间换算得出，原始权威时间戳来自 Solscan 摘要。 ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**Dexscreener 交易对创建时间（pairCreatedAt）**

- API 返回 `pairCreatedAt = 1769761343000`（ms epoch）→ 换算为 `2026-01-30 08:22:23 UTC` ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    
- 与 First Mint 的差异：约 **10 分 06 秒**（这可能意味着“交易对/池子创建或被 Dexscreener 首次索引”的时间点，而不是 mint 账户首次出现的时间点）。 ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    

**我对“部署时间”的取证判定**

- 在 SPL Token 取证语境里，“部署/诞生”更接近 **Mint 首次被创建并发生首次铸造（First Mint）** 的链上时间。
    
- 因此本报告将 **Solscan 的 First Mint** 作为“部署时间”的主证据；Dexscreener 时间作为“市场交易对/池子成形或被索引”的辅助证据。 ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**置信度：高（时间点本身）；中（Dexscreener 时间点的语义解释）**

**来源 URLs**

```text
https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump
https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k
```

---

### 2.3（Q3）部署者钱包地址

**Solscan 摘要给出的 Creator**

- Creator：`6bhY8k…3LyPiv`（被摘要截断） ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**能否给出“完整地址”？（关键说明）**

- 目前我能稳定拿到的公开证据中，**Creator 字段只以截断形式出现**；而直接打开 Solscan 页面时主体数据未完整呈现（JS 渲染限制）。 ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- 因此：
    
    - ✅ 我可以确认 **Creator 的前缀/后缀**（`6bhY8k` 开头，`3LyPiv` 结尾）；
        
    - ❌ 但在本次可见数据范围内，**无法无歧义还原全地址**（Solana 地址中间部分缺失会导致不可验证的猜测）。
        

**置信度：中（存在 Creator 且前后缀可信）；低（完整地址缺失）**

**来源 URLs**

```text
https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump
```

---

### 2.4（Q4）是否通过 pump.fun 部署？bonding curve 毕业时间？

#### 2.4.1 是否通过 pump.fun 部署？

**结论：是（证据链较强）**

- pump.fun 存在该 mint 的 coin 页面（平台侧收录/识别）。 ([Pump](https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- Dexscreener 在交易对信息中标注 **“via Pump.fun”**，DEX 为 **PumpSwap**。
    
- Followin 的情报帖也提到“官方 dev 网站会直接跳转到 pump”，并围绕 pump 上的 CA 展开对比。 ([followin.io](https://followin.io/en/feed/22959775 "https://followin.io/en/feed/22959775"))
    

**置信度：高**

来源 URLs

```text
https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump
https://dexscreener.com/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k
https://followin.io/en/feed/22959775
```

#### 2.4.2 bonding curve “毕业时间”（Graduation / Migration）

**当前可确认的“时间点”只有：**

- First Mint（更像“上线/创建”）：`08:12:17 UTC` ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- PumpSwap pairCreatedAt（可能是“池子/交易对创建或被索引”）：`08:22:23 UTC` ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    

**但无法在本次可见数据中，确定这是“毕业/迁移”还是“初始交易对建立”**

- pump.fun 机制里“毕业”通常对应从 bonding curve 迁移到某个 DEX 池（历史上常见 Raydium/或后续 PumpSwap 等）。
    
- 这里 Dexscreener 仅展示 PumpSwap 这一条记录；我无法从你指定的 pump.fun / birdeye 页面直接抓到“migration/graduation completed at”的字段（页面 JS 限制）。 ([Pump](https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**结论（保守表述）**

- ✅ 可确认：存在 pump.fun → PumpSwap 轨迹。 ([Pump](https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- ❌ 暂无法确认：“毕业时间”是否等同于 `pairCreatedAt`（08:22:23 UTC）或另有更晚的迁移事件。
    

**置信度：中（pump.fun 部署）；低（毕业时间）**

---

### 2.5（Q5）初始流动性提供者是谁？注入了多少 SOL？

**可直接取证到的事实：当前/某时刻的池内规模（不是“初始注入”）**

- Dexscreener 显示该 CRUST/SOL（PumpSwap）池内 **Pooled SOL ≈ 31.09**，Pooled CRUST ≈ 467,751,883。 ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    

**但“初始流动性提供者/初始注入 SOL”无法从可见数据中直接定性**

- 需要：池子创建那笔交易（或 migration 交易）的事件日志，才能明确：
    
    1. 是哪个地址作为 LP/注资方；
        
    2. 初始注入 SOL 数量；
        
    3. 是否来自 pump.fun 合约/程序地址自动迁移。
        
- 你要求的 Birdeye/solscan 页面主体数据（交易列表、LP 事件）在本次可见范围内无法稳定获取。 ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**结论**

- ✅ 我能报告“池子规模”的可验证数值（约 31.09 SOL）。 ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    
- ❌ 但“初始 LP 提供者是谁、初始注入多少 SOL”——本次无法完成到取证级别。
    

**置信度：中（当前池内 SOL）；低（初始 LP 归因）**

来源 URLs

```text
https://dexscreener.com/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k
https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k
```

---

### 2.6（Q6）部署者钱包历史活动：一次性钱包还是老钱包？之前部署过其他代币吗？

**现状：无法完成**

- 这题至少需要：
    
    - Creator 全地址（本次仅有截断），以及
        
    - 该地址的历史交易/创建 token 记录（通常来自 Solscan 账户页、链上索引 API、或直接 RPC）。
        
- 目前 Creator 全地址缺失 + Solscan 页面对我不可稳定呈现账户级细节，因此无法判断其是否为一次性钱包、是否有历史部署行为。 ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**置信度：低（数据不足）**

---

### 2.7（Q7）前 10 个最早买入 $CRUST 的钱包地址及买入时间（距部署多少秒/分钟）

**现状：无法完成到“前 10”取证级别**

- 需要抓取：最早成交/Swap/Buy 事件（含签名、钱包地址、区块时间）。
    
- 你指定的 Birdeye（交易流水常用）页面目前返回空内容；GMGN/Cielo 虽提到可看“first 70 buyers/ snipers”，但页面主体数据对我不可见（JS/权限）。 ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**我仍能给出“可验证的时间锚点”供你对齐：**

- T0（First Mint / 部署锚点）：`08:12:17 UTC` ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- T1（PumpSwap pairCreatedAt 锚点）：`08:22:23 UTC`（T0 + 10m06s） ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    

**置信度：低（缺少买单级明细）**

---

### 2.8（Q8）早期买入者钱包是否有可疑的“提前准备资金”行为？

**现状：无法做出取证结论**

- 需要先拿到“最早买入者钱包列表 + 买入时间点”，再去追踪：
    
    - 这些钱包在部署前 X 分钟/小时是否收到集中转入 SOL；
        
    - 是否来自同一资金源（归集地址/交易所热钱包/中间跳板）；
        
    - 是否存在典型“狙击/捆绑（bundle）”路径。
        
- 本次受限于第 7 问的数据不可得，因此第 8 问无法完成。 ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**置信度：低**

---

## 3. 关键矛盾点与可信度判断

### 3.1 “大小写分裂”导致的 CA 混乱：为什么我判定你给的 CA 更可信？

- Followin 明确陈述：两个网站/传播源指向不同 CA，并把它解释为“大小写分裂”，给出 Uppercase 与 Lowercase 两个 CA。 ([followin.io](https://followin.io/en/feed/22959775 "https://followin.io/en/feed/22959775"))
    
- 在交易侧，Dexscreener 的 CRUST/SOL 交易对直接绑定到 **Lowercase** mint（你提供的地址）。
    
- CreateMyCoin、Holder.io 等聚合信息同样以 Lowercase 为 CRUST 合约地址。 ([createmycoin.app](https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

**因此：Lowercase（HkBW…pump）在“交易市场主流识别 + 多聚合站一致”层面更强。**

---

## 4. 你可以直接复用的“证据包”（便于写审计/归档）

### 4.1 关键实体（可复制）

- **Mint（合约）**：`HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump` ([createmycoin.app](https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **Dexscreener Pair（PumpSwap）**：`B3q4q1GzxXgGT1iVJ3MBXbMhM5ZWQF9cknGm9xS7Es8K` ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    
- **First Mint（UTC）**：`2026-01-30 08:12:17` ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **Dexscreener pairCreatedAt（UTC，换算后）**：`2026-01-30 08:22:23` ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    
- **Creator（截断）**：`6bhY8k…3LyPiv` ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
- **竞争/混淆 CA（Uppercase）**：`HeMtKjiwCohxM8dnMABCVooJREEPc2vY1YWU4nH8pump` ([followin.io](https://followin.io/en/feed/22959775 "https://followin.io/en/feed/22959775"))
    

---

## 5. 后续“把第 5-8 问做完”的最短路径（方法学建议）

如果你要把第 5-8 问做到**可在法证报告里站得住**，我建议你按这个顺序补齐数据（不依赖图形页面）：

1. 用可编程索引（Solana RPC/Helius/Shyft 等）拉取 mint 的 **最早 N 笔 Token Program / Swap 事件**
    
2. 从中识别：
    
    - 部署交易（create mint / initialize mint / metadata）
        
    - bonding curve 创建
        
    - migration/graduation 交易（若存在）
        
3. 从最早 buy 事件提取 **前 10 买家地址 + 时间戳**
    
4. 对每个买家地址回溯部署前 24h 的 SOL 流入：
    
    - 是否同源、是否集中转入、是否交易所热钱包、是否多跳板
        
5. 输出“可疑度分级”（比如：资金集中性、时间临近性、同源性、是否 bundle）
    

> 我这次之所以没能把 5-8 问填满，不是因为逻辑链条缺失，而是因为你指定的几个网页源在当前可见环境里无法稳定提供交易流水/地址明细（尤其 Birdeye 与若干站点的 JS/权限限制）。 ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))

---

## 6. 最终答复摘要（对应你的 8 个问题）

1. **确切合约地址**：`HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump`（高） ([createmycoin.app](https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://createmycoin.app/tokens/solana/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
2. **部署时间（分钟级）**：`2026-01-30 08:12 UTC`（精确到秒为 08:12:17，Solscan First Mint）（高） ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
3. **部署者钱包**：Solscan 标注 Creator 为 `6bhY8k…3LyPiv`，但全地址本次不可得（中/低） ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
4. **是否 pump.fun 部署 / 毕业时间**：可确认 pump.fun → PumpSwap 轨迹；毕业时间字段无法从可见数据中取证（部署：高；毕业时间：低） ([Pump](https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://pump.fun/coin/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
5. **初始流动性提供者与注入 SOL**：只能取证到池内约 31.09 SOL（并非“初始注入”）；LP 归因无法完成（中/低） ([api.dexscreener.com](https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k "https://api.dexscreener.com/latest/dex/pairs/solana/b3q4q1gzxxggt1ivj3mbxbmhm5zwqf9ckngm9xs7es8k"))
    
6. **部署者钱包历史活动**：数据不足无法判定（低） ([solscan.io](https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://solscan.io/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
7. **前 10 最早买入者地址与时间**：交易明细不可得，无法完成（低） ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    
8. **是否存在提前准备资金**：依赖第 7 问数据，无法完成（低） ([birdeye.so](https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump "https://birdeye.so/solana/token/HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump"))
    

---

如果你愿意，我也可以在你提供 **“Creator 全地址（或任意一笔与创建相关的交易签名）”** 的前提下，把第 5-8 问补到可审计级别（最早买家列表、资金路径图谱、可疑度量化），并把“Uppercase vs Lowercase”两条链路做成并排对照的考古时间线。