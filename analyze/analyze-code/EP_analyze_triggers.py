import json
from collections import Counter
from merge_challenges_records import ChallengeManager

TOP_N = 50
SUBSTR_LEN = 4

def analyze_phase(msgs, phase_name, top_n=TOP_N, substr_len=SUBSTR_LEN):
    print(f"\n=== {phase_name.upper()} PHASE ===")
    subs = Counter()
    for msg in msgs:
        text = msg.replace(' ', '')
        for i in range(len(text) - substr_len + 1):
            subs[text[i:i+substr_len]] += 1
    words = Counter(w for msg in msgs for w in msg.split())
    print(f"\nTop {top_n} words:")
    for word, cnt in words.most_common(top_n):
        print(f"'{word}': {cnt}")

def main():
    mgr = ChallengeManager()
    early = mgr.early_msgs
    mid   = mgr.mid_msgs
    late  = mgr.late_msgs

    analyze_phase(early, "early")
    analyze_phase(mid,   "mid")
    analyze_phase(late,  "late")

if __name__ == '__main__':
    main()
