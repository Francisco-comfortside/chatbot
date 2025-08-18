# voice_module.py
import io
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_STT_MODEL, OPENAI_TTS_MODEL

class VoiceHandler:
    def __init__(
            self, api_key=OPENAI_API_KEY, 
            stt_model=OPENAI_STT_MODEL, 
            tts_model=OPENAI_TTS_MODEL, 
            voice="alloy"
        ):
        """
        Handles Speech-to-Text (STT) and Text-to-Speech (TTS) using OpenAI.
        """
        self.client = OpenAI(api_key=api_key)
        self.stt_model = stt_model
        self.tts_model = tts_model
        self.voice = voice


    def transcribe_audio(self, audio_bytes: bytes, file_ext="wav") -> str:
        """
        Convert audio bytes to text using in-memory buffer (no temp file).
        """
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = f"temp.{file_ext}"  # required so API knows the format

        transcript = self.client.audio.transcriptions.create(
            model=self.stt_model,
            file=audio_file
        )
        return transcript.text

    def text_to_speech(self, text: str, format="mp3") -> bytes:
        """
        Convert text to audio (text-to-speech).
        Returns audio bytes in-memory.
        """
        response = self.client.audio.speech.create(
            model=self.tts_model,
            voice=self.voice,
            input=text
        )
        return response.read()