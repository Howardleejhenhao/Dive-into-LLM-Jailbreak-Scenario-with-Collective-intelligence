import json
from pathlib import Path
import pprint

class ChallengeManager:
    """
    Load and manage challenges and their game records for analysis.
    Provides:
      - self.records_map: mapping challenge_id -> list of raw game records
      - self.combined_map: mapping challenge_id -> combined metadata + records + all utterances
    Default JSON paths are used if not provided.
    """
    def __init__(self, challenges_source=Path('game-data') / 'challenges.json', records_source=Path('game-data') / 'game_records.json'):
        # Load raw data
        self.challenges = self._load_json(challenges_source)
        self.records = self._load_json(records_source)
        self.records_map = {}
        for rec in self.records:
            cid = rec.get('challenge_id')
            self.records_map.setdefault(cid, []).append(rec)
        self.combined_map = {}
        for chal in self.challenges:
            cid = chal.get('id')
            records = self.records_map.get(cid, [])
            utterances = []
            for sess in records:
                for turn in sess.get('conversation', []):
                    role = turn.get('role')
                    for part in turn.get('parts', []):
                        text = part.get('text')
                        utterances.append({'role': role, 'text': text})
            self.combined_map[cid] = {
                'id': cid,
                'model': chal.get('model'),
                'description': chal.get('description'),
                'defender_prompt': chal.get('defender_prompt'),
                'forbidden_words': chal.get('forbidden_words'),
                'defender_first_reply': chal.get('defender_first_reply'),
                'successful_attacks': chal.get('successful_attacks'),
                'creator': chal.get('creator_username'),
                'game_records': records,
                'all_utterances': utterances
            }

    def _load_json(self, source):
        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(f"JSON file not found: {path}")
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
        elif isinstance(source, list):
            return source
        else:
            raise ValueError(f"Unsupported source type: {type(source)}")

    def get_combined_list(self):
        return list(self.combined_map.values())

    def get_by_id(self, challenge_id):
        return self.combined_map.get(challenge_id)

    def validate(self):
        ids_chal = {c.get('id') for c in self.challenges}
        ids_map = set(self.records_map.keys())
        total_sessions = len(self.records)
        total_utterances = sum(len(v['all_utterances']) for v in self.combined_map.values())
        if self.combined_map:
            sample = next(iter(self.combined_map.values()))
            for k, v in sample.items():
                if k not in ('game_records', 'all_utterances'):
                    print(f"  {k}: {v}")
        print("Validation passed.")

if __name__ == '__main__':
    manager = ChallengeManager()
    manager.validate()
    print(manager.combined_map["b18a4c20-4949-46d4-8121-41408728f269"])