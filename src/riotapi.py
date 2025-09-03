# src/riotapi.py
import requests
from .config import RIOT_API_KEY, RIOT_REGION, MATCH_REGION

HEADERS = {"X-Riot-Token": RIOT_API_KEY}

# ---------------------------
# Synchronous Riot API calls
# ---------------------------

def riot_get(url: str):
    """Perform a synchronous GET request to the Riot API."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


# Summoner endpoints
def get_summoner_by_name(name: str):
    """Get summoner info by name."""
    url = f"https://{RIOT_REGION}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}"
    return riot_get(url)


# Match endpoints
def get_matches_by_puuid(puuid: str, count: int = 20):
    """Get recent match IDs by PUUID."""
    url = f"https://{MATCH_REGION}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}"
    return riot_get(url)


def get_match(match_id: str):
    """Get detailed match info by match ID."""
    url = f"https://{MATCH_REGION}.api.riotgames.com/tft/match/v1/matches/{match_id}"
    return riot_get(url)


# League endpoints
def get_league_entries(tier: str = "CHALLENGER", queue: str = "RANKED_TFT"):
    """
    Returns a list of entries in the specified tier.
    Tier must be one of CHALLENGER, GRANDMASTER, MASTER.
    """
    tier = tier.upper()
    platform_region = "na1"  # Change to your region if needed

    if tier == "CHALLENGER":
        url = f"https://{platform_region}.api.riotgames.com/tft/league/v1/challenger?queue={queue}"
    elif tier == "GRANDMASTER":
        url = f"https://{platform_region}.api.riotgames.com/tft/league/v1/grandmaster?queue={queue}"
    elif tier == "MASTER":
        url = f"https://{platform_region}.api.riotgames.com/tft/league/v1/master?queue={queue}"
    else:
        raise ValueError("Tier must be CHALLENGER, GRANDMASTER, or MASTER.")

    return riot_get(url)["entries"]
