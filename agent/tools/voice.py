try:
    import speech_recognition as sr
    import pyttsx3
    import threading
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

def listen_voice() -> str:
    if not VOICE_AVAILABLE:
        return "⚠️ Voice input is only available on desktop app."
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Bol raha hoon... (5 seconds)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="en-IN")
            return text
        except sr.WaitTimeoutError:
            return "⚠️ Koi awaaz nahi aayi."
        except sr.UnknownValueError:
            return "⚠️ Samajh nahi aaya, dobara bolo."
        except Exception as e:
            return f"Voice error: {str(e)}"

def speak_text(text: str) -> str:
    if not VOICE_AVAILABLE:
        return "⚠️ Voice output is only available on desktop app."
    def _speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak).start()
    return f"🔊 Speaking: {text[:100]}..."

LISTEN_TOOL = {
    "type": "function",
    "function": {
        "name": "listen_voice",
        "description": "Listen to user's voice input via microphone.",
        "parameters": {"type": "object", "properties": {}}
    }
}

SPEAK_TOOL = {
    "type": "function",
    "function": {
        "name": "speak_text",
        "description": "Speak out the response using text-to-speech.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to speak"}
            },
            "required": ["text"]
        }
    }
}