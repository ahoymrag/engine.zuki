import motor_control
import speech
import ai_brain
import sensors
import web_server

def main():
    print("\n🤖 Welcome to Zuki's Console! Type 'help' for commands.")
    
    while True:
        command = input("\n📝 Enter command: ").strip().lower()

        if command == "exit":
            print("Shutting down Zuki...")
            break
        elif command == "help":
            print("\nAvailable Commands:")
            print("  move [direction] - Move Zuki (forward, backward, left, right)")
            print("  speak [text] - Make Zuki talk")
            print("  sense - Read sensor data")
            print("  ai [question] - Ask Zuki something")
            print("  web - Start web server")
            print("  exit - Shutdown Zuki")
        elif command.startswith("move "):
            direction = command.split(" ")[1]
            motor_control.move(direction)
        elif command.startswith("speak "):
            text = command[6:]  # Extracts everything after "speak "
            speech.speak(text)
        elif command == "sense":
            sensors.read_sensors()
        elif command.startswith("ai "):
            query = command[3:]  # Extracts everything after "ai "
            response = ai_brain.process_query(query)
            print("🧠 Zuki:", response)
        elif command == "web":
            web_server.start()
        else:
            print("❌ Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()
