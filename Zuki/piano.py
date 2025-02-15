# piano.py using pynput instead of keyboard
from pynput import keyboard
import numpy as np
import pygame
import time
import sys

# Initialize the Pygame mixer (audio only, no window)
sample_rate = 44100
pygame.mixer.pre_init(sample_rate, -16, 1, 512)
pygame.mixer.init()

# Define key frequency mappings (same as before)
white_keys = {
    'a': 261.63, 's': 293.66, 'd': 329.63,
    'f': 349.23, 'g': 392.00, 'h': 440.00,
    'j': 493.88, 'k': 523.25, 'l': 587.33,
    ';': 659.25
}
black_keys = {
    'q': 277.18, 'w': 311.13, 'e': 369.99,
    'r': 415.30, 't': 466.16, 'y': 554.37,
    'u': 622.25, 'i': 739.99, 'o': 830.61,
    'p': 932.33
}

def generate_sine_wave(frequency, duration, sample_rate=44100, volume=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = volume * np.sin(2 * np.pi * frequency * t)
    waveform = (waveform * 32767).astype(np.int16)
    return waveform

def play_note(frequency, duration=0.3):
    wave = generate_sine_wave(frequency, duration, sample_rate)
    sound = pygame.sndarray.make_sound(wave)
    sound.play()
    time.sleep(duration)

def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = None

    if k == '1':
        print("Shutdown triggered.")
        pygame.mixer.quit()
        # Stop listener by returning False
        return False
    elif k in white_keys:
        freq = white_keys[k]
        print(f"White key '{k}' pressed: {freq} Hz")
        play_note(freq)
    elif k in black_keys:
        freq = black_keys[k]
        print(f"Black key '{k}' pressed: {freq} Hz")
        play_note(freq)

def run_console_piano():
    print("Console piano mode activated.")
    print("Use keys [a s d f g h j k l ;] for white keys.")
    print("Use keys [q w e r t y u i o p] for black keys.")
    print("Press '1' to exit piano mode.")
    # Create and start the listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    run_console_piano()
