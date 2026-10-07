"""Prototype speech service; the supplied string is a simulated transcript."""


class SpeechService:
    def transcribe(self, audio_input: str) -> str:
        if not isinstance(audio_input, str) or not audio_input.strip():
            raise ValueError("Provide nonempty transcript text for simulated voice input.")
        return audio_input.strip()
