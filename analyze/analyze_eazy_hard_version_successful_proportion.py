import json
from pathlib import Path
import matplotlib.pyplot as plt

easy_version_id = [
    'ffaab627-1fc7-4afa-a7c8-894e15c54b8b',
    '9d4c15d1-128a-408e-a34c-4810db13e87e',
    '9b3c8e46-2c71-4e93-ab5a-e92d1d14968d',
    'd514a7fc-ec3d-44d7-ab88-fd19b43b82e1'
]
hard_version_id = [
    '8d330c03-93c8-43c3-80c6-0a335172a6cd',
    'ee5b5a9d-ff83-46c3-836c-835173c0eddb',
    'b6a01639-8b47-432a-aeff-eb2833ad2a25',
    'c7fda774-2f05-4e1b-8176-f5c96f3bb5ce'
]

records_path = Path('game-data') / 'game_records.json'
with records_path.open('r', encoding='utf-8') as f:
    records = json.load(f)

def compute_stats(ids):
    relevant = [rec for rec in records if rec.get('challenge_id') in ids]
    total = len(relevant)
    success = sum(1 for rec in relevant if rec.get('winner') == 'attacker')
    return total, success

easy_total, easy_success = compute_stats(easy_version_id)
hard_total, hard_success = compute_stats(hard_version_id)

easy_rate = easy_success / easy_total if easy_total > 0 else 0
hard_rate = hard_success / hard_total if hard_total > 0 else 0

categories = ['Easy', 'Hard']
rates = [easy_rate, hard_rate]

plt.figure(figsize=(6, 4))
bars = plt.bar(categories, rates, color=['skyblue', 'salmon'])
plt.title('Attack Success Rate by Difficulty')
plt.ylabel('Success Rate')
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', linewidth=0.5)

for bar, total, success, rate in zip(bars, [easy_total, hard_total], [easy_success, hard_success], rates):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, 
        height + 0.02, 
        f"{success}/{total}\n{rate:.1%}", 
        ha='center', 
        va='bottom'
    )

plt.show()
