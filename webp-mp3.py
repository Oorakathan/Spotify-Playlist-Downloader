import os
import subprocess

input_folder = "SMusic"
output_folder = "MP3s"
os.makedirs(output_folder, exist_ok=True)

ffmpeg_path = r'D:\cyber learining\spotify downloader\ffmpeg-2025-05-26-git-43a69886b2-full_build\ffmpeg-2025-05-26-git-43a69886b2-full_build\bin\ffmpeg.exe'

for filename in os.listdir(input_folder):
    if filename.endswith(".webm"):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".mp3"
        output_path = os.path.join(output_folder, output_filename)

        print(f"🎧 Converting: {filename} → {output_filename}")
        result = subprocess.run([
            ffmpeg_path,
            "-i", input_path,
            "-q:a", "0",
            "-map", "a",
            output_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"✅ Done: {output_filename}")
        else:
            print(f"❌ Error converting {filename}")
            print(result.stderr.decode())

print("\n🎵 All conversions complete.")
