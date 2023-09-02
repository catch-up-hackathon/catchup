import dotenv
import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from gensim.summarization import summarize

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

youtube_api_key = os.environ["YOUTUBE_API_KEY"]


def get_video_insights(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=statistics,snippet&key={youtube_api_key}"
    response = requests.get(url)

    video_data = response.json()["items"][0]

    insights = {
        "title": video_data["snippet"]["title"],
        "description": video_data["snippet"]["description"],
        "published_at": video_data["snippet"]["publishedAt"],
        "view_count": video_data["statistics"]["viewCount"],
        "like_count": video_data["statistics"]["likeCount"],
    }
    return insights


def get_video_summary(video_id):
    # Get the video transcript
    transcript = None
    
    # Try to get Korean ('ko') transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko"])
    except Exception as e:
        pass

    # If Korean transcript is not available, try English ('en') transcript
    if not transcript:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        except Exception as e:
            print(f"Could not retrieve English transcript: {e}")

    if transcript:
        text = ". ".join([entry["text"] for entry in transcript])
    else:
        print("Script를 추출할 수 없습니다.")
        text = ""
        
    # Summarize the transcript
    # summary = summarize(text)

    return text

def save_text_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)  # 디렉토리가 없는 경우 생성
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)

if __name__ == "__main__":
    video_id = os.environ["VIDEO_ID"]
    insights = get_video_insights(video_id)
    print(insights)
    summary = get_video_summary(video_id)
    print(summary)
    
    if summary:
        output_directory = "./script"  # 원하는 디렉토리 경로로 변경
        output_filename = f"{video_id}.txt"
        save_text_to_file(summary, output_directory, output_filename)
        print(f"요약된 텍스트가 '{output_directory}/{output_filename}' 파일에 저장되었습니다.")
    else:
        print("요약된 텍스트가 없으므로 파일로 저장되지 않았습니다.")
