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

def save_srt_extended_sentences(segments, output_path):
    """
    Karaoke-style: words are revealed one by one within each sentence.
    Each subtitle entry shows all words spoken so far in the sentence,
    starting exactly when that word is pronounced.

    Example for "How true it was":
      Entry 1: "How"           → starts when 'How' is spoken
      Entry 2: "How true"      → starts when 'true' is spoken
      Entry 3: "How true it"   → starts when 'it' is spoken
      Entry 4: "How true it was" → starts when 'was' is spoken, ends at sentence end
    """
    with open(output_path, "w", encoding="utf-8") as f:
        index = 1
        for segment in segments:
            words = segment.get("words", [])
            if not words:
                # Fallback: no word timestamps available, write full sentence
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()
                f.write(f"{index}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
                index += 1
                continue

            sentence_end = format_timestamp(segment["end"])

            for i, word_info in enumerate(words):
                word_start = format_timestamp(word_info["start"])

                # Each entry ends when the NEXT word begins, or at sentence end
                if i + 1 < len(words):
                    word_end = format_timestamp(words[i + 1]["start"])
                else:
                    word_end = sentence_end

                # Accumulate all words up to and including the current word
                accumulated_text = " ".join(
                    w["word"].strip() for w in words[: i + 1]
                )

                f.write(f"{index}\n")
                f.write(f"{word_start} --> {word_end}\n")
                f.write(f"{accumulated_text}\n\n")
                index += 1

def get_user_choice():
    while True:
        print("\nChoose subtitle mode:")
        print("  1. Sentence by sentence")
        print("  2. Word by word")
        print("  3. Extended sentences (words revealed as spoken, within each sentence)")
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")

def main():
    if not os.path.exists(AUDIO_FILE):
        print(f"Audio file '{AUDIO_FILE}' not found.")
        return

    choice = get_user_choice()

    if choice == "1":
        segments = transcribe_audio(AUDIO_FILE, word_level=False)
        save_srt_sentence(segments, OUTPUT_FILE)
        print(f"Sentence-level subtitles saved to {OUTPUT_FILE}")

    elif choice == "2":
        segments = transcribe_audio(AUDIO_FILE, word_level=True)
        save_srt_word_by_word(segments, OUTPUT_FILE)
        print(f"Word-by-word subtitles saved to {OUTPUT_FILE}")

    else:
        segments = transcribe_audio(AUDIO_FILE, word_level=True)
        save_srt_extended_sentences(segments, OUTPUT_FILE)
        print(f"Extended sentence subtitles saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()