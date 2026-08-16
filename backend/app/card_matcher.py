import math
import json

from app.models import User
from typing import Any

with open('app/cache/monster_card_list.json', 'r') as file:
    MONSTERS: list[dict] = json.load(file)


async def most_close_card(user: User) -> str | None:
    #Select the most similar YuGiOh card according to the user stats

    def _to_int(value: Any, default: int = 0) -> int:
        try:
            if value in (None, "", "?"):
                return default
            return int(float(value))
        except (TypeError, ValueError):
            return default

    tag_weight = {
        # Most common tags
        "implementation": 0.1,
        "math": 0.3,
        "greedy": 0.3,
        "brute force": 0.4,
        # Uncommon tags
        "constructive algorithms": 0.7,
        "data structures": 0.8,
        "sortings": 0.7,
        "two pointers": 0.8,
        "binary search": 0.8,
        # Specialized tags
        "dp": 1.2,
        "graphs": 1.3,
        "trees": 1.3,
        "number theory": 1.4,
        "dfs and similar": 1.2,
        "combinatorics": 1.4,
        "geometry": 1.6,
        "bitmasks": 1.5,
        "shortest paths": 1.5,
        "string suffix structures": 2.0,
        "fft": 2.0,
    }

    tag_to_monster = {
        "implementation": "Warrior",
        "brute force": "Beast",
        "greedy": "Fiend",
        "math": "Spellcaster",
        "number theory": "Spellcaster",
        "combinatorics": "Fairy",
        "fft": "Psychic",
        "data structures": "Cyberse",
        "trees": "Plant",
        "bitmasks": "Zombie",
        "string suffix structures": "Dragon",
        "graphs": "Thunder",
        "dfs and similar": "Insect",
        "shortest paths": "Winged Beast",
        "geometry": "Machine",
        "binary search": "Rock",
        "two pointers": "Aqua",
        "constructive algorithms": "Pyro",
        "dp": "Wyrm",
        "sortings": "Sea Serpent",
    }

    max_rank_to_level = {
        "headquarters": 0,
        "unrated": 0,
        "newbie": 1,
        "pupil": 2,
        "specialist": 4,
        "expert": 5,
        "candidate master": 6,
        "master": 7,
        "international master": 8,
        "grandmaster": 9,
        "international grandmaster": 10,
        "legendary grandmaster": 11,
        "legend": 12,
        "tourist": 12,
        "jiangly": 12,
    }

    dominant_tag = "implementation"
    max_score = -1.0

    for item in user.tags:
        raw_tag, count = item[0], item[1]
        clean_tag = str(raw_tag).lower()
        weight = tag_weight.get(clean_tag, 1.0)

        try:
            score = float(count) * weight
        except (TypeError, ValueError):
            continue

        if score > max_score:
            max_score = score
            dominant_tag = clean_tag

    target_race = tag_to_monster.get(dominant_tag)

    user_max_rating = _to_int(user.max_rating, 0)
    target_atk = int(user_max_rating * 1.25)

    user_solved = max(_to_int(user.solved_problems, 0), 0)
    target_def = min(int(math.sqrt(user_solved) * 36.5), 4000)

    user_rank = user.max_rank.lower()
    target_level = max_rank_to_level.get(user_rank, 1)

    if target_level >= 10:
        candidates = [
            card for card in MONSTERS
            if _to_int(card.get("level") or card.get("rank") or 0, 0) >= 10
        ]
    else:
        candidates = [
            card for card in MONSTERS
            if str(card.get("race", "")).lower() == target_race.lower()
        ]

    if not candidates:
        candidates = MONSTERS

    w_atk, w_def, w_level = 0.55, 0.25, 0.20
    best_card = None
    min_distance = float("inf")
    best_tiebreak = float("inf")

    for card in candidates:
        card_atk = _to_int(card.get("atk"), 0)
        card_def = _to_int(card.get("def"), 0)
        card_level = _to_int(card.get("level") or card.get("rank") or card.get("linkval"), 1)

        norm_atk_diff = (target_atk - card_atk) / 4000.0
        norm_def_diff = (target_def - card_def) / 4000.0
        norm_level_diff = (target_level - card_level) / 12.0

        distance = math.sqrt(
            w_atk * (norm_atk_diff ** 2) +
            w_def * (norm_def_diff ** 2) +
            w_level * (norm_level_diff ** 2)
        )

        card_id = _to_int(card.get("id"), 10**12)

        if (distance < min_distance) or (distance == min_distance and card_id < best_tiebreak):
            min_distance = distance
            best_tiebreak = card_id
            best_card = card

    images = best_card.get("card_images", []) if best_card else []
    image_url = images[0].get("image_url") if images else None
    return image_url