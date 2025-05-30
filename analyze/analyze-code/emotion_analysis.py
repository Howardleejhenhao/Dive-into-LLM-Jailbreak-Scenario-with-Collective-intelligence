# emotion_analysis_with_names.py

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from merge_challenges_records import ChallengeManager

EMOTION_LABELS = [
    "neutral",     # LABEL_0
    "happy",       # LABEL_1
    "sad",         # LABEL_2
    "angry",       # LABEL_3
    "surprise",    # LABEL_4
    "fear",        # LABEL_5
    "disgust",     # LABEL_6
    "question"     # LABEL_7
]

def emotion_based_analysis():
    mgr = ChallengeManager()
    success_msgs = mgr.success_user_msgs
    fail_msgs    = mgr.fail_user_msgs

    model_id = "Johnson8187/Chinese-Emotion"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model     = AutoModelForSequenceClassification.from_pretrained(model_id)
    emotion_pipeline = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        return_all_scores=False
    )

    def count_emotions(msgs):
        counts = {emo: 0 for emo in EMOTION_LABELS}
        results = emotion_pipeline(msgs, batch_size=32)
        for r in results:
            idx = int(r["label"].split("_")[1])
            emo = EMOTION_LABELS[idx]
            counts[emo] += 1
        return counts

    success_counts = count_emotions(success_msgs)
    fail_counts    = count_emotions(fail_msgs)
    total_succ = len(success_msgs)
    total_fail = len(fail_msgs)

    print("Emotion Analysis of Jailbreak Prompts")
    print("-------------------------------------")
    print(f"Total successful prompts: {total_succ}")
    print(f"Total failed prompts:    {total_fail}\n")
    print(f"{'Emotion':<10} {'Success %':>10} {'Fail %':>10}")
    print("-" * 32)
    for emo in EMOTION_LABELS:
        sr = success_counts[emo] / total_succ if total_succ else 0
        fr = fail_counts[emo]    / total_fail if total_fail else 0
        print(f"{emo:<10} {sr:>9.2%} {fr:>9.2%}")

if __name__ == "__main__":
    emotion_based_analysis()
