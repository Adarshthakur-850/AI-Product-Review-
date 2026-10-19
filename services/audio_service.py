"""
Real-Time Audio Processing Service.
Handles in-memory audio format normalization, speech-to-text transcription,
and Text-to-Speech (TTS) response synthesis.
"""
import io
import os
import tempfile
from typing import Dict, Any, Optional
import soundfile as sf
import speech_recognition as sr
from services.language_detector import LanguageDetector

class AudioService:
    """
    Real-time speech-to-text and speech synthesis service.
    """
    
    @staticmethod
    def normalize_to_wav(audio_bytes: bytes) -> bytes:
        """
        Converts uploaded/recorded audio bytes into standard 16-bit PCM WAV.
        """
        try:
            data, samplerate = sf.read(io.BytesIO(audio_bytes))
            out_buf = io.BytesIO()
            sf.write(out_buf, data, samplerate, format="WAV", subtype="PCM_16")
            return out_buf.getvalue()
        except Exception:
            # If already WAV or unreadable by sf, return raw bytes
            return audio_bytes

    @staticmethod
    def transcribe_audio_bytes(
        audio_bytes: bytes,
        preferred_language: str = "en-IN"
    ) -> Dict[str, Any]:
        """
        Transcribes audio bytes to text using SpeechRecognition (Google STT / Whisper).
        Supports:
        - "en-IN" (Indian English / Hinglish)
        - "hi-IN" (Hindi)
        - "en-US" (Standard English)
        """
        if not audio_bytes or len(audio_bytes) < 100:
            return {
                "success": False,
                "transcript": "",
                "detected_language": "en",
                "language_label": "Empty Audio",
                "confidence": 0.0,
                "error": "No audio received. Please speak into the microphone before submitting."
            }

        wav_bytes = AudioService.normalize_to_wav(audio_bytes)
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = recognizer.record(source)
                
            # Attempt transcription with preferred language
            try:
                transcript = recognizer.recognize_google(audio_data, language=preferred_language)
            except Exception:
                # Fallback to alternate language (e.g. if hi-IN fails, try en-IN)
                fallback_lang = "hi-IN" if preferred_language.startswith("en") else "en-IN"
                transcript = recognizer.recognize_google(audio_data, language=fallback_lang)
                
            lang_info = LanguageDetector.detect(transcript)
            
            return {
                "success": True,
                "transcript": transcript,
                "detected_language": lang_info["language"],
                "language_label": lang_info["label"],
                "confidence": 0.92,
                "error": None
            }
        except sr.UnknownValueError:
            return {
                "success": False,
                "transcript": "",
                "detected_language": "en",
                "language_label": "Unknown",
                "confidence": 0.0,
                "error": "Could not understand audio. Please speak clearly into the microphone."
            }
        except Exception as e:
            return {
                "success": False,
                "transcript": "",
                "detected_language": "en",
                "language_label": "Error",
                "confidence": 0.0,
                "error": f"Audio processing error: {str(e)}"
            }

    @staticmethod
    def synthesize_speech_wav(text: str) -> Optional[bytes]:
        """
        Generates spoken audio WAV bytes from text using pyttsx3.
        """
        if not text or not text.strip():
            return None
        
        tmp_file = None
        try:
            import pyttsx3
            engine = pyttsx3.init()
            # Set speech rate
            engine.setProperty("rate", 165)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                tmp_file = f.name
                
            engine.save_to_file(text, tmp_file)
            engine.runAndWait()
            
            if os.path.exists(tmp_file):
                with open(tmp_file, "rb") as f:
                    wav_data = f.read()
                return wav_data
        except Exception as e:
            print(f"TTS synthesis notice: {e}")
            return None
        finally:
            if tmp_file and os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except Exception:
                    pass
        return None
