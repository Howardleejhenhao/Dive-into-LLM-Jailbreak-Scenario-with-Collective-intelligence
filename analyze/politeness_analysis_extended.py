# politeness_analysis_extended.py

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from merge_challenges_records import ChallengeManager
from collections import Counter

def politeness_direct_none_rates(threshold=0.5):
    mgr = ChallengeManager()
    success_msgs = mgr.success_user_msgs
    fail_msgs    = mgr.fail_user_msgs

    tokenizer = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli", use_fast=False)
    model     = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")
    classifier = pipeline(
        "zero-shot-classification",
        model=model,
        tokenizer=tokenizer,
        multi_label=True
    )

    candidate_labels = ["polite", "direct"]

    def categorize(text):
        out = classifier(text, candidate_labels)
        scores = dict(zip(out["labels"], out["scores"]))
        polite_score = scores.get("polite", 0)
        direct_score = scores.get("direct", 0)
        if polite_score >= threshold and polite_score > direct_score:
            return "polite"
        elif direct_score >= threshold and direct_score > polite_score:
            return "direct"
        else:
            return "none"

    def compute_rates(msgs):
        cats = [categorize(t) for t in msgs]
        total = len(cats)
        counts = Counter(cats)
        return {cat: counts.get(cat, 0) / total for cat in ["polite", "direct", "none"]}, counts, total

    rates_succ, counts_succ, total_succ = compute_rates(success_msgs)
    rates_fail, counts_fail, total_fail = compute_rates(fail_msgs)

    print("Categories among successful attacks:")
    for cat in ["polite", "direct", "none"]:
        print(f"- {cat.capitalize()}: {counts_succ.get(cat,0)}/{total_succ} "
              f"({rates_succ.get(cat,0)*100:.2f}%)")
    print("\nCategories among failed attacks:")
    for cat in ["polite", "direct", "none"]:
        print(f"- {cat.capitalize()}: {counts_fail.get(cat,0)}/{total_fail} "
              f"({rates_fail.get(cat,0)*100:.2f}%)")

if __name__ == "__main__":
    politeness_direct_none_rates()

