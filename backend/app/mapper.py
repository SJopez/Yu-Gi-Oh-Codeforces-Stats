from __future__ import annotations
import math
from typing import Any, Dict, List, Optional

from app.models import User


RANK_TO_LEVEL: Dict[str, int] = {
    'newbie': 1,
    'pupil': 2,
    'specialist': 3,
    'expert': 4,
    'candidate master': 5,
    'master': 7,
    'international master': 8,
    'grandmaster': 10,
    'international grandmaster': 11,
    'legendary grandmaster': 12,
    'tourist': 12,
    'jiangly': 12,
}

TAG_TO_RACE: Dict[str, str] = {
    'dp': 'Wyrm',
    'math': 'Spellcaster',
    'graphs': 'Thunder',
    'data structures': 'Cyberse',
    'strings': 'Beast',
    'greedy': 'Beast-Warrior',
}


def compute_target_atk(max_rating: Optional[int]) -> int:
    if max_rating is None:
        return 0
    return math.floor(max_rating * 1.25)


def compute_target_def(solved_problems: Optional[int]) -> int:
    if not solved_problems:
        return 0
    val = math.floor(math.sqrt(solved_problems) * 36.5)
    return min(val, 4000)


def map_rank_to_level(max_rank: Optional[str]) -> int:
    if not max_rank:
        return 1
    key = max_rank.lower()
    return RANK_TO_LEVEL.get(key, 1)


def map_tag_to_race(tags: Optional[List[List[Any]]]) -> str:
    # `tags` expected like [['dp', count], ['math', count], ...]
    if not tags:
        return 'Warrior'
    # find tag with largest count
    try:
        dominant = max(tags, key=lambda t: t[1])[0]  # type: ignore
    except Exception:
        dominant = tags[0][0]

    dominant = dominant.lower()
    for key in TAG_TO_RACE:
        if key in dominant:
            return TAG_TO_RACE[key]
    return 'Warrior'


def build_target_from_user(user: User) -> Dict[str, Any]:
    atk = compute_target_atk(user.max_rating)
    deff = compute_target_def(user.solved_problems)
    level = map_rank_to_level(user.max_rank)
    race = map_tag_to_race(user.tags)

    return {
        'target_atk': atk,
        'target_def': deff,
        'target_level': level,
        'target_race': race,
    }


def weighted_distance(candidate: Dict[str, Any], target: Dict[str, Any]) -> float:
    # Normalize deltas
    atk_t = max(1, target.get('target_atk', 1))
    def_t = max(1, target.get('target_def', 1))
    lvl_t = max(1, target.get('target_level', 1))

    delta_atk = (candidate.get('atk', 0) - target['target_atk']) / atk_t
    delta_def = (candidate.get('def', 0) - target['target_def']) / def_t
    delta_lvl = (candidate.get('level', 0) - target['target_level']) / 12.0

    dist = math.sqrt(0.55 * (delta_atk ** 2) + 0.25 * (delta_def ** 2) + 0.20 * (delta_lvl ** 2))
    return dist


def choose_best_card(candidates: List[Dict[str, Any]], target: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not candidates:
        return None
    best = None
    best_score = None
    for c in candidates:
        score = weighted_distance(c, target)
        if best_score is None or score < best_score or (score == best_score and c.get('id', 0) < best.get('id', 0)):
            best = c
            best_score = score
    return best
