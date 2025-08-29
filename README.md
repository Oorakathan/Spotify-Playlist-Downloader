# Spotify Playlist Downloader

## Overview
This project is a **Spotify Playlist Downloader** script.  
It downloads songs from a Spotify playlist using the playlist link you provide.  
The songs are first saved in `.webp` format and can be converted to `.mp3` format using the included conversion script.

---

## Requirements
- Python 3.8+
- [Spotify Developer Account](https://developer.spotify.com/)
- [FFmpeg](https://ffmpeg.org/) (extract the downloaded FFmpeg ZIP into the same project directory)

---

## Setup

### 1. Spotify Developer Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/)
2. Click the burger menu -> Dashboard
3. Create a new app:
   * App name: anything you like
   * Website: ```http://localhost```
   * Redirect URL: ```http://127.0.0.1:8888/callback```
   * API/SDK: Choose Web API
4. Save the app.
5. Open the app and copy Client ID and Client Secret.
6. Paste them into the script where required

### 2. Virtual Environment
Open CMD in the project folder and run:
```python -m venv venv```
Activate the virtual environment
```.\venv\Scripts\activate```
Install Dependencies
```pip install -r requirements.txt```

### 3. Usage
Run the downloader script:
```python download.py```
Run-Time Instructions
* Once the program starts, paste your Spotify playlist link
* While pasting, remove everything after ```?``` in the link
* After entering, it will redirect you to a login page
* Log in to your Spotify account, Click agree, and close the window.
* You have successfully authorized your server
* Your download will now start (it may take some time based on you internet connectivity and CPU).
* For faster downloads, you can use ```prallel_download.py```.
