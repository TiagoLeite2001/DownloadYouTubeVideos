
from pytube import YouTube
import subprocess
import os

def deleteFile(path):
    os.remove(path)

def download_video(url):
    audio_path = "audio.mp4"
    video_path = "video.mp4"

    yt = YouTube(url)
    videos = yt.streams

    audio = videos.filter(mime_type='audio/mp4').order_by('abr').desc().first()

    original_filename = audio.default_filename

    video_non_progressive = videos.filter(mime_type='video/mp4',progressive=False, file_extension='mp4').order_by('resolution').desc().first()
    video_progressive = videos.filter(mime_type='video/mp4',progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    print(original_filename)

    if(video_progressive.resolution == video_non_progressive.resolution):
        print("\nHighest resolution available: ", video_progressive.resolution)
        video_progressive.download()

    else:

        print("\n(Default/Fatest) 0 - Highest resolution available (progressive video): ", video_progressive.resolution)
        print("(Slowest) 1  - Highest resolution available (non progressive video): ", video_non_progressive.resolution)


        choice = input("Choose desired resolution: \n")

        if(choice == 1):

            video_non_progressive.download(filename=video_path)
            audio.download(filename=audio_path)

            join_audio_video(video_path, audio_path, original_filename)

            deleteFile(video_path)
            deleteFile(audio_path)

        else:
            video_progressive.download()



def join_audio_video(video_file, audio_file, output_file):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    subprocess.run(command)


url = input("Enter the URL of the video you want to download: ")
download_video(url)
print("Video was downloaded sucessfully!")








