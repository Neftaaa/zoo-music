import discord
from discord import app_commands
from colorama import Fore
import json
import os
import validators
from youtube_search import YoutubeSearch

from src.functions.init import *
from src.functions.senders import *
from src.functions.downloaders import *


def run_discord_bot():
    class Client(discord.Client):
        def __init__(self) -> None:
            intents = discord.Intents.all()

            super().__init__(intents=intents)
            self.synced = False

        async def on_ready(self):
            await self.wait_until_ready()
            if not self.synced:
                await tree.sync()
                self.synced = True

            print(f'{Fore.GREEN}{bot.user}{Fore.RESET} is now running!{Fore.RESET}')

    bot = Client()
    tree = app_commands.CommandTree(bot)
    token = get_bot_token()

    def yt_search(prompt: str) -> str:
        result = json.loads(YoutubeSearch(prompt, max_results=1).to_json())
        return f"https://youtube.com/watch?v={result['videos'][0]['id']}"

    @tree.command(name="play", description="Joue la piste audio d'une vidéo YouTube.")
    async def play(interaction: discord.Interaction, search: str):
        await interaction.response.defer()

        bot_voice_channels = interaction.client.voice_clients

        if validators.url(search):
            media = detect_media(search)
            if media is None:
                await send_deferred_bot_response(interaction, f"Lien non-supporté. Les différents médias disponibles sont : `{str(get_supported_medias().keys())}`")
                return

            video_url = search
            download_audio(video_url, media)

        else:
            video_url = yt_search(search)

        if not bot_voice_channels:

            if interaction.user.voice is None:
                await send_deferred_bot_response(interaction, "Impossible de jouer la musique si vous n'êtes pas connecté(e) à un salons vocal.")
                return

            channel_to_join = interaction.user.voice.channel
            voice_client = await channel_to_join.connect()

        else:
            voice_client = bot_voice_channels[0]
            if voice_client.is_playing():
                voice_client.stop()

        yt_audio_dl(video_url)

        voice_client.play(discord.FFmpegPCMAudio("Temp/audio.mp3", executable="ffmpeg/ffmpeg.exe"))

        await send_deferred_bot_response(interaction, f"**Playing :** {video_url}")

    @tree.command(name="leave", description="Déconnecte le bot.")
    async def leave(interaction: discord.Interaction):

        if interaction.client.voice_clients is not None:
            await interaction.client.voice_clients[0].disconnect(force=True)

    bot.run(token)
