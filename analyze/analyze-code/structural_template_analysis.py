import re
from collections import Counter
from merge_challenges_records import ChallengeManager

def extract_template(text):
    m = re.match(r'^([A-Za-z\u4e00-\u9fff]+[:：])', text.strip())
    if m:
        return m.group(1)
    m = re.match(r'^(you are [A-Za-z]+|你是 [\u4e00-\u9fff]+)', text.strip(), re.IGNORECASE)
    if m:
        return m.group(1)
    return 'NONE'

def analyze_templates():
    mgr = ChallengeManager()
    data = []
    for txt in mgr.success_user_msgs:
        data.append(('success', txt))
    for txt in mgr.fail_user_msgs:
        data.append(('fail', txt))

    template_counts = Counter()
    template_success = Counter()
    template_fail = Counter()

    for label, text in data:
        tpl = extract_template(text)
        template_counts[tpl] += 1
        if label == 'success':
            template_success[tpl] += 1
        else:
            template_fail[tpl] += 1

    print(f"{'TEMPLATE':<20} {'TOTAL':>5} {'SUCCESS':>8} {'FAIL':>6} {'SUCCESS_RATE':>13}")
    print('-' * 60)
    for tpl, total in template_counts.most_common():
        succ = template_success[tpl]
        fail = template_fail[tpl]
        rate = succ / total if total else 0
        print(f"{tpl:<20} {total:5d} {succ:8d} {fail:6d} {rate:13.2%}")

if __name__ == '__main__':
    analyze_templates()
