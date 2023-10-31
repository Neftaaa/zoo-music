from pytube import YouTube
from os import remove, listdir, rename


def get_supported_medias() -> dict:
    return {
        "YouTube": "https://www.youtube.com/watch?v="
    }


def detect_media(url: str) -> str | None:
    supported_medias = get_supported_medias()
    for media in supported_medias.items():
        if url.startswith(media[1]):
            return media[0]

    return


def yt_audio_dl(url: str):
    video = YouTube(url)
    audio = video.streams.filter(only_audio=True).first()
    outfile = audio.download(output_path="Temp/")

    if "audio.mp3" in listdir("Temp/"):
        remove("Temp/audio.mp3")

    rename(outfile, "Temp/audio.mp3")


def download_audio(url: str, media: str):
    if media == "YouTube":
        yt_audio_dl(url)
