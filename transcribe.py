import whisper
import os

AUDIO_FILE = "audio.mp3"
OUTPUT_FILE = "subtitles.srt"

def format_timestamp(seconds):
    millisec = int(seconds * 1000)
    hours = millisec // 3600000
    minutes = (millisec % 3600000) // 60000
    seconds = (millisec % 60000) // 1000
    milliseconds = millisec % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def transcribe_audio(audio_path):
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing audio...")
    result = model.transcribe(audio_path)

    return result["segments"]

def save_srt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

def main():
    if not os.path.exists(AUDIO_FILE):
        print(f"Audio file '{AUDIO_FILE}' not found.")
        return

    segments = transcribe_audio(AUDIO_FILE)
    save_srt(segments, OUTPUT_FILE)

    print(f"Subtitles saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()