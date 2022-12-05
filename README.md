# YoutubeDownloader
A GUI program that allows anyone to download a video from YouTube with different formats and resolutions.

Dependencies:
- wxPython
- pytube
- ffmpeg-python and FFmpeg installed

# Usage
1) Copy a YouTube video URL.
2) Click either "Download" or "Paste Link" button and wait a couple of minutes.
3) Choose a format: video and audio or audio only.
4) (Optional) Choose a format: .mp4, .avi, .mov, .mkv for video and audio or .ogg, .mp3, .wav for audio only.
5) Choose a resolution (video and audio) or a bitrate (audio only).
6) Select an output path.
7) Click "Download".

# Installation and running from source code
1) Install all dependencies above.
2) Download FFmpeg and place it in the same folder as "main.py".

# Installation and running from release
1) Download the .exe file from Release section.
2) Download FFmpeg and place it in the same folder as the .exe file.

# Building an .exe file from source code
1) Install pyinstaller and [pyinstaller-versionfile](https://pypi.org/project/pyinstaller-versionfile).
2) Run "build.bat". "build" and "dist" folder will appear, the "dist" folder will contain a "youtubedownloader.exe" executable file (don't forget to include FFmpeg with the file to run it).
