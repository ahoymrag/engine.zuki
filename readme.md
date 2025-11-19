# Zuki - Your Personal Robot

## Introduction
Zuki is a Raspberry Pi-powered personal robot with a command-line interface (CLI) and an optional graphical UI that displays emotions and speech bubbles. The project is designed to be modular, with placeholder components that can be replaced with real implementations over time.

## Raspberry Pi Offline Quickstart (Tiny Chat UI)
1. Package the repo (on your dev machine):
   - macOS/Linux: `bash package.sh`
2. Copy `engine.zuki.zip` to your Raspberry Pi and unzip:
   - `unzip engine.zuki.zip -d engine.zuki && cd engine.zuki`
3. Run local setup (offline-friendly):
   - `bash Zuki/install.sh`
   - Optional TTS: `sudo apt-get install -y espeak-ng`
   - If Tk is missing: `sudo apt-get install -y python3-tk`
4. Start the tiny chat UI:
   - `python3 pi_start.py`
5. Tip: enable “Speak” in the UI to have Zuki read replies aloud.


## Tagline::::
Zuki, a multi-functional interactive AI assistant with a graphical UI, speech, AI, and even a playable piano! 

## Core Structure

zuki/
│── main.py
│── zuki_ui.py
│── piano.py
│── speech.py
│── motor_control.py  # (if it exists)
│── sensors.py  # (if it exists)
│── ai_brain.py  # (if it exists)
│── web_server.py  # (if it exists)
│── install.sh  # (optional setup script)
│── requirements.txt  # ✅ ADD THIS FILE HERE!
│── README.md  # (optional: instructions for setup and usage)
│── assets/  # (optional: if you have images, sounds, etc.)
└── venv/  # (optional, but usually not committed)




## Targeted Features
- Command-line interface (CLI) for controlling Zuki.
- Web API for remote control.
- Speech recognition and text-to-speech (TTS) capabilities.
- Motor control for movement.
- Sensor integration for obstacle detection.
- Visual UI using Pygame to display Zuki's emotions.

---

# Using and Playing with Zuki

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
python -m venv .zuki
source .zuki/bin/activate  # Mac/Linux



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

