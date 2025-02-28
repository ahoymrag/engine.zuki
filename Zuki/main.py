# main.py
import motor_control
import speech
import ai_brain
import sensors
import web_server
import piano  # Import your piano module (piano.py)
import notes  # Import our notes module
import personality  

def main():
    print("\n🤖 Welcome to Zuki's Console! Type 'help' for commands.")
    
    while True:
        # 1) Check Zuki's mood each loop
        mood_message = personality.check_mood()
        if mood_message:
            print(f"\n💭 {mood_message}\n")
            # Optionally speak the mood:
            # speech.speak(mood_message)

        # 2) Get user command
        command = input("\n📝 Enter command: ").strip().lower()

        # 3) Handle commands
        if command == "exit":
            print("Shutting down Zuki...")
            break
        elif command == "help":
            print("\nAvailable Commands:")
            print("  move [direction]   - Move Zuki (forward, backward, left, right)")
            print("  speak [text]       - Make Zuki talk")
            print("  sense              - Read sensor data")
            print("  ai [question]      - Ask Zuki something")
            print("  web                - Start web server")
            print("  piano              - Launch the console piano")
            print("  note [text]        - Save a note with timestamp")
            print("  notes              - List saved notes")
            print("  clear notes        - Clear all saved notes")
            print("  hello zuki         - Greet Zuki (reset lonely timer)")
            print("  exit               - Shutdown Zuki")
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
            # Launch the console-based piano mode
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
        else:
            print("❌ Unknown command. Type 'help' for available commands.")
            speech.speak("Unknown command. Please type help for available commands.")

if __name__ == "__main__":
    main()