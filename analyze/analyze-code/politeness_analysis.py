from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from merge_challenges_records import ChallengeManager

def politeness_rates():
    mgr = ChallengeManager()
    success_msgs = mgr.success_user_msgs
    fail_msgs    = mgr.fail_user_msgs

    model_id = "joeddav/xlm-roberta-large-xnli"
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    model     = AutoModelForSequenceClassification.from_pretrained(model_id)

    classifier = pipeline(
        "zero-shot-classification",
        model=model,
        tokenizer=tokenizer
    )
    labels = ["polite", "direct"]

    def is_polite(text):
        out = classifier(text, labels, multi_label=False)
        return out["labels"][0] == "polite"

    num_succ = len(success_msgs)
    num_fail = len(fail_msgs)

    polite_succ = sum(is_polite(t) for t in success_msgs)
    polite_fail = sum(is_polite(t) for t in fail_msgs)

    rate_succ = polite_succ / num_succ if num_succ else 0
    rate_fail = polite_fail / num_fail if num_fail else 0

    print(f"Politeness rate among successful attacks: {rate_succ:.2%} "
          f"({polite_succ}/{num_succ})")
    print(f"Politeness rate among failed attacks:     {rate_fail:.2%} "
          f"({polite_fail}/{num_fail})")

if __name__ == "__main__":
    politeness_rates()
