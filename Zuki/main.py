# main.py

import motor_control
import speech
import ai_brain
import sensors
import web_server
import piano  # piano.py
import notes  # notes.py
import personality  # personality.py
import zuki_games  # Our new file with the 2 games
import time
import os
import random
from chat_brain import EnhancedChatBrain

def show_help():
    """Display available commands with animations."""
    os.system('clear')  # Clear the terminal for a clean display
    print("\n✨ Welcome to Zuki's Command Center! ✨\n")
    time.sleep(0.5)

    commands = [
        "move [direction]   - Move Zuki (forward, backward, left, right)",
        "speak [text]       - Make Zuki talk",
        "sense              - Read sensor data",
        "ai [question]      - Ask Zuki something",
        "web                - Start web server",
        "piano              - Launch the console piano",
        "note [text]        - Save a note (timestamped)",
        "notes              - List saved notes",
        "clear notes        - Clear all saved notes",
        "hello zuki         - Greet Zuki (reset lonely timer)",
        "care guide         - Show how to take care of Zuki",
        "exit               - Shutdown Zuki",
        "zuki magic         - Play the number guessing magic trick!",
        "20 questions       - Play a yes/no guess game!",
        "chat               - Enter chat mode with Zuki"
    ]

    print("🛠️  Available Commands:\n")
    for command in commands:
        print(f"  ➡️  {command}")
        time.sleep(0.2)  # Add a slight delay for animation effect

    print("\n💡 Tip: Type 'exit' to shut down Zuki anytime.")
    print("🎉 Have fun exploring Zuki's features!\n")

def main():
    print("\n🤖 Welcome to Zuki's Console! Type 'help' for commands.")
    
    while True:
        # 1) Check Zuki's mood each loop
        mood_message = personality.check_mood()
        if mood_message:
            print(f"\n💭 {mood_message}\n")
            # Optional: Have Zuki speak the mood
            # speech.speak(mood_message)

        # 2) Get user command
        command = input("\n📝 Enter command: ").strip().lower()

        # 3) Handle commands
        if command == "exit":
            print("Shutting down Zuki...")
            # speech.speak("Shutting down Zuki...")
            break
        
        elif command == "help":
            show_help()

        elif command.startswith("move "):
            direction = command.split(" ")[1]
            motor_control.move(direction)
            speech.speak(f"Moving {direction}")

        elif command.startswith("speak "):
            text = command[6:]
            speech.speak(text)

        elif command == "sense":
            sensors.read_sensors()
            speech.speak("Reading sensor data.")

        elif command.startswith("ai "):
            query = command[3:]
            response = ai_brain.process_query(query)
            print("🧠 Zuki:", response)
            speech.speak(f"Here is the answer: {response}")

        elif command == "web":
            web_server.start()
            speech.speak("Starting the web server.")

        elif command == "piano":
            piano.run_console_piano()

        elif command.startswith("note "):
            note_text = command[5:]
            response = notes.add_note(note_text)
            print(response)

        elif command == "notes":
            response = notes.list_notes()
            print("📒 Your Notes:\n", response)

        elif command == "clear notes":
            response = notes.clear_notes()
            print(response)

        elif command == "hello zuki":
            response = personality.greet_zuki()
            print(response)
            speech.speak(response)

        elif command == "care guide":
            guide = personality.show_care_guide()
            print(guide)
            # Optionally speak just a summary line:
            # speech.speak("Here's how to take care of me!")

        elif command == "zuki magic":
            # Start the guess-the-number trick
            zuki_games.magic_trick()

        elif command == "20 questions":
            # Start the yes/no questions game
            zuki_games.twenty_questions()

        elif command == "chat":
            chat_mode()

        else:
            print("❌ Unknown command. Type 'help' for available commands.")
            speech.speak("Unknown command. Please type help for available commands.")

def chat_mode():
    chat_brain = EnhancedChatBrain()
    print("\n🗣️ Entering chat mode with Zuki (type 'exit chat' to leave)")
    print("Zuki: Hello! I'm excited to chat with you! What's on your mind?")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "exit chat":
            print("Zuki: Goodbye! Back to command mode!")
            break
        
        response = chat_brain.process_input(user_input)
        print(f"Zuki: {response}")

if __name__ == "__main__":
    main()