import subprocess

def run_console_piano():
    """A simple console piano using espeak."""
    print("🎹 Welcome to Zuki's Console Piano!")
    print("Press keys (a-g) to play notes, or 'q' to quit.")

    while True:
        note = input("Enter a note (a-g) or 'q' to quit: ").strip().lower()

        if note == 'q':
            print("Exiting the piano. Goodbye!")
            break
        elif note in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            try:
                subprocess.run(["espeak", f"Note {note}"], check=True)
            except FileNotFoundError:
                print("Error: 'espeak' is not installed. Please install it using 'sudo apt install espeak'.")
            except Exception as e:
                print(f"Error while trying to play the note: {e}")
        else:
            print("Invalid input. Please enter a note (a-g) or 'q' to quit.")

if __name__ == "__main__":
    run_console_piano()
