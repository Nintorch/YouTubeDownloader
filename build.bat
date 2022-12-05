@echo off
create-version-file information.yml --outfile file_version_info.txt
pyinstaller -F --windowed --add-data "images;images" ^
    --version-file="file_version_info.txt" -i "icon.ico" -n youtubedownloader main.py
del file_version_info.txt
pause