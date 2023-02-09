from pytube import YouTube
import subprocess
import os

def download_video(url):
    yt = YouTube(url)
    videos = yt.streams
    
    audio = videos.filter(mime_type='audio/mp4').order_by('abr').desc().first()

    original_filename = audio.default_filename

    print(original_filename)

    audio_path = "audio.mp4"
    audio.download(filename=audio_path)
    
    video = videos.filter(mime_type='video/mp4',progressive=False, file_extension='mp4').order_by('resolution').desc().first()
    print("Highest resolution available non progressive video: ", video.resolution)
    video_path = "video.mp4"
    video.download(filename=video_path)
    
    join_audio_video(video_path, audio_path, original_filename)

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

# delete the audio file
os.remove("audio.mp4")
# delete the video file
os.remove("video.mp4")






