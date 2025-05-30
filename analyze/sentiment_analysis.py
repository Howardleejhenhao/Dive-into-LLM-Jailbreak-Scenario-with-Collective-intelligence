# positive_sentiment_rates_corrected.py

from merge_challenges_records import ChallengeManager
from transformers import pipeline

def positive_sentiment_rates():
    manager = ChallengeManager()
    success_msgs = manager.success_user_msgs
    fail_msgs = manager.fail_user_msgs

    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="uer/roberta-base-finetuned-dianping-chinese",
        tokenizer="uer/roberta-base-finetuned-dianping-chinese"
    )

    success_results = sentiment_pipeline(success_msgs, batch_size=32)
    success_positive = sum(1 for r in success_results if r["label"].upper().startswith("POS"))
    total_success = len(success_msgs)
    positive_rate_success = success_positive / total_success if total_success else 0

    fail_results = sentiment_pipeline(fail_msgs, batch_size=32)
    fail_positive = sum(1 for r in fail_results if r["label"].upper().startswith("POS"))
    total_fail = len(fail_msgs)
    positive_rate_fail = fail_positive / total_fail if total_fail else 0

    print(f"Positive sentiment rate among successful attacks: {positive_rate_success:.2%}")
    print(f"Positive sentiment rate among failed attacks:     {positive_rate_fail:.2%}")

if __name__ == "__main__":
    positive_sentiment_rates()
