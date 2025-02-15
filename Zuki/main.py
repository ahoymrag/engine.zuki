import motor_control
import speech
import ai_brain
import sensors
import web_server
import piano  # Import your piano module (piano.py)

def main():
    print("\n🤖 Welcome to Zuki's Console! Type 'help' for commands.")
    
    while True:
        command = input("\n📝 Enter command: ").strip().lower()

        if command == "exit":
            print("Shutting down Zuki...")
            speech.speak("Shutting down Zuki...")
            break
        elif command == "help":
            print("\nAvailable Commands:")
            print("  move [direction]  - Move Zuki (forward, backward, left, right)")
            print("  speak [text]      - Make Zuki talk")
            print("  sense             - Read sensor data")
            print("  ai [question]     - Ask Zuki something")
            print("  web               - Start web server")
            print("  piano             - Launch the console piano")
            print("  exit              - Shutdown Zuki")
            speech.speak("Here are the available commands.")
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
            # Launch the console-based piano mode.
            piano.run_console_piano()
        else:
            print("❌ Unknown command. Type 'help' for available commands.")
            speech.speak("Unknown command. Please type help for available commands.")

if __name__ == "__main__":
    main()
