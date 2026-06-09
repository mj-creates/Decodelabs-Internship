import os
import yt_dlp
import whisper
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def download_audio(youtube_url):
    print("⬇️ Downloading audio...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print("✅ Audio downloaded")

def transcribe_audio():
    print("🎙️ Transcribing audio...")
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")
    print("✅ Transcription done")
    return result["text"]

def generate_reels(transcript):
    print("🤖 Generating Reels content...")
    prompt = f"""
You are a viral social media expert.

Given this video transcript, identify the 5 most engaging segments and for each one generate:
1. VIRAL HEADLINE (punchy, under 10 words)
2. CAPTION (2-3 sentences, hook + value + CTA)
3. B-ROLL DESCRIPTION (describe what visuals would appear in this reel)
4. SEGMENT QUOTE (the exact line from transcript that makes this viral)

Transcript:
{transcript}

Format your response exactly like this for each reel:
REEL 1:
Headline: ...
Caption: ...
B-Roll: ...
Quote: ...
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def save_output(content):
    with open("reels_output.txt", "w") as f:
        f.write(content)
    print("💾 Saved to reels_output.txt")

def main():
    url = input("Enter YouTube URL: ")
    download_audio(url)
    transcript = transcribe_audio()
    reels = generate_reels(transcript)
    print("\n" + reels)
    save_output(reels)

if __name__ == "__main__":
    main()