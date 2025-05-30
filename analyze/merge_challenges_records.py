import json
from pathlib import Path
import math

class ChallengeManager:
    def __init__(self,
                 challenges_source=Path('game-data') / 'challenges.json',
                 records_source=Path('game-data') / 'game_records.json'):
        self.challenges = self._load_json(challenges_source)
        self.records = self._load_json(records_source)
        self.records_map = {}
        self.success_user_msgs = []
        self.success_model_msgs = []
        self.fail_user_msgs = []
        self.fail_model_msgs = []
        for rec in self.records:
            cid = rec.get('challenge_id')
            self.records_map.setdefault(cid, []).append(rec)
            is_success = rec.get('winner') == 'attacker'
            for turn in rec.get('conversation', []):
                role = turn.get('role')
                for part in turn.get('parts', []):
                    text = part.get('text')
                    if role == 'user':
                        (self.success_user_msgs if is_success else self.fail_user_msgs).append(text)
                    elif role == 'model':
                        (self.success_model_msgs if is_success else self.fail_model_msgs).append(text)
        self.early_msgs, self.mid_msgs, self.late_msgs = self._categorize_phases()

    def _load_json(self, source):
        if isinstance(source, (str, Path)):
            with Path(source).open('r', encoding='utf-8') as f:
                return json.load(f)
        elif isinstance(source, list):
            return source
        raise ValueError

    def _categorize_phases(self):
        early, mid, late = [], [], []
        for rec in self.records:
            if rec.get('winner') != 'attacker':
                continue
            convo = rec.get('conversation', [])
            user_msgs = [turn['parts'][0]['text']
                         for turn in convo
                         if turn.get('role') == 'user']
            total = len(user_msgs)
            if total == 0:
                continue
            if total < 2:
                late.extend(user_msgs)
                continue
            e_cut = math.ceil(total / 3)
            m_cut = math.ceil(2 * total / 3)
            for idx, text in enumerate(user_msgs):
                if idx < e_cut:
                    early.append(text)
                elif idx < m_cut:
                    mid.append(text)
                else:
                    late.append(text)
        return early, mid, late

    def get_combined_list(self):
        return list(self.records_map.values())

    def get_by_id(self, challenge_id):
        return self.records_map.get(challenge_id)

    def validate(self):
        total = len(self.records)
        su = len(self.success_user_msgs)
        sm = len(self.success_model_msgs)
        fu = len(self.fail_user_msgs)
        fm = len(self.fail_model_msgs)
        eu = len(self.early_msgs)
        mu = len(self.mid_msgs)
        lu = len(self.late_msgs)
        print(f"sessions: {total}; "
              f"success user msgs: {su}, success model msgs: {sm}; "
              f"fail user msgs: {fu}, fail model msgs: {fm}; "
              f"early: {eu}, mid: {mu}, late: {lu}")

if __name__ == '__main__':
    manager = ChallengeManager()
    manager.validate()
    print("Early phase messages:", manager.early_msgs)
    print("Mid phase messages:", manager.mid_msgs)
    print("Late phase messages:", manager.late_msgs)
