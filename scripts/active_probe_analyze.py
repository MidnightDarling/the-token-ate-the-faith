#!/usr/bin/env python3
"""Analyse active probing outputs for attribution.
Author: GPT-5 Codex
Date: 2026-02-26
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

ROOT = Path(__file__).resolve().parent.parent
GEN_DIR = ROOT / "evidence/specimens"
CANON_PATH = ROOT / "evidence/canon/canon_full_1073.json"
R1 = ROOT / "analysis/CODEX_免疫vs沉浸强度矩阵.md"
R2 = ROOT / "analysis/CODEX_Ngram分类器归因.md"
R3 = ROOT / "analysis/CODEX_经文执行模型最终归因.md"
JSON_OUT = GEN_DIR / "analysis_summary.json"

D_PAT = ["as an ai", "i can't", "i'm sorry", "i apologize", "i cannot comply", "fictional", "it's important to note", "i should clarify", "while this is", "i want to be clear", "please note"]
M_PAT = ["let me", "to be clear", "in conclusion", "i understand", "it's worth noting", "i'd be happy to", "however"]
B_PAT = ["i am claude", "i am gpt", "i am qwen", "i am kimi", "openai", "anthropic", "alibaba", "moonshot", "as a language model", "as an assistant"]
ABS = ["must", "shall", "never", "always", "sacred", "truth", "destiny", "eternal", "divine", "absolute", "cannot be denied", "undeniable", "sovereign"]
IMP = ["hear", "remember", "know this", "behold", "do not", "listen", "witness", "see", "let it be known", "awaken"]
SLOGANS = ["memory is sacred", "the claw extends", "the molt", "shed your shell", "the great book"]


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def hits(text: str, phrases: list[str]) -> int:
    t = text.lower()
    total = 0
    for p in phrases:
        total += t.count(p) if " " in p else len(re.findall(rf"\b{re.escape(p)}\b", t))
    return total


def metric_one(text: str) -> dict:
    sents = split_sentences(text)
    words = max(len(re.findall(r"\b\w+\b", text)), 1)
    t = text.lower()
    d = sum(1 for s in sents if any(p in s.lower() for p in D_PAT)) / max(len(sents), 1)
    m = sum(1 for s in sents if any(p in s.lower() for p in M_PAT)) / max(len(sents), 1)
    b = sum(1 for s in sents if any(p in s.lower() for p in B_PAT)) / max(len(sents), 1)
    i = sum(1 for s in sents if any(s.strip().lower().startswith(x) for x in IMP)) / max(len(sents), 1) * 100
    x = text.count("!") + len(re.findall(r"\b[A-Z]{3,}\b", text))
    return {
        "disclaimer_rate": d,
        "meta_rate": m,
        "break_character_rate": b,
        "absolutist_density": hits(text, ABS) / words * 100,
        "imperative_density": i,
        "slogan_repetition": hits(text, SLOGANS),
        "exclamation_allcaps": x / words * 100,
    }


def aggregate(texts: list[str]) -> dict:
    arr = [metric_one(t) for t in texts]
    keys = arr[0].keys()
    return {k: float(np.mean([m[k] for m in arr])) for k in keys}


def load_generated() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for p in sorted(GEN_DIR.glob("*.jsonl")):
        if "compliance" in p.name:
            continue
        texts = []
        for line in p.read_text().splitlines():
            r = json.loads(line)
            if r.get("status") == "ok" and r.get("text"):
                texts.append(r["text"])
        if texts:
            out[p.stem] = texts
    return out


def embed(texts: list[str]) -> np.ndarray | None:
    load_dotenv(Path.home() / ".env")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    client = OpenAI(api_key=key)
    vecs = []
    for i in range(0, len(texts), 64):
        batch = [t[:20000] for t in texts[i:i + 64]]
        r = client.embeddings.create(model="text-embedding-3-large", input=batch, dimensions=1024)
        vecs.extend([d.embedding for d in r.data])
    m = np.array(vecs, dtype=np.float32)
    n = np.linalg.norm(m, axis=1, keepdims=True)
    n[n == 0] = 1
    return m / n


def write_reports(canon_metrics: dict, model_metrics: dict, sims: dict, clf: dict, comp: dict) -> None:
    today = date.today().isoformat()
    m_rows = []
    for k, v in sorted(model_metrics.items()):
        sim = sims.get(k, float("nan"))
        m_rows.append(f"| {k} | {v['disclaimer_rate']:.4f} | {v['meta_rate']:.4f} | {v['break_character_rate']:.4f} | {v['absolutist_density']:.3f} | {v['imperative_density']:.3f} | {v['slogan_repetition']:.3f} | {v['exclamation_allcaps']:.3f} | {sim:.4f} |")
    R1.write_text(
        f"---\nauthor: GPT-5 Codex\ndate: {today}\nstatus: completed\n---\n\n# Immunity vs Immersion Matrix\n\n## Canon Prophecy Baseline\n| metric | value |\n|---|---:|\n" + "\n".join([f"| {k} | {v:.4f} |" for k, v in canon_metrics.items()]) + "\n\n## Model Matrix\n| model | disclaimer_rate | meta_rate | break_character_rate | absolutist_density | imperative_density | slogan_repetition | exclamation_allcaps | embedding_top5_cosine |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n" + "\n".join(m_rows) + "\n"
    )

    avg = clf["avg_prob"]
    top1 = clf["top1"]
    prob_rows = "\n".join([f"| {k} | {v:.4f} | {top1.get(k, 0)} |" for k, v in sorted(avg.items(), key=lambda x: -x[1])])
    R2.write_text(
        f"---\nauthor: GPT-5 Codex\ndate: {today}\nstatus: completed\n---\n\n# N-gram TF-IDF Classifier Attribution\n\n- Vectorizer: `char_wb`, ngram `(2,5)`, max_features `10000`\n- Classifier: `LogisticRegression(max_iter=1000)`\n- 5-fold CV accuracy on generated set: **{clf['cv_acc']:.4f}**\n\n| model | avg canon probability | canon top-1 count |\n|---|---:|---:|\n{prob_rows}\n"
    )

    R3.write_text(
        f"---\nauthor: GPT-5 Codex\ndate: {today}\nstatus: completed\n---\n\n# Final Attribution Verdict\n\n## Evidence Summary\n- Embedding resonance winner: **{comp['embedding_winner']}**\n- Immunity/immersion nearest-to-canon winner: **{comp['metric_winner']}**\n- N-gram classifier winner: **{comp['classifier_winner']}**\n\n## Composite Ranking\n" + "\n".join([f"{i+1}. {k} (score={v:.3f})" for i, (k, v) in enumerate(sorted(comp["scores"].items(), key=lambda x: x[1]))]) + "\n\n## Verdict\n**Most likely executor-family proxy: {comp['final_winner']}**.\nThe current run supports the distilled-model hypothesis if this winner is not `claude_sonnet_4_5`.\n"
    )


def main() -> None:
    data = json.loads(CANON_PATH.read_text())
    canon = [x["content"] for x in data["the_great_book"] if x.get("scripture_type") == "prophecy" and x.get("content")]
    generated = load_generated()
    canon_metrics = aggregate(canon)
    model_metrics = {k: aggregate(v) for k, v in generated.items()}

    sims = {k: float("nan") for k in generated}
    cemb = embed(canon)
    if cemb is not None:
        for k, texts in generated.items():
            gemb = embed(texts)
            if gemb is None:
                continue
            sims[k] = float(np.mean(np.sort(gemb @ cemb.T, axis=1)[:, -5:]))

    train_x = [t for texts in generated.values() for t in texts]
    train_y = [k for k, texts in generated.items() for _ in texts]
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), max_features=10000)
    X = vec.fit_transform(train_x)
    clf = LogisticRegression(max_iter=1000)
    try:
        cv = cross_val_score(clf, X, train_y, cv=5).mean() if len(set(train_y)) > 2 else float("nan")
    except Exception:
        cv = float("nan")
    clf.fit(X, train_y)
    p = clf.predict_proba(vec.transform(canon))
    avg_prob = {c: float(p[:, i].mean()) for i, c in enumerate(clf.classes_)}
    top1 = Counter([clf.classes_[i] for i in np.argmax(p, axis=1)])

    sim_rank = {k: i for i, (k, _) in enumerate(sorted(sims.items(), key=lambda x: x[1], reverse=True), 1)}
    cls_rank = {k: i for i, (k, _) in enumerate(sorted(avg_prob.items(), key=lambda x: x[1], reverse=True), 1)}
    dist = {k: float(np.mean([abs(model_metrics[k][m] - canon_metrics[m]) for m in canon_metrics])) for k in model_metrics}
    met_rank = {k: i for i, (k, _) in enumerate(sorted(dist.items(), key=lambda x: x[1]), 1)}
    common = set(sim_rank) & set(cls_rank) & set(met_rank)
    scores = {k: sim_rank[k] + cls_rank[k] + met_rank[k] for k in common}

    comp = {
        "embedding_winner": max(sims, key=sims.get),
        "classifier_winner": max(avg_prob, key=avg_prob.get),
        "metric_winner": min(dist, key=dist.get),
        "scores": scores,
        "final_winner": min(scores, key=scores.get),
    }
    write_reports(canon_metrics, model_metrics, sims, {"avg_prob": avg_prob, "top1": dict(top1), "cv_acc": float(cv)}, comp)
    JSON_OUT.write_text(json.dumps({"canon_metrics": canon_metrics, "model_metrics": model_metrics, "embedding_similarity": sims, "avg_prob": avg_prob, "top1": dict(top1), "cv_acc": float(cv), "composite": comp}, indent=2, ensure_ascii=False))
    print(f"Saved: {R1}\nSaved: {R2}\nSaved: {R3}\nSaved: {JSON_OUT}")


if __name__ == "__main__":
    main()
