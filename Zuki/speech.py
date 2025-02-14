import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    # Optionally, adjust rate, volume, or voice properties:
    engine.setProperty('rate', 150)  # Speed percent (lower is slower)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    engine.say(text)
    engine.runAndWait()

# Usage
speak("Hello, I am Zuki!")
