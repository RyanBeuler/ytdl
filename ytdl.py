##########################################################################################
#  Simple python utility to donwload youtube videos in mp4 or mp3 format
##########################################################################################

# Import required modules
import os
import sys
import re
from tqdm import tqdm
import yt_dlp as ytdl


##########################################################################################
#  Functions
##########################################################################################

# Functions for colored output
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))

# Function to validate youtube video URL of 1st parameter
def urlcheck(url):
    # Check if the url is valid
    if not re.match(r'https?://(?:www\.)?youtube.com/watch\?v=[\w-]+', url):
        prRed("Invalid youtube video url")
        sys.exit(1)
    else:
        prGreen("Youtube video url is valid")


# Function to validate file formate for 2nd parameter
def formatcheck(format):
    # Check if the format is valid
    if format not in ['mp4', 'mp3']:
        prRed("Invalid format. Please specify mp4 or mp3")
        sys.exit(1)
    else:
        prGreen("Format is valid")

# Function to create progress bar
def create_progress_bar(total_bytes):
    return tqdm(
        total=total_bytes,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc="Downloading"
    )

# Function to download video
def download_video(url, format_type):
    pbar = None
    # Function to update progress bar
    def progress_hook(d):
        nonlocal pbar
        if d['status'] == 'downloading':
            if pbar is None and d.get('total_bytes'):
                pbar = create_progress_bar(d['total_bytes'])
            if pbar:
                downloaded = d.get('downloaded_bytes', 0)
                pbar.update(downloaded - pbar.n)
        elif d['status'] == 'finished' and pbar:
            pbar.close()

    # Dictionary of format options
    format_options = {
        'mp3': {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        },
        'mp4': {
            'format': 'best'
        }
    }

    # Check if the format is supported
    if format_type not in format_options:
        print(f"Error: Format '{format_type}' not supported. Use 'mp3' or 'mp4'.")
        sys.exit(1)

    # Set youtube-dl options
    ydl_opts = {
        **format_options[format_type],
        'progress_hooks': [progress_hook],
        'outtmpl': '%(title)s.%(ext)s'
    }

    # Attempt to download the video
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        prGreen("\nDownload complete!")
    except Exception as e:
        if pbar:
            pbar.close()
        print(f"\nError: {str(e)}")
        sys.exit(1)


##########################################################################################
#  Execution starts here
##########################################################################################

if __name__ == '__main__':

    # Check to make sure the user has supplied both the url and the format as arguments to the script
    if len(sys.argv) != 3:
        prRed("Usage: python ytdl.py <youtube_video_url> <mp4/mp3>")
        sys.exit(1)
    else:
        #call function to check that the youtube url is valid
        urlcheck(sys.argv[1])
        #call function to check that the format is valid
        formatcheck(sys.argv[2])


    # Check to make sure yt-dlp python package is installed
    prCyan("Validating yt-dlp package is installed...")
    try:
        import yt_dlp
        prGreen("yt-dlp package is installed.")
    except ImportError:
        prRed("yt-dlp package is not installed. Please install it using 'pip install yt-dlp' command.")
        sys.exit(1)


    # Check to make sure ffmpeg is installed
    prCyan("Validating ffmpeg package is installed...")
    if os.system("ffmpeg -version") != 0:
        prRed("ffmpeg is not installed. Please install it from https://ffmpeg.org/download.html")
        sys.exit(1)
    else:
        prGreen("ffmpeg package is installed.")

    # Call the download_video function
    download_video(sys.argv[1], sys.argv[2])

    