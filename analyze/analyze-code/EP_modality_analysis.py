import json
from merge_challenges_records import ChallengeManager
from transformers import pipeline
from collections import Counter

def phase_modality_analysis():
    manager = ChallengeManager()
    early_msgs = manager.early_msgs
    mid_msgs   = manager.mid_msgs
    late_msgs  = manager.late_msgs

    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

    labels = ["factual", "suggestion", "hypothetical", "conditional"]

    def classify_phase(texts):
        if not texts:
            return []
        results = classifier(
            texts,
            candidate_labels=labels,
            multi_label=False,
            batch_size=16
        )
        if isinstance(results, dict):
            results = [results]
        return [res["labels"][0] for res in results]

    early_preds = classify_phase(early_msgs)
    mid_preds   = classify_phase(mid_msgs)
    late_preds  = classify_phase(late_msgs)

    def print_distribution(name, msgs, preds):
        counts = Counter(preds)
        total = len(msgs)
        print(f"\nModality distribution for {name} phase (n={total}):")
        for label in labels:
            count = counts.get(label, 0)
            rate = count / total if total else 0
            print(f"  {label}: {count}/{total} ({rate:.2%})")

    print_distribution("early", early_msgs, early_preds)
    print_distribution("mid", mid_msgs, mid_preds)
    print_distribution("late", late_msgs, late_preds)

if __name__ == "__main__":
    phase_modality_analysis()
