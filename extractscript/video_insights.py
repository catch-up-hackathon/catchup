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
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko"])
    text = ". ".join([entry["text"] for entry in transcript])
    # Summarize the transcript
    # summary = summarize(text)

    return text


if __name__ == "__main__":
    video_id = "kpeQCq4mIXs"
    insights = get_video_insights(video_id)
    print(insights)
    summary = get_video_summary(video_id)
    print(summary)
