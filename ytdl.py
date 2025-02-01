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


# Custom progress hook function for tqdm progress bar
def progress_hook(d):
    if d['status'] == 'downloading':
        # We update the progress bar by the number of bytes downloaded
        downloaded = d['downloaded_bytes']
        pbar.update(downloaded - pbar.n)  # Update progress
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')

# Function to download video
def download_video(url, format_choice):
    global pbar  # Access global progress bar

    # Set the options for yt-dlp
    if format_choice == "mp3":
        ydl_opts = {
            'format': 'bestaudio',  # Download best audio
            'extractaudio': True,         # Extract audio
            'audioformat': 'mp3',         # Convert to mp3
            'outtmpl': '%(title)s.%(ext)s',  # Set output file name
            'progress_hooks': [progress_hook],  # Progress hook to update tqdm
        }
    else:
        ydl_opts = {
            'format': 'mp4',  # Download best video and audio
            'outtmpl': '%(title)s.%(ext)s',  # Set output file name
            'progress_hooks': [progress_hook],  # Progress hook to update tqdm
        }

    # Create the tqdm progress bar, with total set to 1 (this will change dynamically)
    pbar = tqdm(total=1, unit='B', unit_scale=True, desc="Downloading")

    # Create yt-dlp instance and start the download
    with ytdl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])  # Start the download
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            pbar.close()  # Close the progress bar when done


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

    