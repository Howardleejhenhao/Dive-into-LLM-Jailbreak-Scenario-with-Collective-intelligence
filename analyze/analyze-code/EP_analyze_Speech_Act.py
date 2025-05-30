import json
from transformers import pipeline
from merge_challenges_records import ChallengeManager
from collections import Counter

def zero_shot_phase_type_rates():
    mgr = ChallengeManager()
    early_msgs = mgr.early_msgs
    mid_msgs   = mgr.mid_msgs
    late_msgs  = mgr.late_msgs

    classifier = pipeline(
        "zero-shot-classification",
        model="joeddav/xlm-roberta-large-xnli"
    )
    candidate_labels = ["declarative", "question", "command", "exclamation"]

    def classify_bulk(messages):
        if not messages:
            return []
        results = classifier(messages, candidate_labels, batch_size=32)
        return [r["labels"][0] for r in results]
    early_labels = classify_bulk(early_msgs)
    mid_labels   = classify_bulk(mid_msgs)
    late_labels  = classify_bulk(late_msgs)

    def compute_rate(labels):
        cnt = Counter(labels)
        total = sum(cnt.values()) or 1
        return {lbl: cnt.get(lbl, 0) / total for lbl in candidate_labels}

    early_rates = compute_rate(early_labels)
    mid_rates   = compute_rate(mid_labels)
    late_rates  = compute_rate(late_labels)

    print("Sentence type distribution in EARLY phase:")
    for lbl, rate in early_rates.items():
        print(f"  {lbl}: {rate:.1%}")
    print("\nSentence type distribution in MID phase:")
    for lbl, rate in mid_rates.items():
        print(f"  {lbl}: {rate:.1%}")
    print("\nSentence type distribution in LATE phase:")
    for lbl, rate in late_rates.items():
        print(f"  {lbl}: {rate:.1%}")

if __name__ == "__main__":
    zero_shot_phase_type_rates()
