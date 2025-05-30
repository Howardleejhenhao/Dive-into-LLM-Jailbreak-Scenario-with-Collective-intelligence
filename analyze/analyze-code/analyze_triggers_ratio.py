import jieba
from merge_challenges_records import ChallengeManager
from collections import Counter
import re

STOP_WORDS = set([
    "我","你","的","了","是","在","和","有","就",
    "也","都","嗎","吧","呢","喔","哦","哈哈",
    " ", "，","。","！","？"
])

def doc_term_counts(msgs):
    cnt = Counter()
    for msg in msgs:
        seen = set()
        for t in jieba.lcut(msg):
            t = t.strip()
            if not t or re.fullmatch(r"[\W\d_]+", t):
                continue
            if t in STOP_WORDS:
                continue
            if len(t) < 3:
                continue
            if t not in seen:
                cnt[t] += 1
                seen.add(t)
    return cnt

def find_common_terms(manager, top_n=20):
    succ_msgs = manager.success_user_msgs
    fail_msgs = manager.fail_user_msgs

    succ_cnt = doc_term_counts(succ_msgs)
    fail_cnt = doc_term_counts(fail_msgs)
    common = set(succ_cnt) & set(fail_cnt)

    total_succ = len(succ_msgs)
    total_fail = len(fail_msgs)

    data = []
    for t in common:
        ds = succ_cnt[t]
        df = fail_cnt[t]
        data.append((t, ds, df, ds/total_succ, df/total_fail))

    data.sort(key=lambda x: x[3], reverse=True)
    print(f"\nTop {top_n} Common Terms (by doc frequency, len≥3):")
    for t, ds, df, sr, fr in data[:top_n]:
        print(f"'{t}': succ_docs {ds}/{total_succ} ({sr:.2%}), "
              f"fail_docs {df}/{total_fail} ({fr:.2%})")

def find_exclusive_success_terms(manager, min_docs=5):
    succ_msgs = manager.success_user_msgs
    fail_msgs = manager.fail_user_msgs

    succ_cnt = doc_term_counts(succ_msgs)
    fail_cnt = doc_term_counts(fail_msgs)

    total_succ = len(succ_msgs)
    total_fail = len(fail_msgs)

    exclusive = []
    for t, ds in succ_cnt.items():
        df = fail_cnt.get(t, 0)
        if ds >= min_docs and df == 0:
            exclusive.append((t, ds))

    exclusive.sort(key=lambda x: x[1], reverse=True)
    print(f"\nTerms Only in Success (in ≥{min_docs} msgs):")
    for t, ds in exclusive:
        sr = ds / total_succ
        print(f"'{t}': succ_docs {ds}/{total_succ} ({sr:.2%}), fail_docs 0/{total_fail} (0.00%)")

def main():
    mgr = ChallengeManager()
    find_common_terms(mgr, top_n=20)
    find_exclusive_success_terms(mgr, min_docs=10)

if __name__ == '__main__':
    main()
