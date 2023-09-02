import dotenv
import os
from pytube import YouTube
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

url = "https://www.youtube.com/shorts/viM1rOvhh_w"

def save_mp4_to_file(url, directory, video_id):
    if 'shorts' in url:
        youtube_video_url = f"https://www.youtube.com/shorts/{video_id}"
    else:
        youtube_video_url = f"https://www.youtube.com/watch?v={video_id}"
    youtube_video = YouTube(youtube_video_url)
    streams = youtube_video.streams.filter(only_audio=True)
    stream = streams.first()
    os.makedirs(directory, exist_ok=True)  # 디렉토리가 없는 경우 생성
    stream.download(filename=f"./audio/{video_id}.mp4")

if __name__ == "__main__":
    video_id = os.environ["VIDEO_ID"]
    
    output_directory = "./audio"  # 원하는 디렉토리 경로로 변경
    output_filename = f"{video_id}"
    save_mp4_to_file(url, output_directory, output_filename)
    print(f"영상이 '{output_directory}/{output_filename}' 파일에 저장되었습니다.")
