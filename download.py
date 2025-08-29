import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from tqdm import tqdm  # Add this import at the top

# === Spotify API Credentials ===
CLIENT_ID = 'aa94004a0579406599d55f88aca9be76'
CLIENT_SECRET = 'f435c05f6dbb47e69a10f1903b3e6c73'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
# Ensure this matches the Redirect URI in your Spotify Developer Dashboard
SCOPE = 'playlist-read-private'

# === Create SMusic Directory ===
DOWNLOAD_DIR = "SMusic"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === Start Local Server to Handle Redirect URI ===
class SpotifyRedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/callback"):
            # Extract the authorization code from the URL
            code = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('code', None)
            if code:
                print("🔑 Code received: ", code[0])
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization successful! You can now return to the terminal.")
                self.server.code = code[0]  # Save the code for later use
            else:
                self.send_response(400)
                self.end_headers()

# === Function to Start the HTTP Server for Spotify OAuth Redirect ===
def start_local_server():
    server = HTTPServer(('localhost', 8888), SpotifyRedirectHandler)
    print("📍 Starting local server at http://localhost:8888/")
    webbrowser.open(f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}")
    server.handle_request()  # Handle a single request and then return

# === Function to Authenticate and Get Access Token ===
def authenticate():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".cache"
    ))
    print("✅ Authentication complete.")
    return sp  # Return the authenticated Spotify client

# === Get Tracks from Spotify Playlist ===
def get_playlist_tracks(sp, playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    songs = []
    offset = 0

    while True:
        results = sp.playlist_items(playlist_id, offset=offset)
        items = results.get('items', [])
        if not items:
            break
        for item in items:
            track = item.get('track')
            if not track:
                continue
            artist_names = ', '.join(artist['name'] for artist in track['artists'])
            track_name = track['name']
            song_str = f"{artist_names} - {track_name}"
            songs.append(song_str)
        offset += len(items)

    return songs

# === Download Track Using yt_dlp ===
def download_song(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,           # Suppress output
        'no_warnings': True,     # Suppress warnings
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'ffmpeg_location': r'D:\cyber learining\spotify downloader\ffmpeg-2025-05-26-git-43a69886b2-full_build\ffmpeg-2025-05-26-git-43a69886b2-full_build\bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        # Remove the print statement for cleaner output
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query}"])
    except Exception as e:
        print(f"❌ Error downloading {query}: {e}")

# === Main Script ===
if __name__ == "__main__":
    try:
        # Authenticate and get the Spotify client
        sp = authenticate()

        # Get the playlist URL from user
        url = input("🎵 Enter your Spotify playlist URL: ").strip()

        # Fetch the tracks from the playlist
        tracks = get_playlist_tracks(sp, url)
        print(f"\n📊 Total Tracks Found: {len(tracks)}\n")

        # Create a single progress bar for the total downloads
        with tqdm(total=len(tracks), desc="Downloading", unit="track", leave=True) as progress_bar:
            # Download each track using yt_dlp without individual progress bars
            for song in tracks:
                download_song(song)  # No progress bar here
                progress_bar.update(1)  # Update the total progress bar after each song download
                time.sleep(1)  # Be polite to YouTube servers

    except Exception as e:
        print(f"❌ Error: {e}")

