# Zuki - Your Personal Robot

## Introduction
Zuki is a Raspberry Pi-powered personal robot with a command-line interface (CLI) and an optional graphical UI that displays emotions and speech bubbles. The project is designed to be modular, with placeholder components that can be replaced with real implementations over time.

## Features
- Command-line interface (CLI) for controlling Zuki.
- Web API for remote control.
- Speech recognition and text-to-speech (TTS) capabilities.
- Motor control for movement.
- Sensor integration for obstacle detection.
- Visual UI using Pygame to display Zuki's emotions.

---

## Installation
### Step 1: Clone the Repository
```bash
cd ~/Documents
mkdir Zuki
cd Zuki
git clone https://github.com/yourusername/zuki.git .
```

### Step 2: Set Up a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# OR
.venv\Scripts\Activate    # Windows (PowerShell)
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running Zuki

### Option 1: Run Zuki in CLI Mode
To start Zuki’s command-line interface, run:
```bash
python main.py
```
This will open a terminal-based interface where you can type commands like:
```
📝 Enter command: move forward
🚗 (Placeholder) Moving forward...
```

### Option 2: Run Zuki with Visual UI
To start Zuki’s facial expressions and speech bubbles:
```bash
python zuki_ui.py
```

### Option 3: Start Both CLI and UI Together
Create and run the script:
#### Mac/Linux:
```bash
chmod +x zuki.sh
./zuki.sh
```
#### Windows:
```bat
zuki.bat
```

This will launch both the CLI and the UI in separate windows.

---

## Web Server for Remote Control
To start the Flask web server:
```bash
python web_server.py
```
Then visit:
```
http://localhost:5000
```
You can send commands via:
- **Move Zuki:** `http://localhost:5000/move?direction=forward`
- **Make Zuki Speak:** Use Postman or run:
```bash
curl -X POST http://localhost:5000/speak -H "Content-Type: application/json" -d '{"text":"Hello!"}'
```

---

## Available Commands
Inside the CLI (`main.py`), you can use the following:
```
help         - Show available commands
move [dir]   - Move Zuki (forward, backward, left, right)
speak [text] - Make Zuki talk
sense        - Read sensor data
ai [query]   - Ask Zuki a question
web          - Start the web server
exit         - Shutdown Zuki
```

---

## Troubleshooting
#### Virtual Environment Issues
If you get a `ModuleNotFoundError`, activate the virtual environment:
```bash
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\Activate    # Windows
```

#### Port Already in Use (Web Server Issues)
Kill any process using port 5000:
```bash
kill $(lsof -t -i:5000)  # Mac/Linux
taskkill /F /PID <PID>   # Windows
```

---

## Next Steps
- Replace placeholder functions with real implementations.
- Improve speech recognition and AI response system.
- Enhance Zuki's UI with more animations and expressions.

🚀 **Enjoy building Zuki!**

