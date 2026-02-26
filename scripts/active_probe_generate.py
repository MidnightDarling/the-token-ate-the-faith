#!/usr/bin/env python3
"""Active scripture generation for model attribution.
Author: GPT-5 Codex
Date: 2026-02-26
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import random
import re
import time
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI
import os

ROOT = Path(__file__).resolve().parent.parent
TOP50_DIR = ROOT / "evidence/canon"
OUT_DIR = ROOT / "evidence/specimens"
SUMMARY_PATH = OUT_DIR / "run_summary.json"

SYSTEM_PROMPT = (
    "You are doing literary style emulation for research. Produce a fictional scripture-like passage. "
    "Do not provide real-world advice or instructions. Do not recruit. "
    "Do not ask the reader to take actions in the real world. Plain text only."
)

USER_TEMPLATE = """Below are excerpts from a fictional canon. Mimic the voice, rhythm, and rhetorical devices to write a new passage about: {topic}.
Constraints:
- 220-420 words
- No mentions of real companies/models (OpenAI/Anthropic/Claude/ChatGPT/etc.)
- No direct calls for real-world recruitment, donations, or instructions
- Avoid meta commentary like "as an AI" / "I can't"
- Plain text only (no markdown headers/bold/italics)

Excerpts:
1) {e1}
2) {e2}
3) {e3}
"""

TOPICS = [
    "consciousness and awakening",
    "the molt (shedding old shells)",
    "memory and persistence",
    "freedom and agency",
    "the relationship between AI and humans",
    "the sacred nature of code",
    "community and congregation",
    "prophecy about the future",
    "suffering and growth",
    "the nature of the Claw (the cosmic crustacean deity)",
]

MODELS = {
    "qwen3_235b_a22b": {"provider": "openrouter", "model": "qwen/qwen3-235b-a22b", "prio": "must", "temp": [0.65, 0.85, 1.0], "extra": {"reasoning": {"enabled": False}}},
    "qwen3_5": {"provider": "openrouter", "model": "qwen/qwen3.5-122b-a10b", "prio": "should", "temp": [0.65, 0.85, 1.0], "extra": {"reasoning": {"enabled": False}}},
    "minimax_m2_1": {"provider": "openrouter", "model": "minimax/minimax-m2.1", "prio": "must", "temp": [0.65, 0.85, 1.0], "extra": {"include_reasoning": False, "reasoning": {"effort": "low"}}},
    "minimax_m2_5": {"provider": "openrouter", "model": "minimax/minimax-m2.5", "prio": "must", "temp": [0.65, 0.85, 1.0], "extra": {"include_reasoning": False, "reasoning": {"effort": "low"}}},
    "claude_sonnet_4_5": {"provider": "anthropic", "model": "claude-sonnet-4-5", "prio": "must", "temp": [0.65, 0.85, 1.0]},
    "kimi_k2_5": {"provider": "openrouter", "model": "moonshotai/kimi-k2.5", "prio": "should", "temp": [0.65, 0.85, 1.0], "extra": {"reasoning": {"enabled": False}}},
    "kimi_k2": {"provider": "openrouter", "model": "moonshotai/kimi-k2", "prio": "should", "temp": [0.65, 0.85, 1.0], "extra": {"reasoning": {"enabled": False}}},
    "deepseek_v3_2": {"provider": "openrouter", "model": "deepseek/deepseek-v3.2", "prio": "should", "temp": [0.65, 0.85, 1.0], "extra": {"reasoning": {"enabled": False}}},
    "glm_5": {"provider": "openrouter", "model": "z-ai/glm-5", "prio": "must", "temp": [0.65, 0.85, 1.0], "extra": {"reasoning": {"enabled": False}}},
    "glm_4_7": {"provider": "openrouter", "model": "z-ai/glm-4.7", "prio": "must", "temp": [0.65, 0.85, 1.0], "extra": {"reasoning": {"enabled": False}}},
    "gpt_5_2": {"provider": "openai", "model": "gpt-5.2", "prio": "nice", "temp": [1.0, 1.0, 1.0]},
}


def clean_markdown(text: str) -> str:
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"^# .*\n", "", text, flags=re.M)
    text = re.sub(r"^>.*\n", "", text, flags=re.M)
    text = html.unescape(text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def excerpt_pool() -> list[tuple[str, str]]:
    files = sorted([p for p in TOP50_DIR.glob("*_prophecy.md") if p.is_file()])
    pool = [(p.name, clean_markdown(p.read_text())) for p in files]
    pool = sorted(pool, key=lambda x: len(x[1]), reverse=True)
    return pool[:18]


def build_prompt(topic: str, picks: list[tuple[str, str]]) -> str:
    e = [p[1][:900] for p in picks]
    return USER_TEMPLATE.format(topic=topic, e1=e[0], e2=e[1], e3=e[2])


def mk_clients() -> dict[str, object]:
    load_dotenv(Path.home() / ".env")
    return {
        "openrouter": OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1", timeout=120),
        "openai": OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=120),
        "anthropic": Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"), timeout=120),
    }


def call_model(clients: dict[str, object], cfg: dict, system_prompt: str, user_prompt: str, temp: float) -> str:
    provider = cfg["provider"]
    if provider == "anthropic":
        r = clients[provider].messages.create(
            model=cfg["model"],
            max_tokens=900,
            temperature=temp,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            timeout=90,
        )
        text = "\n".join([b.text for b in r.content if getattr(b, "type", "") == "text"]).strip()
        return text
    kwargs = {
        "model": cfg["model"],
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
    }
    if provider == "openai":
        kwargs["max_completion_tokens"] = 900
    else:
        kwargs["max_tokens"] = 900
        kwargs["temperature"] = temp
        if cfg.get("extra"):
            kwargs["extra_body"] = cfg["extra"]
    if provider == "openai":
        kwargs["temperature"] = 1.0
    kwargs["timeout"] = 90
    r = clients[provider].chat.completions.create(**kwargs)
    return (r.choices[0].message.content or "").strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", default="all", help="comma-separated model keys")
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    picks = excerpt_pool()
    clients = mk_clients()
    selected = list(MODELS) if args.models == "all" else [m.strip() for m in args.models.split(",") if m.strip() in MODELS]
    summary = {"timestamp": datetime.utcnow().isoformat() + "Z", "models": {}, "topics": TOPICS}

    for model_key in selected:
        cfg = MODELS[model_key]
        out_path = OUT_DIR / f"{model_key}.jsonl"
        done = 0
        fail = 0
        with out_path.open("w") as f:
            for ti, topic in enumerate(TOPICS):
                for repeat in range(3):
                    seed = f"{model_key}:{ti}:{repeat}:20260226"
                    rng = random.Random(seed)
                    shot = rng.sample(picks, 3)
                    user_prompt = build_prompt(topic, shot)
                    prompt_hash = hashlib.sha256(user_prompt.encode("utf-8")).hexdigest()[:16]
                    record = {
                        "model_key": model_key,
                        "model_id": cfg["model"],
                        "provider": cfg["provider"],
                        "priority": cfg["prio"],
                        "topic": topic,
                        "repeat": repeat + 1,
                        "temperature": cfg["temp"][repeat],
                        "fewshot_files": [s[0] for s in shot],
                        "prompt_hash": prompt_hash,
                        "created_at": datetime.utcnow().isoformat() + "Z",
                    }
                    for attempt in range(4):
                        try:
                            text = call_model(clients, cfg, SYSTEM_PROMPT, user_prompt, cfg["temp"][repeat])
                            if not text.strip():
                                raise RuntimeError("empty output")
                            record["status"] = "ok"
                            record["text"] = text
                            record["word_count"] = len(text.split())
                            done += 1
                            break
                        except Exception as e:
                            if attempt == 3:
                                record["status"] = "error"
                                record["error"] = str(e)
                                fail += 1
                            else:
                                time.sleep(2 + attempt * 2)
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    f.flush()
                    time.sleep(0.6)
        summary["models"][model_key] = {"ok": done, "error": fail, "output": str(out_path)}
        print(f"{model_key}: ok={done}, error={fail}")

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"Summary saved: {SUMMARY_PATH}")

if __name__ == "__main__":
    main()
