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

    print("Transcribing audio with word timestamps...")
    result = model.transcribe(audio_path, word_timestamps=True)

    return result["segments"]

def save_srt_word_by_word(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        index = 1

        for segment in segments:
            # Each segment now contains a "words" list
            for word_info in segment.get("words", []):
                start = format_timestamp(word_info["start"])
                end = format_timestamp(word_info["end"])
                word = word_info["word"].strip()

                f.write(f"{index}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{word}\n\n")

                index += 1

def main():
    if not os.path.exists(AUDIO_FILE):
        print(f"Audio file '{AUDIO_FILE}' not found.")
        return

    segments = transcribe_audio(AUDIO_FILE)
    save_srt_word_by_word(segments, OUTPUT_FILE)

    print(f"Word-by-word subtitles saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()