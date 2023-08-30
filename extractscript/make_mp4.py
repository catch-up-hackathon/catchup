import whisper
from pytube import YouTube

video_id = 'w74dvSGcZoM'

youtube_video_url = f"https://www.youtube.com/watch?v={video_id}"
youtube_video = YouTube(youtube_video_url)
streams = youtube_video.streams.filter(only_audio=True)
stream = streams.first()
stream.download(filename=f'./audio/{video_id}.mp4')
