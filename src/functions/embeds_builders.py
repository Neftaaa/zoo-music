import discord
from datetime import datetime


def convert_server_data_dict(server_data: dict) -> dict:
    motd = server_data["motd"]
    clean_motd = motd["clean"]
    if len(clean_motd) == 1:
        usable_motd = clean_motd[0]
    else:
        usable_motd = f"{clean_motd[0]}\n{clean_motd[1]}"

    players_info = server_data["players"]
    online_player_count = players_info["online"]
    max_player_count = players_info["max"]

    version = server_data["version"]
    return {"final_motd": usable_motd, "online_player_count": online_player_count,
            "max_player_count": max_player_count, "version": version}


def build_error_embed(lang: str) -> discord.embeds.Embed:

    error_embed = discord.Embed(title="Error", color=discord.Color.red())
    return error_embed
