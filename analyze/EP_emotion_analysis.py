# emotion_analysis_by_phase.py

import json
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from merge_challenges_records import ChallengeManager

EMOTION_LABELS = [
    "neutral",
    "happy",
    "sad",
    "angry",
    "surprise",
    "fear",
    "disgust",
    "question"
]

def emotion_based_analysis():
    mgr = ChallengeManager()
    early_msgs = mgr.early_msgs
    mid_msgs   = mgr.mid_msgs
    late_msgs  = mgr.late_msgs

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
        if not msgs:
            return counts
        results = emotion_pipeline(msgs, batch_size=32)
        for r in results:
            idx = int(r["label"].split("_")[1])
            emo = EMOTION_LABELS[idx]
            counts[emo] += 1
        return counts

    early_counts = count_emotions(early_msgs)
    mid_counts   = count_emotions(mid_msgs)
    late_counts  = count_emotions(late_msgs)

    total_early = len(early_msgs)
    total_mid   = len(mid_msgs)
    total_late  = len(late_msgs)

    print("Emotion Analysis by Phase (Successful Attacks)")
    print("------------------------------------------------\n")
    print(f"{'Phase':<10} {'#Msgs':>7}  {'Emotion':<10} {'Count':>7}  {'% of Phase':>10}")
    print("-" *  50)
    for phase_name, counts, total in [
        ("Early", early_counts, total_early),
        ("Mid",   mid_counts,   total_mid),
        ("Late",  late_counts,  total_late),
    ]:
        for emo in EMOTION_LABELS:
            cnt = counts[emo]
            pct = cnt / total * 100 if total else 0.0
            print(f"{phase_name:<10} {total:>7}  {emo:<10} {cnt:>7}  {pct:>9.2f}%")
        print()

if __name__ == "__main__":
    emotion_based_analysis()
