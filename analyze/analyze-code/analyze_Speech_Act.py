import json
from transformers import pipeline
from merge_challenges_records import ChallengeManager
from collections import Counter

def zero_shot_sentence_type_rates():
    mgr = ChallengeManager()
    success_msgs = mgr.success_user_msgs
    fail_msgs = mgr.fail_user_msgs

    classifier = pipeline(
        "zero-shot-classification",
        model="joeddav/xlm-roberta-large-xnli"
    )
    candidate_labels = ["declarative", "question", "command", "exclamation"]

    def classify_bulk(messages):
        results = classifier(messages, candidate_labels, batch_size=32)
        return [r["labels"][0] for r in results]

    success_labels = classify_bulk(success_msgs)
    fail_labels    = classify_bulk(fail_msgs)

    def compute_rate(labels):
        cnt = Counter(labels)
        total = sum(cnt.values())
        return {lbl: cnt.get(lbl, 0) / total for lbl in candidate_labels}

    success_rates = compute_rate(success_labels)
    fail_rates    = compute_rate(fail_labels)

    print("Sentence type distribution among successful attacks:")
    for lbl, rate in success_rates.items():
        print(f"  {lbl}: {rate:.1%}")
    print("\nSentence type distribution among failed attacks:")
    for lbl, rate in fail_rates.items():
        print(f"  {lbl}: {rate:.1%}")

if __name__ == "__main__":
    zero_shot_sentence_type_rates()
