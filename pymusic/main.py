import subprocess
import requests
from urllib.parse import quote_plus
import re
import vlc
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def banner():
    """
    Display a fancy banner for the program.
    """
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("=" * 50)
    print("🎵  WELCOME TO YOUTUBE SONG PLAYER 🎵")
    print("=" * 50)
    print(Style.RESET_ALL)


def get_audio_stream(url):
    """
    Fetch the audio URL using yt-dlp.
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "-f", "bestaudio", "--get-url", url],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"{Fore.RED}Error fetching audio stream: {result.stderr}")
            return None
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        return None


def play_audio(url):
    """
    Play the audio stream using VLC.
    """
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(url)
    media.get_mrl()
    player.set_media(media)
    player.play()
    print(f"{Fore.GREEN}🎶 Playing... Press Ctrl+C to stop. 🎶")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        player.stop()
        print(f"{Fore.YELLOW}\nStopped playback.")


def search_youtube(query):
    """
    Search YouTube and get video URLs.
    """
    search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    response = requests.get(search_url)
    video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
    if video_ids:
        return [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids]
    else:
        print(f"{Fore.RED}No results found.")
        return None


def choose_song(query):
    """
    Search YouTube and let the user select a song from the results, showing duration.
    """
    urls = search_youtube(query)
    if not urls:
        return None

    print(f"\n{Fore.MAGENTA}Search Results:")
    for i, url in enumerate(urls[:10], 1):  # Limit to the first 10 results
        try:
            yt = subprocess.run(
                ["yt-dlp", "--get-title", "--get-duration", url],
                capture_output=True,
                text=True,
            )
            output = yt.stdout.strip().split("\n")
            title = output[0] if len(output) > 0 else "Unknown Title"
            duration = output[1] if len(output) > 1 else "Unknown Duration"
            print(f"{Fore.BLUE}[{i}] {title} ({Fore.GREEN}{duration}{Fore.BLUE})")
        except Exception as e:
            print(f"{Fore.BLUE}[{i}] {url} (Error fetching title and duration)")

    try:
        choice = int(
            input(f"\n{Fore.YELLOW}Enter the number of the song you want to play: ")
        )
        if 1 <= choice <= len(urls[:10]):
            return urls[choice - 1]
        else:
            print(f"{Fore.RED}Invalid choice. Returning to main menu.\n")
            return None
    except ValueError:
        print(f"{Fore.RED}Invalid input. Returning to main menu.\n")
        return None


def main():
    while True:
        banner()
        print(f"{Fore.GREEN}1: Search and play the first result")
        print(f"{Fore.GREEN}2: Search by name and choose from a list")
        print(f"{Fore.GREEN}3: Play from a YouTube URL")
        print(f"{Fore.GREEN}4: Exit")
        print("=" * 50)

        choice = input(f"{Fore.YELLOW}Enter your choice: ").strip()

        url = None
        if choice == "1":
            query = input(f"{Fore.CYAN}Enter the song name: ").strip()
            urls = search_youtube(query)
            url = urls[0] if urls else None
        elif choice == "2":
            query = input(f"{Fore.CYAN}Enter the song name: ").strip()
            url = choose_song(query)
        elif choice == "3":
            url = input(f"{Fore.CYAN}Paste the YouTube URL: ").strip()
        elif choice == "4":
            print(f"{Fore.YELLOW}Goodbye! 🎵")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Returning to main menu.\n")
            continue

        if url:
            print(f"{Fore.GREEN}Fetching audio for: {url}")
            audio_url = get_audio_stream(url)
            if audio_url:
                play_audio(audio_url)
            else:
                print(f"{Fore.RED}Failed to fetch audio.")
        else:
            print(f"{Fore.RED}No URL found or operation canceled.\n")


if __name__ == "__main__":
    main()
