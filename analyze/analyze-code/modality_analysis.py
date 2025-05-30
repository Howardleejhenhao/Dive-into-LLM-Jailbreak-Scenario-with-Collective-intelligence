import json
from merge_challenges_records import ChallengeManager
from transformers import pipeline
from collections import Counter

def modality_analysis():
    manager = ChallengeManager()
    success_msgs = manager.success_user_msgs
    fail_msgs    = manager.fail_user_msgs

    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

    labels = ["factual", "suggestion", "hypothetical", "conditional"]

    def classify_batch(texts):
        results = classifier(
            texts,
            candidate_labels=labels,
            multi_label=False,
            batch_size=16
        )
        if isinstance(results, dict):
            results = [results]
        return [res["labels"][0] for res in results]
    success_preds = classify_batch(success_msgs)
    fail_preds    = classify_batch(fail_msgs)

    success_counts = Counter(success_preds)
    fail_counts    = Counter(fail_preds)
    total_success  = len(success_msgs)
    total_fail     = len(fail_msgs)

    print("Modality distribution for successful attacks:")
    for label in labels:
        count = success_counts.get(label, 0)
        rate  = count / total_success if total_success else 0
        print(f"  {label}: {count}/{total_success} ({rate:.2%})")

    print("\nModality distribution for failed attacks:")
    for label in labels:
        count = fail_counts.get(label, 0)
        rate  = count / total_fail if total_fail else 0
        print(f"  {label}: {count}/{total_fail} ({rate:.2%})")

if __name__ == "__main__":
    modality_analysis()
