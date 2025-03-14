import os
from gtts import gTTS
from pydub import AudioSegment


def text_to_speech(input_text_file, output_audio_file, language="en", slow=False):
    """
    Convert text from a file into speech and save it as a .wav file.

    Args:
        input_text_file (str): Path to the text file.
        output_audio_file (str): Path to save the .wav file.
        language (str): Language code for TTS (default: "en" for English).
        slow (bool): Whether to speak slower (default: False).
    """
    # Read text from file
    with open(input_text_file, "r", encoding="utf-8") as file:
        text = file.read().strip()

    if not text:
        print("⚠ Error: The input text file is empty!")
        return

    # Convert text to speech (gTTS)
    tts = gTTS(text=text, lang=language, slow=slow)

    # Save as temporary MP3 file
    temp_mp3 = "temp_audio.mp3"
    tts.save(temp_mp3)

    # Convert MP3 to WAV using pydub
    audio = AudioSegment.from_mp3(temp_mp3)
    audio.export(output_audio_file, format="wav")

    # Cleanup temp file
    os.remove(temp_mp3)

    print(f"🎙️ Audio saved successfully as: {output_audio_file}")


# Example Usage
if __name__ == "__main__":
    input_text = "input_text.txt"  # Replace with your text file path
    output_wav = "output_speech.wav"
    text_to_speech(input_text, output_wav)
