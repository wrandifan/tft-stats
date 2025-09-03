from .bot import bot
from .config import DISCORD_TOKEN

if __name__ == "__main__":
    assert DISCORD_TOKEN is not None, "DISCORD_TOKEN is missing from .env"
    bot.run(DISCORD_TOKEN)