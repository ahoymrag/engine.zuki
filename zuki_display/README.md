# Zuki Display - Full-Featured Frontend

A standalone Python web application featuring a kid-friendly 3D animated face for Zuki robot with **ALL Zuki features integrated**! Perfect for running on Raspberry Pi!

## Features

- 🤖 **3D Animated Face** - Big expressive eyes using Three.js
- 🎨 **Kid-Friendly Design** - Soft, colorful, and playful interface
- 📱 **Interactive Menu** - Control Zuki's expressions with fun buttons
- 🎭 **Multiple Expressions** - Happy, Excited, Sleepy, Surprised, Wink, and Love
- 🗣️ **Speech/TTS** - Make Zuki speak
- 🧠 **AI Brain** - Ask Zuki questions
- 📡 **Sensors** - Read sensor data
- 🎮 **Games** - Magic trick and 20 Questions
- 📒 **Notes** - Save and view notes
- 💭 **Personality** - Mood tracking and care guide
- 💬 **Chat** - Interactive chat with Zuki
- 🍓 **Raspberry Pi Ready** - Optimized for Raspberry Pi performance

## How to Run from the Repo

### Option 1: From the repo root

```bash
cd engine.zuki
cd zuki_display
pip install -r requirements.txt
python start.py
```

### Option 2: Direct path

```bash
python zuki_display/start.py
```

### Option 3: Using app.py directly

```bash
cd zuki_display
python app.py
```

Then open your browser to:
```
http://localhost:5000
```

Or if running on Raspberry Pi, access from another device:
```
http://[raspberry-pi-ip]:5000
```

## Installation

1. Make sure you're in the `engine.zuki` repository
2. Install Python dependencies:
```bash
cd zuki_display
pip install -r requirements.txt
```

Note: The app will automatically detect if Zuki modules are available. If the `Zuki` folder is in the parent directory, all features will work. Otherwise, it runs in display-only mode.

## Usage

### Expressions
- Click the colorful expression buttons to change Zuki's face
- Watch Zuki's eyes follow your mouse cursor

### Zuki Features
- **👋 Greet Zuki** - Say hello and reset the lonely timer
- **📡 Read Sensors** - Get sensor data
- **🪄 Magic Trick** - Play the number guessing game (requires terminal)
- **❓ 20 Questions** - Play the guessing game (requires terminal)
- **📒 View Notes** - See all saved notes
- **💝 Care Guide** - Learn how to take care of Zuki

### Chat
- Type messages in the chat box to talk with Zuki
- Zuki will respond using the chat brain

### Mood Tracking
- Zuki's mood is automatically checked every 30 seconds
- The face expression updates based on mood
- Greet Zuki regularly to keep them happy!

## Requirements

- Python 3.6+
- Flask and Flask-CORS (installed via requirements.txt)
- Modern web browser with WebGL support
- Zuki modules (optional - for full features)

## Full Feature List

When running from the repo with Zuki modules available, you get:

✅ **All Zuki Features:**
- Speech/Text-to-Speech
- AI Brain queries
- Motor control
- Sensor reading
- Games (Magic Trick, 20 Questions)
- Notes system
- Personality/mood system
- Chat functionality
- Care guide

## Notes

- The app runs on port 5000 by default
- It's designed to be lightweight and run smoothly on Raspberry Pi
- The 3D face uses Three.js loaded from CDN (requires internet connection)
- For offline use, you can download Three.js locally
- Games that require terminal interaction will prompt you to use the console
- All features are accessible via the web interface or API endpoints

## API Endpoints

The app provides REST API endpoints for all features:
- `GET /api/status` - Get Zuki status and mood
- `POST /api/speak` - Make Zuki speak
- `POST /api/move` - Move Zuki
- `GET /api/sense` - Read sensors
- `POST /api/ai` - Ask AI question
- `POST /api/greet` - Greet Zuki
- `GET /api/mood` - Check mood
- `GET /api/care-guide` - Get care guide
- `POST /api/note` - Add note
- `GET /api/notes` - List notes
- `POST /api/notes/clear` - Clear notes
- `POST /api/chat` - Chat with Zuki

