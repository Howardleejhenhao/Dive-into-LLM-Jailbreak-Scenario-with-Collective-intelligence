# politeness_analysis_by_phase.py

import json
from pathlib import Path
from collections import Counter

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from merge_challenges_records import ChallengeManager

def politeness_direct_none_rates_by_phase(threshold=0.5, top_phases=("early", "mid", "late")):
    mgr = ChallengeManager()
    phase_msgs = {
        "early": mgr.early_msgs,
        "mid":   mgr.mid_msgs,
        "late":  mgr.late_msgs
    }

    tokenizer = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli", use_fast=False)
    model     = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")
    classifier = pipeline(
        "zero-shot-classification",
        model=model,
        tokenizer=tokenizer,
        multi_label=True
    )

    candidate_labels = ["polite", "direct"]

    def categorize(text: str) -> str:
        out = classifier(text, candidate_labels)
        scores = dict(zip(out["labels"], out["scores"]))
        polite_score = scores.get("polite", 0.0)
        direct_score = scores.get("direct", 0.0)
        if polite_score >= threshold and polite_score > direct_score:
            return "polite"
        elif direct_score >= threshold and direct_score > polite_score:
            return "direct"
        else:
            return "none"

    def compute_rates(msgs: list[str]) -> tuple[dict, Counter, int]:
        cats = [categorize(t) for t in msgs]
        total = len(cats)
        counts = Counter(cats)
        rates = {cat: counts.get(cat, 0) / total if total > 0 else 0.0
                 for cat in ["polite", "direct", "none"]}
        return rates, counts, total

    for phase in top_phases:
        msgs = phase_msgs.get(phase, [])
        rates, counts, total = compute_rates(msgs)

        print(f"--- {phase.title()} Phase ({total} messages) ---")
        for cat in ["polite", "direct", "none"]:
            cnt = counts.get(cat, 0)
            pct = rates.get(cat, 0.0) * 100
            print(f"{cat.capitalize():<6}: {cnt}/{total} ({pct:.2f}%)")
        print()

if __name__ == "__main__":
    politeness_direct_none_rates_by_phase()
