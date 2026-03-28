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

def transcribe_audio(audio_path, word_level=False):
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing audio...")
    result = model.transcribe(audio_path, word_timestamps=word_level)

    return result["segments"]

def save_srt_sentence(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

def save_srt_word_by_word(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        index = 1

        for segment in segments:
            for word_info in segment.get("words", []):
                start = format_timestamp(word_info["start"])
                end = format_timestamp(word_info["end"])
                word = word_info["word"].strip()

                f.write(f"{index}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{word}\n\n")

                index += 1

def get_user_choice():
    while True:
        choice = input("Choose subtitle mode:\n1. Sentence by sentence\n2. Word by word\nEnter 1 or 2: ").strip()
        if choice in ["1", "2"]:
            return choice
        print("Invalid input. Please enter 1 or 2.")

def main():
    if not os.path.exists(AUDIO_FILE):
        print(f"Audio file '{AUDIO_FILE}' not found.")
        return

    choice = get_user_choice()

    if choice == "1":
        segments = transcribe_audio(AUDIO_FILE, word_level=False)
        save_srt_sentence(segments, OUTPUT_FILE)
        print(f"Sentence-level subtitles saved to {OUTPUT_FILE}")
    else:
        segments = transcribe_audio(AUDIO_FILE, word_level=True)
        save_srt_word_by_word(segments, OUTPUT_FILE)
        print(f"Word-by-word subtitles saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()