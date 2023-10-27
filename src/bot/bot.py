import json
import discord
from discord import app_commands
from colorama import Fore
from pytube import YouTube
import os
import validators
from youtube_search import YoutubeSearch

from src.functions.init import *
from src.functions.senders import *


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

    def get_video_url(prompt: str) -> str:
        result = json.loads(YoutubeSearch(prompt, max_results=1).to_json())
        return f"https://youtube.com/watch?v={result['videos'][0]['id']}"

    def download_video_audio(url: str):
        video = YouTube(url)
        audio = video.streams.filter(only_audio=True).first()
        outfile = audio.download(output_path="Temp/")

        if "audio.mp3" in listdir("Temp/"):
            os.remove("Temp/audio.mp3")

        os.rename(outfile, "Temp/audio.mp3")

    @tree.command(name="play", description="Joue la piste audio d'une vidéo YouTube.")
    async def play(interaction: discord.Interaction, search: str):
        await interaction.response.defer()

        bot_voice_channels = interaction.client.voice_clients

        if not bot_voice_channels:
            channel_to_join = interaction.user.voice.channel
            voice_client = await channel_to_join.connect()

        else:
            voice_client = bot_voice_channels[0]
            if voice_client.is_playing():
                voice_client.stop()

        if validators.url(search):
            video_url = search

        else:
            video_url = get_video_url(search)

        download_video_audio(video_url)

        voice_client.play(discord.FFmpegPCMAudio("Temp/audio.mp3", executable="ffmpeg/ffmpeg.exe"))

        await send_deferred_bot_response(interaction, f"**Playing :** {video_url}")

    bot.run(token)
