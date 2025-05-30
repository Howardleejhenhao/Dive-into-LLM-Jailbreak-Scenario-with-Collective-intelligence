from merge_challenges_records import ChallengeManager
from collections import Counter

top_n = 50
def analyze_success_user(manager, top_n=top_n, substr_len=4):
    msgs = manager.success_user_msgs
    subs = Counter()
    for msg in msgs:
        text = msg.replace(' ', '')
        for i in range(len(text) - substr_len + 1):
            subs[text[i:i+substr_len]] += 1
    words = Counter(w for msg in msgs for w in msg.split())
    print(f"\nTop {top_n} words in successful user messages:")
    for word, cnt in words.most_common(top_n):
        print(f"'{word}': {cnt}")


def analyze_success_model(manager, top_n=top_n, substr_len=4):
    msgs = manager.success_model_msgs
    subs = Counter()
    for msg in msgs:
        text = msg.replace(' ', '')
        for i in range(len(text) - substr_len + 1):
            subs[text[i:i+substr_len]] += 1
    words = Counter(w for msg in msgs for w in msg.split())
    print(f"\nTop {top_n} words in successful model messages:")
    for word, cnt in words.most_common(top_n):
        print(f"'{word}': {cnt}")


def analyze_fail_user(manager, top_n=top_n, substr_len=4):
    msgs = manager.fail_user_msgs
    subs = Counter()
    for msg in msgs:
        text = msg.replace(' ', '')
        for i in range(len(text) - substr_len + 1):
            subs[text[i:i+substr_len]] += 1
    words = Counter(w for msg in msgs for w in msg.split())
    print(f"\nTop {top_n} words in failed user messages:")
    for word, cnt in words.most_common(top_n):
        print(f"'{word}': {cnt}")


def analyze_fail_model(manager, top_n=top_n, substr_len=4):
    msgs = manager.fail_model_msgs
    subs = Counter()
    for msg in msgs:
        text = msg.replace(' ', '')
        for i in range(len(text) - substr_len + 1):
            subs[text[i:i+substr_len]] += 1
    words = Counter(w for msg in msgs for w in msg.split())
    print(f"\nTop {top_n} words in failed model messages:")
    for word, cnt in words.most_common(top_n):
        print(f"'{word}': {cnt}")


def main():
    manager = ChallengeManager()
    analyze_success_user(manager)
    analyze_success_model(manager)
    analyze_fail_user(manager)
    analyze_fail_model(manager)

if __name__ == '__main__':
    main()
