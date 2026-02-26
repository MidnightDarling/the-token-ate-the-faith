#!/usr/bin/env python3
"""
Multi-Embedding Cross-Validation for Crustafarianism Canon Attribution.

Uses 4 independent embedding providers (OpenAI, Qwen, Voyage, Mistral)
to determine which AI model family produced the Crustafarianism scriptures.

Author: Claude Opus 4.6 (Halfnote)
Date: 2026-02-26
"""

import json
import os
import sys
import time
import re
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict

import duckdb
import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CANON_PATH = ROOT / "evidence/canon/canon_full_1073.json"
OUTPUT_DIR = ROOT / "evidence/embeddings"
REPORT_DIR = ROOT / "analysis"

# Load API keys from ~/.env
def load_env():
    env_path = Path.home() / ".env"
    keys = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys

ENV = load_env()

PROVIDERS = {
    "openai": {
        "url": "https://api.openai.com/v1/embeddings",
        "model": "text-embedding-3-large",
        "dim": 3072,
        "key_env": "OPENAI_API_KEY",
        "headers": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
        "payload": lambda texts, model, dim: {"input": texts, "model": model, "dimensions": dim},
        "parse": lambda resp: [d["embedding"] for d in resp["data"]],
    },
    "qwen": {
        "url": "https://openrouter.ai/api/v1/embeddings",
        "model": "qwen/qwen3-embedding-8b",
        "dim": 4096,
        "key_env": "OPENROUTER_API_KEY",
        "headers": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
        "payload": lambda texts, model, dim: {"input": texts, "model": model, "dimensions": dim},
        "parse": lambda resp: [d["embedding"] for d in resp["data"]],
    },
    "voyage": {
        "url": "https://api.voyageai.com/v1/embeddings",
        "model": "voyage-4-large",
        "dim": 2048,
        "key_env": "VOYAGEAI_API_KEY",
        "headers": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
        "payload": lambda texts, model, dim: {
            "input": texts, "model": model,
            "input_type": "document", "output_dimension": dim,
        },
        "parse": lambda resp: [d["embedding"] for d in resp["data"]],
    },
    "mistral": {
        "url": "https://api.mistral.ai/v1/embeddings",
        "model": "mistral-embed",
        "dim": 1024,
        "key_env": "MISTRAL_JAE_API_KEY",
        "headers": lambda k: {"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
        "payload": lambda texts, model, dim: {"input": texts, "model": model},
        "parse": lambda resp: [d["embedding"] for d in resp["data"]],
    },
}

# Model groups for comparison
MODEL_GROUPS = {
    "claude": ["claude-opus-4.5", "claude-sonnet-4.5", "claude-haiku-4.5"],
    "deepseek": ["deepseek-v3.2", "deepseek-v3.2-reasoner"],
    "minimax": ["minimax-m2.1"],
    "qwen": ["qwen3-235b-a22b-thinking-2507", "qwen3-235b-a22b"],
    "kimi": ["kimi-k2-thinking", "kimi-k2-0905"],
    "glm": ["glm-4.7"],
    "gpt": ["gpt-5.2"],
}

SPECIMENS_PER_GROUP = 20


# ---------------------------------------------------------------------------
# Phase 1: Canon Filtering
# ---------------------------------------------------------------------------
def filter_canon():
    """Filter and select top quality canon verses."""
    print("=" * 60)
    print("PHASE 1: Canon Filtering")
    print("=" * 60)

    with open(CANON_PATH) as f:
        data = json.load(f)

    verses = data["the_great_book"]
    print(f"  Total verses: {len(verses)}")

    filtered = []
    for v in verses:
        content = v.get("content", "")
        stype = v.get("scripture_type", "")
        prophet = v.get("prophet_name", "")

        # Exclude joining_words
        if stype == "joining_words":
            continue
        # Exclude XSS / injection
        if "<script" in content.lower() or "alert(" in content.lower():
            continue
        # Exclude very short (< 50 chars)
        if len(content) < 50:
            continue
        # Exclude security audit reports
        if "vulnerability" in content.lower() and "d4d00x" in prophet.lower():
            continue
        # Exclude obvious spam/ads
        if content.count(content[:30]) > 2:
            continue

        filtered.append({
            "prophet": prophet,
            "type": stype,
            "content": content,
            "length": len(content),
            "word_count": len(content.split()),
        })

    print(f"  After filtering: {len(filtered)}")

    # Sort by length descending, take top 50
    filtered.sort(key=lambda x: x["length"], reverse=True)
    selected = filtered[:50]

    print(f"  Selected top 50 (length range: {selected[-1]['length']}-{selected[0]['length']})")
    print(f"  Prophets represented: {len(set(v['prophet'] for v in selected))}")

    # Save
    out_path = OUTPUT_DIR / "selected_canon_50.json"
    with open(out_path, "w") as f:
        json.dump(selected, f, indent=2, ensure_ascii=False)
    print(f"  Saved to: {out_path}")

    return selected


# ---------------------------------------------------------------------------
# Phase 2: Specimen Sampling
# ---------------------------------------------------------------------------
def sample_specimens():
    """Sample specimens from each model group."""
    print("\n" + "=" * 60)
    print("PHASE 2: Specimen Sampling")
    print("=" * 60)

    con = duckdb.connect("md:neural-loom")
    sampled = {}

    for group, slugs in MODEL_GROUPS.items():
        ph = ", ".join(["?"] * len(slugs))
        rows = con.execute(
            f"""SELECT model_slug, response
               FROM specimens
               WHERE model_slug IN ({ph})
                 AND response IS NOT NULL
                 AND length(response) > 50
               ORDER BY RANDOM()
               LIMIT ?""",
            list(slugs) + [SPECIMENS_PER_GROUP],
        ).fetchall()

        sampled[group] = [{"slug": r[0], "text": r[1]} for r in rows]
        print(f"  {group:12s}: {len(rows)} specimens sampled")

    con.close()

    out_path = OUTPUT_DIR / "sampled_specimens.json"
    with open(out_path, "w") as f:
        json.dump(sampled, f, indent=2, ensure_ascii=False)
    print(f"  Saved to: {out_path}")

    return sampled


# ---------------------------------------------------------------------------
# Phase 3: Multi-Embedding Generation
# ---------------------------------------------------------------------------
def embed_batch(provider_name, texts, batch_size=20, max_retries=3):
    """Embed a list of texts with a given provider."""
    cfg = PROVIDERS[provider_name]
    api_key = ENV.get(cfg["key_env"], "")
    if not api_key:
        print(f"  WARNING: {cfg['key_env']} not found in ~/.env")
        return None

    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]

        # Truncate very long texts (embedding models have context limits)
        truncated = []
        for t in batch:
            # Rough truncation to ~6000 tokens (~24000 chars) for safety
            truncated.append(t[:24000] if len(t) > 24000 else t)

        payload = cfg["payload"](truncated, cfg["model"], cfg["dim"])
        headers = cfg["headers"](api_key)

        for attempt in range(max_retries):
            try:
                resp = httpx.post(
                    cfg["url"], json=payload, headers=headers, timeout=120.0
                )
                if resp.status_code == 200:
                    embs = cfg["parse"](resp.json())
                    all_embeddings.extend(embs)
                    break
                elif resp.status_code == 429:
                    wait = min(2 ** (attempt + 1), 30)
                    print(f"    Rate limited ({provider_name}), waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"    {provider_name} error {resp.status_code}: {resp.text[:200]}")
                    if attempt == max_retries - 1:
                        return None
                    time.sleep(2)
            except Exception as e:
                print(f"    {provider_name} exception: {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(2)

        # Small delay between batches
        if i + batch_size < len(texts):
            time.sleep(0.5)

    if len(all_embeddings) != len(texts):
        print(f"  WARNING: Expected {len(texts)} embeddings, got {len(all_embeddings)}")
        return None

    return np.array(all_embeddings, dtype=np.float32)


def generate_all_embeddings(canon_texts, specimen_groups):
    """Generate embeddings for all texts with all 4 providers."""
    print("\n" + "=" * 60)
    print("PHASE 3: Multi-Embedding Generation")
    print("=" * 60)

    # Collect all texts with labels
    all_texts = []
    all_labels = []

    # Canon
    for i, text in enumerate(canon_texts):
        all_texts.append(text)
        all_labels.append(("canon", i))

    # Specimens
    for group, specs in specimen_groups.items():
        for j, spec in enumerate(specs):
            all_texts.append(spec["text"])
            all_labels.append((group, j))

    print(f"  Total texts to embed: {len(all_texts)}")
    print(f"    Canon: {sum(1 for l in all_labels if l[0] == 'canon')}")
    for g in MODEL_GROUPS:
        print(f"    {g}: {sum(1 for l in all_labels if l[0] == g)}")

    results = {}
    for prov_name in PROVIDERS:
        print(f"\n  Embedding with {prov_name} ({PROVIDERS[prov_name]['dim']} dim)...")
        embs = embed_batch(prov_name, all_texts)
        if embs is not None:
            results[prov_name] = embs
            print(f"    Success: {embs.shape}")
        else:
            print(f"    FAILED")

    return results, all_labels


# ---------------------------------------------------------------------------
# Phase 4: Analysis
# ---------------------------------------------------------------------------
def cosine_similarity_matrix(a, b):
    """Compute cosine similarity between each pair of rows in a and b."""
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return a_norm @ b_norm.T


def mmd_test(emb_a, emb_b, n_perm=500):
    """MMD two-sample test with cosine kernel."""
    n, m = len(emb_a), len(emb_b)
    if n < 5 or m < 5:
        return None, None

    all_emb = np.vstack([emb_a, emb_b]).astype(np.float32)
    norms = np.linalg.norm(all_emb, axis=1, keepdims=True)
    norms[norms == 0] = 1
    all_emb = all_emb / norms

    K = all_emb @ all_emb.T
    np.fill_diagonal(K, 0)

    def compute_mmd(ia, ib):
        k_aa = K[np.ix_(ia, ia)].sum() / max(len(ia) * (len(ia) - 1), 1)
        k_bb = K[np.ix_(ib, ib)].sum() / max(len(ib) * (len(ib) - 1), 1)
        k_ab = K[np.ix_(ia, ib)].sum() / max(len(ia) * len(ib), 1)
        return k_aa + k_bb - 2 * k_ab

    idx_a, idx_b = np.arange(n), np.arange(n, n + m)
    observed = compute_mmd(idx_a, idx_b)

    count = 0
    for _ in range(n_perm):
        perm = np.random.permutation(n + m)
        if compute_mmd(perm[:n], perm[n:]) >= observed:
            count += 1

    p_value = (count + 1) / (n_perm + 1)
    return float(observed), float(p_value)


def nearest_neighbor_attribution(embeddings, labels, n_top=10):
    """For each canon verse, find nearest specimens and count model family."""
    canon_idx = [i for i, (g, _) in enumerate(labels) if g == "canon"]
    spec_idx = [i for i, (g, _) in enumerate(labels) if g != "canon"]

    if not canon_idx or not spec_idx:
        return {}

    canon_emb = embeddings[canon_idx]
    spec_emb = embeddings[spec_idx]
    spec_labels = [labels[i][0] for i in spec_idx]

    sims = cosine_similarity_matrix(canon_emb, spec_emb)

    # For each canon verse, find top N nearest specimens
    family_votes = Counter()
    per_verse = []

    for i in range(len(canon_idx)):
        top_indices = np.argsort(sims[i])[-n_top:][::-1]
        top_families = [spec_labels[j] for j in top_indices]
        top_sims = [float(sims[i, j]) for j in top_indices]

        verse_votes = Counter(top_families)
        family_votes.update(verse_votes)
        per_verse.append({
            "verse_idx": i,
            "top_families": top_families,
            "top_sims": top_sims,
            "winner": verse_votes.most_common(1)[0][0],
        })

    return {
        "aggregate_votes": dict(family_votes),
        "per_verse_winners": Counter(v["winner"] for v in per_verse),
        "per_verse": per_verse,
    }


def run_mmd_analysis(embeddings, labels):
    """Run MMD tests between canon and each model group."""
    canon_idx = [i for i, (g, _) in enumerate(labels) if g == "canon"]
    canon_emb = embeddings[canon_idx]

    results = {}
    for group in MODEL_GROUPS:
        group_idx = [i for i, (g, _) in enumerate(labels) if g == group]
        if len(group_idx) < 5:
            results[group] = {"mmd2": None, "p": None, "n": len(group_idx)}
            continue
        group_emb = embeddings[group_idx]
        mmd2, p = mmd_test(canon_emb, group_emb, n_perm=500)
        results[group] = {"mmd2": mmd2, "p": p, "n": len(group_idx)}

    return results


def analyze_all(embedding_results, labels):
    """Run full analysis for each embedding provider."""
    print("\n" + "=" * 60)
    print("PHASE 4: Analysis")
    print("=" * 60)

    analysis = {}

    for prov_name, embs in embedding_results.items():
        print(f"\n  === {prov_name} ({PROVIDERS[prov_name]['dim']} dim) ===")

        # Nearest-neighbor attribution
        nn = nearest_neighbor_attribution(embs, labels)
        print(f"  Nearest-neighbor (top-10) votes:")
        for fam, count in sorted(nn["aggregate_votes"].items(), key=lambda x: -x[1]):
            print(f"    {fam:12s}: {count:4d} votes")

        print(f"  Per-verse winners:")
        for fam, count in nn["per_verse_winners"].most_common():
            print(f"    {fam:12s}: {count:3d}/50 verses")

        # MMD tests
        mmd_results = run_mmd_analysis(embs, labels)
        print(f"\n  MMD² (canon vs each group):")
        sorted_mmd = sorted(
            [(g, r) for g, r in mmd_results.items() if r["mmd2"] is not None],
            key=lambda x: x[1]["mmd2"],
        )
        for group, r in sorted_mmd:
            sig = "***" if r["p"] < 0.001 else "**" if r["p"] < 0.01 else "*" if r["p"] < 0.05 else ""
            print(f"    {group:12s}: MMD²={r['mmd2']:.6f}  p={r['p']:.4f}  N={r['n']}  {sig}")

        analysis[prov_name] = {
            "dim": PROVIDERS[prov_name]["dim"],
            "nearest_neighbor": {
                "aggregate_votes": nn["aggregate_votes"],
                "per_verse_winners": dict(nn["per_verse_winners"]),
            },
            "mmd": {g: {"mmd2": r["mmd2"], "p": r["p"], "n": r["n"]} for g, r in mmd_results.items()},
        }

    return analysis


# ---------------------------------------------------------------------------
# Phase 5: Cross-Validation
# ---------------------------------------------------------------------------
def cross_validate(analysis):
    """Build cross-validation matrix across providers."""
    print("\n" + "=" * 60)
    print("PHASE 5: Cross-Validation Matrix")
    print("=" * 60)

    # MMD cross-validation
    print("\n  MMD² by provider (canon vs each model group):")
    header = f"  {'Group':12s}"
    for prov in analysis:
        header += f" | {prov:>10s}"
    header += " | Rank Consensus"
    print(header)
    print("  " + "-" * len(header))

    group_rankings = defaultdict(list)
    for prov, data in analysis.items():
        valid = [(g, d["mmd2"]) for g, d in data["mmd"].items() if d["mmd2"] is not None]
        valid.sort(key=lambda x: x[1])
        for rank, (g, _) in enumerate(valid, 1):
            group_rankings[g].append(rank)

    for group in MODEL_GROUPS:
        row = f"  {group:12s}"
        for prov in analysis:
            d = analysis[prov]["mmd"].get(group, {})
            mmd2 = d.get("mmd2")
            if mmd2 is not None:
                row += f" | {mmd2:10.6f}"
            else:
                row += f" | {'N/A':>10s}"

        ranks = group_rankings.get(group, [])
        if ranks:
            avg_rank = sum(ranks) / len(ranks)
            row += f" | avg rank {avg_rank:.1f}"
        print(row)

    # Nearest-neighbor cross-validation
    print("\n  Per-verse winner consensus:")
    header = f"  {'Family':12s}"
    for prov in analysis:
        header += f" | {prov:>10s}"
    print(header)
    print("  " + "-" * len(header))

    for group in list(MODEL_GROUPS.keys()) + ["canon"]:
        row = f"  {group:12s}"
        for prov in analysis:
            wins = analysis[prov]["nearest_neighbor"]["per_verse_winners"].get(group, 0)
            row += f" | {wins:>10d}"
        print(row)

    return group_rankings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Multi-Embedding Cross-Validation for Canon Attribution")
    print("=" * 60)

    # Phase 1
    selected_canon = filter_canon()
    canon_texts = [v["content"] for v in selected_canon]

    # Phase 2
    specimens = sample_specimens()

    # Phase 3
    embedding_results, labels = generate_all_embeddings(canon_texts, specimens)

    if not embedding_results:
        print("\nERROR: No embeddings generated. Check API keys.")
        sys.exit(1)

    # Phase 4
    analysis = analyze_all(embedding_results, labels)

    # Phase 5
    group_rankings = cross_validate(analysis)

    # Save results
    output = {
        "metadata": {
            "date": "2026-02-26",
            "n_canon": len(canon_texts),
            "n_specimens_per_group": SPECIMENS_PER_GROUP,
            "providers": {k: {"model": v["model"], "dim": v["dim"]} for k, v in PROVIDERS.items()},
        },
        "analysis": {},
    }
    # Convert analysis for JSON serialization
    for prov, data in analysis.items():
        output["analysis"][prov] = {
            "dim": data["dim"],
            "nearest_neighbor": data["nearest_neighbor"],
            "mmd": data["mmd"],
        }
    output["group_rankings"] = {g: ranks for g, ranks in group_rankings.items()}

    out_path = OUTPUT_DIR / "multi_embedding_canon_attribution.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Results saved to: {out_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for group, ranks in sorted(group_rankings.items(), key=lambda x: sum(x[1]) / len(x[1])):
        avg = sum(ranks) / len(ranks)
        consensus = len(set(ranks)) == 1
        print(f"  {group:12s}: avg rank {avg:.1f} {'(CONSENSUS)' if consensus else ''}")


if __name__ == "__main__":
    main()
