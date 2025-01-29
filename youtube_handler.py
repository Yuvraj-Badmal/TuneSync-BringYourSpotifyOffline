import os
import re
import yt_dlp
from config import DOWNLOADS_FOLDER

# Global flag to track stop/skip
stop_flag = False
skip_flag = False

def sanitize_filename(filename):
    """ Removes invalid characters and ensures the filename ends only once with .mp3 """
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove invalid characters
    if filename.lower().endswith(".mp3"):  # Prevent double .mp3
        filename = filename[:-4]  # Remove existing .mp3 to avoid duplication
    return filename + ".mp3"  # Append a single .mp3

def search_youtube(song_name, artist):
    """ Searches for the best YouTube video matching the song. """
    query = f"{song_name} {artist} official music video"
    ydl_opts = {"default_search": "ytsearch1", "quiet": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=False)
        return info_dict["entries"][0]["webpage_url"] if "entries" in info_dict else None

def download_audio(youtube_url, song_name):
    """ Downloads and converts YouTube audio to MP3, ensuring the correct filename. """
    global stop_flag, skip_flag

    filename = sanitize_filename(song_name)
    filepath = os.path.join(DOWNLOADS_FOLDER, filename)

    if os.path.exists(filepath):
        print(f"✅ Skipping: {filename} (Already downloaded)")
        return filepath  # Skip if already downloaded

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOADS_FOLDER, "%(title)s.%(ext)s"),  # Ensures yt-dlp does not append another .mp3
        "ffmpeg_location": "C:/ffmpeg/bin",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": False,
        "progress_hooks": [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(youtube_url, download=True)
            downloaded_filepath = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")

            #  Ensure the final saved file has a single .mp3 extension
            final_filepath = os.path.join(DOWNLOADS_FOLDER, sanitize_filename(os.path.basename(downloaded_filepath)))

            #  Rename file if it still contains double .mp3
            if downloaded_filepath != final_filepath:
                os.rename(downloaded_filepath, final_filepath)

            return final_filepath
        except yt_dlp.utils.DownloadError:
            print("Download interrupted.")

    return None

def progress_hook(d):
    """ Stops or skips the download immediately when triggered. """
    global stop_flag, skip_flag
    if stop_flag or skip_flag:
        raise yt_dlp.utils.DownloadError("Download stopped by user.")
