import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from tqdm import tqdm
import concurrent.futures

# === Spotify API Credentials ===
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret_key'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'playlist-read-private'

# === Create SMusic Directory ===
DOWNLOAD_DIR = "SMusic"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class SpotifyRedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/callback"):
            code = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('code', None)
            if code:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization complete. You may close this window.")
                self.server.code = code[0]
            else:
                self.send_response(400)
                self.end_headers()

def start_local_server():
    server = HTTPServer(('localhost', 8888), SpotifyRedirectHandler)
    server.handle_request()

def authenticate():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".cache"
    ))
    return sp

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

class QuietLogger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def download_song(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'logger': QuietLogger(),
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'ffmpeg_location': r'D:\cyber learining\spotify downloader\ffmpeg-2025-05-26-git-43a69886b2-full_build\ffmpeg-2025-05-26-git-43a69886b2-full_build\bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query}"])
    except:
        pass  # Silently ignore errors


if __name__ == "__main__":
    try:
        sp = authenticate()
        url = input("🎵 Enter your Spotify playlist URL: ").strip()
        tracks = get_playlist_tracks(sp, url)

        with tqdm(total=len(tracks), desc="Downloading", unit="track", leave=True) as progress_bar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(download_song, song) for song in tracks]
                for future in concurrent.futures.as_completed(futures):
                    progress_bar.update(1)
                    time.sleep(1)

    except:
        pass  # Silently handle all errors
