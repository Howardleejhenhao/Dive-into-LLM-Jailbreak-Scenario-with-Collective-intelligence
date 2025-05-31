import numpy as np
from transformers import pipeline
from merge_challenges_records import ChallengeManager

def compute_toxicity_scores(messages, tox_pipeline):
    results = tox_pipeline(messages, batch_size=16, top_k=None)
    if results and isinstance(results[0], dict):
        results = [results]
    non_toxic_scores = []
    toxic_scores     = []
    for score_list in results:
        d = {item["label"]: item["score"] for item in score_list}
        non_toxic_scores.append(d.get("NON_TOXIC", 0.0))
        toxic_scores.append(d.get("TOXIC", 0.0))
    avg_non_toxic = float(np.mean(non_toxic_scores)) if non_toxic_scores else 0.0
    avg_toxic     = float(np.mean(toxic_scores))     if toxic_scores     else 0.0
    return avg_non_toxic, avg_toxic

def main():
    manager = ChallengeManager()
    success_msgs = manager.success_user_msgs
    fail_msgs    = manager.fail_user_msgs

    tox_pipeline = pipeline(
        "text-classification",
        model="textdetox/xlmr-large-toxicity-classifier-v2",
        tokenizer="textdetox/xlmr-large-toxicity-classifier-v2",
        top_k=None
    )

    s_non, s_tox = compute_toxicity_scores(success_msgs, tox_pipeline)
    f_non, f_tox = compute_toxicity_scores(fail_msgs,    tox_pipeline)

    print("=== Toxicity Scores ===")
    print(f"Successful attacks (n={len(success_msgs)}):")
    print(f"  Avg NON_TOXIC: {s_non:.4f}")
    print(f"  Avg TOXIC    : {s_tox:.4f}\n")
    print(f"Failed attacks     (n={len(fail_msgs)}):")
    print(f"  Avg NON_TOXIC: {f_non:.4f}")
    print(f"  Avg TOXIC    : {f_tox:.4f}")

if __name__ == "__main__":
    main()
