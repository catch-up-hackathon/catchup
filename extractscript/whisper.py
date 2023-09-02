# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import dotenv
import os
import openai

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

openai.api_key = os.environ["OPENAI_API_KEY"]
video_id = os.environ["VIDEO_ID"]

audio_file= open(f"./audio/{video_id}.mp4", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)

with open(f"./script/{video_id}.txt", "w", encoding="utf-8") as txt:
    txt.write(transcript["text"])
