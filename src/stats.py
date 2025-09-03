from collections import defaultdict
from .riotapi import get_match

def aggregate_champion_stats(match_ids: list[str]):
    champ_stats = defaultdict(lambda: {"games": 0, "wins": 0, "top4": 0})

    for match_id in match_ids:
        match = get_match(match_id)
        for p in match["info"]["participants"]:
            placement = p["placement"]

            for unit in p["units"]:
                champ = unit["character_id"]
                champ_stats[champ]["games"] += 1
                if placement == 1:
                    champ_stats[champ]["wins"] += 1
                if placement <= 4:
                    champ_stats[champ]["top4"] += 1

    return champ_stats
