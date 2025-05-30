import jieba
import string
import re
import numpy as np
import pandas as pd
from merge_challenges_records import ChallengeManager

def compute_metrics(sentence: str):
    text = sentence.strip()
    char_count = len(text)
    words = [w for w in jieba.lcut(text) if w.strip()]
    word_count = len(words)
    avg_word_len = np.mean([len(w) for w in words]) if words else 0
    unique_words = len(set(words))
    ttr = unique_words / word_count if word_count else 0
    punct_count = len([ch for ch in text if ch in string.punctuation or re.match(r'[\u3000-\u303F\uFF00-\uFFEF]', ch)])
    punct_ratio = punct_count / char_count if char_count else 0
    return {
        'char_count': char_count,
        'word_count': word_count,
        'avg_word_len': avg_word_len,
        'type_token_ratio': ttr,
        'punct_ratio': punct_ratio
    }

def analyze_readability():
    manager = ChallengeManager()
    data = []

    for label, msgs in [('success', manager.success_user_msgs), ('fail', manager.fail_user_msgs)]:
        for s in msgs:
            metrics = compute_metrics(s)
            metrics['label'] = label
            metrics['text'] = s
            data.append(metrics)

    df = pd.DataFrame(data)

    summary = df.groupby('label').agg({
        'char_count': ['mean', 'std'],
        'word_count': ['mean', 'std'],
        'avg_word_len': ['mean', 'std'],
        'type_token_ratio': ['mean', 'std'],
        'punct_ratio': ['mean', 'std']
    })

    print("Readability & Complexity Metrics by Attack Outcome:\n")
    print(summary)

if __name__ == "__main__":
    analyze_readability()
