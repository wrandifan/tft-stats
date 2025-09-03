import discord
from discord.ext import commands
from .riotapi import get_summoner_by_name, get_matches_by_puuid, get_league_entries, get_matches_by_puuid, get_match
from .stats import aggregate_champion_stats
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True   # 👈 allow reading message text
bot = commands.Bot(command_prefix="!", intents=intents)

CHAMPION_MAP = {
    "jinx": "TFT15_Jinx",
    "ahri": "TFT15_Ahri",
    "aatrox": "TFT15_Aatrox",
    # Add more champions as needed
}

# src/bot.py
@bot.command()
async def champion(ctx, champ_name: str, tier: str = None):
    """
    Example:
    !champion Jinx           -> fetches all tiers
    !champion Jinx 3         -> fetches only 3-star Jinx
    !champion Jinx 2,3       -> fetches 2-star and 3-star Jinx
    """
    champ_name = champ_name.lower()  # make search case-insensitive

    # Parse tiers
    if tier:
        try:
            tiers = [int(t.strip()) for t in tier.split(",")]
        except ValueError:
            await ctx.send("Tier must be numbers separated by commas, e.g., 2,3")
            return
    else:
        tiers = None  # None = all tiers

    try:
        # Get top 50 challenger players
        challenger_players = await get_league_entries("CHALLENGER")
        challenger_players = challenger_players[:50]

        # For collecting stats
        champ_stats = []

        for player in challenger_players:
            puuid = player["summonerId"]
            match_ids = await get_matches_by_puuid(puuid, count=20)

            # Fetch match details concurrently
            match_details_tasks = [get_match_details(mid) for mid in match_ids]
            matches = await asyncio.gather(*match_details_tasks, return_exceptions=True)

            for match in matches:
                if isinstance(match, Exception):
                    continue  # skip failed requests

                for participant in match["info"]["participants"]:
                    for unit in participant.get("units", []):
                        # Check if champion name matches
                        unit_id = unit.get("character_id", "").lower()
                        unit_tier = unit.get("tier", 0)
                        if champ_name in unit_id and (tiers is None or unit_tier in tiers):
                            champ_stats.append({
                                "puuid": participant["puuid"][:8],  # shorten for readability
                                "placement": participant["placement"],
                                "tier": unit_tier,
                                "items": ", ".join(unit.get("itemNames", []))
                            })

        # Send results
        if champ_stats:
            # Build table header
            msg = f"Stats for {champ_name.capitalize()}"
            if tiers:
                msg += " " + ",".join(map(str, tiers)) + "-star"
            msg += ":\n"
            msg += "```\n"
            msg += f"{'Player':<10} | {'Placement':<9} | {'Tier':<4} | Items\n"
            msg += "-" * 60 + "\n"
            for stat in champ_stats:
                msg += f"{stat['puuid']:<10} | {stat['placement']:<9} | {stat['tier']:<4} | {stat['items']}\n"
            msg += "```"
            await ctx.send(msg[:2000])  # Discord message limit
        else:
            await ctx.send(f"No {champ_name.capitalize()} units found in recent matches.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
