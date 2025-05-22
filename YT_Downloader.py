# -------------------------------------------
# Created by MaJiX
# YouTube/Playlist to MP3 Downloader using yt-dlp
# -------------------------------------------

import yt_dlp
import os

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "MaJiXs YT Downloads")

def print_header():
    print("\n==============================")
    print("   Created By MaJiX")
    print(" YouTube MP3 Downloader")
    print("==============================\n")

def ensure_download_folder():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

def ask_overwrite(filename):
    while True:
        choice = input(f'File "{filename}" already exists. Overwrite? (y/n): ').strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("Please enter 'y' or 'n'.")

def download_audio():
    url = input("Enter the YouTube video or playlist URL: ").strip()
    ensure_download_folder()

    ydl_opts_info = {
        'quiet': True,
        'skip_download': True,
        'ignoreerrors': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)

        # Determine if playlist or single video
        entries = info.get('entries', [info])  # Playlist entries or single video as list

        for idx, video in enumerate(entries, start=1):
            if video is None:
                print(f"Skipping unavailable video #{idx} in playlist.")
                continue

            title = video.get('title', f"video_{idx}")
            ext = 'mp3'
            if 'entries' in info:
                # Playlist mode: include index in filename
                filename = f"{idx:02d} - {title}.{ext}"
            else:
                filename = f"{title}.{ext}"

            filepath = os.path.join(DOWNLOAD_FOLDER, filename)

            if os.path.exists(filepath):
                if not ask_overwrite(filename):
                    print(f"Skipping \"{filename}\"...\n")
                    continue  # skip download for this video

            ydl_opts_download = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{filename[:-4]}.%(ext)s'),  # remove .mp3, yt-dlp adds correct ext
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': False,
                'no_warnings': True,
                'ignoreerrors': True,
                'ffmpeg_location': 'ffmpeg',
                'noplaylist': True,  # Download single video only here
            }

            print(f"Downloading: {title}")
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([video['webpage_url']])

            print(f"✅ Finished: {filename}\n")

        print(f"\nAll done! Files saved in:\n{DOWNLOAD_FOLDER}\n")

    except Exception as e:
        print("❌ An error occurred:", e)

def main():
    print_header()
    try:
        while True:
            download_audio()
            again = input("Do you want to download another video or playlist? (y/n): ").strip().lower()
            if again != 'y':
                print("Goodbye!")
                break
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()

