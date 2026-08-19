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
        "implementation": 0.8,
        "brute force": 0.6,
        "greedy": 0.6,       
        "sortings": 0.9,
        "two pointers": 1.0,
        "binary search": 1.0,
        "math": 0.9,
        "constructive algorithms": 1.2,
        "bitmasks": 1.3,
        "number theory": 1.4,
        "combinatorics": 1.5,
        "dfs and similar": 1.5,
        "trees": 1.5,
        "strings": 1.7,
        "graphs": 1.7,
        "data structures": 1.8,
        "dp": 1.9,
        "dsu": 1.9,
        "shortest paths": 2.0,
        "hashing": 2.2,
        "games": 2.2,
        "divide and conquer": 2.3,
        "interactive": 2.4,
        "probabilities": 2.5,
        "matrices": 2.5,
        "geometry": 2.6,
        "ternary search": 2.7,
        "expression parsing": 3.0,
        "graph matchings": 3.0,
        "meet-in-the-middle": 3.2,
        "communication": 3.3,
        "2-sat": 3.5,
        "flows": 3.5,
        "chinese remainder theorem": 3.6,
        "string suffix structures": 3.8,
        "fft": 4.0,
        "schedules": 4.0,
        "*special": 2.0,
    }

    tag_to_monster = {
        "implementation": "Warrior",
        "greedy": "Fiend",
        "math": "Spellcaster",
        "brute force": "Beast",
        "sortings": "Warrior",
        "binary search": "Rock",
        "constructive algorithms": "Machine",
        "number theory": "Spellcaster",
        "bitmasks": "Zombie",
        "dfs and similar": "Insect",
        "strings": "Winged Beast",
        "trees": "Plant",
        "combinatorics": "Fairy",
        "graphs": "Thunder",
        "data structures": "Cyberse",
        "dp": "Dragon",
        "two pointers": "Beast-Warrior",
        "dsu": "Cyberse",
        "shortest paths": "Winged Beast",
        "hashing": "Zombie",
        "games": "Fiend",
        "divide and conquer": "Thunder",
        "interactive": "Psychic",
        "matrices": "Machine",
        "geometry": "Dinosaur",
        "ternary search": "Rock",
        "probabilities": "Illusion",
        "expression parsing": "Spellcaster",
        "graph matchings": "Reptile",
        "meet-in-the-middle": "Beast",
        "communication": "Psychic",
        "flows": "Aqua",
        "2-sat": "Insect",
        "chinese remainder theorem": "Divine-Beast",
        "string suffix structures": "Wyrm",
        "fft": "Fish",
        "schedules": "Pyro",
        "*special": "Creator-God",
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

    user_max_rating = user.max_rating
    target_atk = int(user_max_rating * 1.25)

    user_solved = user.solved_problems
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

        card_id = int(card.get("id"))

        if (distance < min_distance) or (distance == min_distance and card_id < best_tiebreak):
            min_distance = distance
            best_tiebreak = card_id
            best_card = card

    images = best_card.get("card_images")
    image_url = images[0].get("image_url")
    return image_url