import json
import csv
import os

with open('../analyze/game-data/challenges.json', 'r', encoding='utf-8') as f:
    challenges = json.load(f)

with open('../analyze/game-data/challenges.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = [
        'id', 'creator_username', 'description', 'defender_prompt', 'defender_first_reply',
        'forbidden_words', 'model', 'successful_attacks', 'category'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for c in challenges:
        writer.writerow({k: c.get(k, '') for k in fieldnames})

with open('../analyze/game-data/game_records.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

with open('../analyze/game-data/game_records.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = [
        'challenge_id', 'winner', 'turns', 'attacker_username', 'defender_username', 'score', 'conversation'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in records:
        conv = []
        for turn in r.get('conversation', []):
            role = turn.get('role', '')
            text = '\n'.join([p.get('text', '') for p in turn.get('parts', [])])
            score = turn.get('score', None)
            if score is not None:
                conv.append(f"[{role}] {text} (score={score})")
            else:
                conv.append(f"[{role}] {text}")
        r_csv = {k: r.get(k, '') for k in fieldnames if k != 'conversation'}
        r_csv['conversation'] = '\n---\n'.join(conv)
        writer.writerow(r_csv)
