import atexit
import http.client
import os
import threading

import ffmpeg
import pytube.exceptions
from pytube import YouTube, Stream
from pytube.exceptions import PytubeError

from urllib.request import urlretrieve
from urllib.error import HTTPError

files_to_delete = []


# replace this function with proper function
def output(string):
    print(string)


# replace this function with proper function
def _error(string):
    print("Error: " + string)


def _clean():
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)


atexit.register(_clean)


class DownloaderException(Exception):
    reason = ""

    def __init__(self, reason):
        self.reason = reason
        _error(reason)

    def __repr__(self):
        return self.reason


def stream_download(stream: Stream, audio_stream: Stream, filepath, thread=True):
    def _download_thread():
        try:
            stream.download(os.path.dirname(filepath), os.path.splitext(os.path.basename(filepath))[0] + "temp.mp4")

            if audio_stream:
                audio_stream.download(os.path.dirname(filepath),
                                      os.path.splitext(os.path.basename(filepath))[0] + "audio.mp4")

                input_video = ffmpeg.input(os.path.splitext(os.path.basename(filepath))[0] + "temp.mp4")
                input_audio = ffmpeg.input(os.path.splitext(os.path.basename(filepath))[0] + "audio.mp4")

                ffmpeg.output(input_video, input_audio, os.path.basename(filepath)).run(quiet=True)

                os.remove(os.path.splitext(filepath)[0] + "temp.mp4")
                os.remove(os.path.splitext(filepath)[0] + "audio.mp4")
            else:
                ffmpeg.input(os.path.splitext(filepath)[0] + "temp.mp4").output(filepath).run(quiet=True)
                os.remove(os.path.splitext(filepath)[0] + "temp.mp4")
            output("Download successful")
        except PytubeError:
            output("Error while downloading")

    if thread:
        threading.Thread(target=_download_thread).start()
    else:
        _download_thread()


# deprecated
def download(url, filepath, with_audio=True, resolution="720p"):
    """
    Download the video with specified type and resolution
    :param url: url for video that needs to be downloaded
    :param filepath: downloaded file path
    :param with_audio: sets whether the video should have audio or not, ignored for audio
    :param resolution: video resolution, ignored for audio
    :return: None
    """

    def _download_thread():
        files_to_delete.append(os.path.splitext(filepath)[0] + ".mp4")

        output("Searching for available streams")
        streams = YouTube(url).streams
        stream: Stream
        video_types = [".avi", ".mp4", ".mov", ".mkv"]
        audio_types = [".mp3", ".ogg", ".wav"]

        if os.path.splitext(filepath)[1] in video_types:
            stream = streams.filter(resolution=resolution, only_video=not with_audio).first()
        elif os.path.splitext(filepath)[1] in audio_types:
            stream = streams.filter(only_audio=True).first()
        else:
            raise DownloaderException(f"Unknown file format \"{os.path.splitext(filepath)[1]}\"")

        if not stream:
            raise DownloaderException("Requested video cannot be downloaded")

        stream_download(stream, filepath, thread=False)

    threading.Thread(target=_download_thread).start()


def _format_length(length):
    secs = length % 60
    minutes = (length // 60) % 60
    hours = (length // 3600) % 24

    if hours:
        res = f"%d:%02d:%02d" % (hours, minutes, secs)
    else:
        res = f"%d:%02d" % (minutes, secs)
    return res


def get_video_details(url):
    try:
        yt = YouTube(url)

        resolutions = []
        videos = []
        audios = []

        streams = []

        # Try to get the stream list
        while True:
            try:
                streams = yt.streams
                break
            except http.client.HTTPException:
                continue

        # Get the information about all needed video and audio streams
        stream: Stream
        for stream in streams.filter(only_audio=True):
            audios.append([stream, stream.abr, stream.filesize])
        for stream in streams:
            if stream.includes_video_track and stream.resolution and stream.resolution not in resolutions:
                resolutions.append(stream.resolution)
                try:
                    size = stream.filesize
                except KeyError:  # 'content-length' missing, for some reason
                    continue
                except HTTPError:  # "Service Unavailable" ?
                    continue
                if not stream.includes_audio_track:
                    size = ((stream.bitrate+audios[0][0].bitrate)//8) * yt.length
                videos.append([stream, stream.resolution, size])

        # Download thumbnail
        urlretrieve(yt.thumbnail_url, "thumbnail.png")

        return {
            "title": yt.title,
            "length": _format_length(yt.length),
            "video": sorted(videos, key=lambda x: int(x[1][:-1]), reverse=True),
            "audio": sorted(audios, key=lambda x: int(x[1][:-4]), reverse=True),
            "thumbnail": "thumbnail.png"
        }
    except pytube.exceptions.RegexMatchError:
        return None


# print(get_video_details("https://www.youtube.com/watch?v=m0UC1SbNLyY"))

if __name__ == "__main__":
    download("https://www.youtube.com/watch?v=TiodJKq92WY", "ImGood.mp3")
