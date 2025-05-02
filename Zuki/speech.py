import subprocess

def speak(text):
    """Use espeak to convert text to speech."""
    try:
        subprocess.run(["espeak", text], check=True)
    except FileNotFoundError:
        print("Error: 'espeak' is not installed. Please install it using 'sudo apt install espeak'.")
    except Exception as e:
        print(f"Error while trying to speak: {e}")

# Usage
speak("Hello, I am Zuki!")
