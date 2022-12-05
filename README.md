# YoutubeDownloader
A GUI program that allows anyone to download a video from YouTube with different formats and resolutions.

Dependencies:
- wxPython
- pytube
- ffmpeg-python and FFmpeg installed

# Installation and running from source code
1) Install all dependencies above.
2) Download FFmpeg and place it in the same folder as "main.py".

# Installation and running from release
1) Download and unpack the .zip file.
2) Download FFmpeg and place it in the same folder as "youtubedownloader.exe".

# Building an .exe file from source code
1) Install pyinstaller and [pyinstaller-versionfile](https://pypi.org/project/pyinstaller-versionfile).
2) Run "build.bat". "build" and "dist" folder will appear, the "dist" folder will contain a "youtubedownloader.exe" executable file (don't forget to include FFmpeg with the file to run it).
