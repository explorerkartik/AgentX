import speech_recognition as sr
import pyttsx3
import threading

def listen_voice() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Bol raha hoon... (5 seconds)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="en-IN")
            print(f"✅ Suna: {text}")
            return text
        except sr.WaitTimeoutError:
            return "⚠️ Koi awaaz nahi aayi."
        except sr.UnknownValueError:
            return "⚠️ Samajh nahi aaya, dobara bolo."
        except Exception as e:
            return f"Voice error: {str(e)}"

def speak_text(text: str) -> str:
    def _speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=_speak)
    thread.start()
    return f"🔊 Bol raha hoon: {text[:100]}..."

LISTEN_TOOL = {
    "type": "function",
    "function": {
        "name": "listen_voice",
        "description": "Listen to user's voice input via microphone and convert to text.",
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
                "text": {"type": "string", "description": "Text to speak aloud"}
            },
            "required": ["text"]
        }
    }
}