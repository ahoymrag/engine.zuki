#!/usr/bin/env python3
"""
Zuki Display - Standalone Python Frontend with Full Zuki Features
A kid-friendly 3D animated face display for Zuki robot
Integrates all Zuki features: speech, AI, games, notes, personality, etc.
Can run standalone on Raspberry Pi
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os
import threading
import time

# Add parent Zuki directory to path to import Zuki modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
zuki_dir = os.path.join(parent_dir, 'Zuki')
if os.path.exists(zuki_dir):
    sys.path.insert(0, zuki_dir)
    
    # Import Zuki modules
    try:
        import speech
        import ai_brain
        import sensors
        import motor_control
        import notes
        import personality
        import zuki_games
        import piano
        from chat_brain import EnhancedChatBrain
        ZUKI_MODULES_AVAILABLE = True
    except ImportError as e:
        print(f"Warning: Some Zuki modules not available: {e}")
        ZUKI_MODULES_AVAILABLE = False
else:
    ZUKI_MODULES_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls

# Global chat brain instance
chat_brain = None
if ZUKI_MODULES_AVAILABLE:
    try:
        chat_brain = EnhancedChatBrain()
    except:
        pass

@app.route('/')
def index():
    """Main page with 3D animated Zuki face"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """API endpoint for status"""
    mood = 'happy'
    mood_message = None
    
    if ZUKI_MODULES_AVAILABLE:
        try:
            mood_message = personality.check_mood()
            if mood_message:
                if 'sad' in mood_message.lower():
                    mood = 'sad'
                elif 'lonely' in mood_message.lower():
                    mood = 'lonely'
        except:
            pass
    
    return jsonify({
        'status': 'online',
        'name': 'Zuki',
        'mood': mood,
        'mood_message': mood_message,
        'modules_available': ZUKI_MODULES_AVAILABLE
    })

@app.route('/api/speak', methods=['POST'])
def api_speak():
    """Make Zuki speak text"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Speech module not available'})
    
    try:
        speech.speak(text)
        return jsonify({'success': True, 'message': f'Zuki said: {text}'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/move', methods=['POST'])
def api_move():
    """Move Zuki"""
    data = request.get_json()
    direction = data.get('direction', '')
    
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Motor control not available'})
    
    try:
        motor_control.move(direction)
        speech.speak(f"Moving {direction}")
        return jsonify({'success': True, 'message': f'Moving {direction}'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/sense', methods=['GET'])
def api_sense():
    """Read sensor data"""
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Sensors not available'})
    
    try:
        result = sensors.read_sensors()
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/ai', methods=['POST'])
def api_ai():
    """Ask Zuki a question"""
    data = request.get_json()
    query = data.get('query', '')
    
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'AI brain not available'})
    
    try:
        response = ai_brain.process_query(query)
        speech.speak(f"Here is the answer: {response}")
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/greet', methods=['POST'])
def api_greet():
    """Greet Zuki"""
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Personality module not available'})
    
    try:
        response = personality.greet_zuki()
        speech.speak(response)
        return jsonify({'success': True, 'message': response})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/mood', methods=['GET'])
def api_mood():
    """Check Zuki's mood"""
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'mood': 'unknown'})
    
    try:
        mood_message = personality.check_mood()
        mood = 'happy'
        if mood_message:
            if 'sad' in mood_message.lower():
                mood = 'sad'
            elif 'lonely' in mood_message.lower():
                mood = 'lonely'
        return jsonify({'success': True, 'mood': mood, 'message': mood_message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/care-guide', methods=['GET'])
def api_care_guide():
    """Get care guide"""
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Personality module not available'})
    
    try:
        guide = personality.show_care_guide()
        return jsonify({'success': True, 'guide': guide})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/note', methods=['POST'])
def api_add_note():
    """Add a note"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Notes module not available'})
    
    try:
        response = notes.add_note(text)
        return jsonify({'success': True, 'message': response})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/notes', methods=['GET'])
def api_list_notes():
    """List all notes"""
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Notes module not available'})
    
    try:
        response = notes.list_notes()
        return jsonify({'success': True, 'notes': response})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/notes/clear', methods=['POST'])
def api_clear_notes():
    """Clear all notes"""
    if not ZUKI_MODULES_AVAILABLE:
        return jsonify({'success': False, 'message': 'Notes module not available'})
    
    try:
        response = notes.clear_notes()
        return jsonify({'success': True, 'message': response})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat with Zuki"""
    data = request.get_json()
    message = data.get('message', '')
    
    if not ZUKI_MODULES_AVAILABLE or chat_brain is None:
        return jsonify({'success': False, 'message': 'Chat brain not available'})
    
    try:
        response = chat_brain.process_input(message)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 Starting Zuki Display with Full Features...")
    print("=" * 60)
    
    if ZUKI_MODULES_AVAILABLE:
        print("✅ Zuki modules loaded successfully!")
    else:
        print("⚠️  Zuki modules not found - running in display-only mode")
        print("   (Place zuki_display folder inside engine.zuki repo)")
    
    print("\n📱 Open your browser to: http://localhost:5000")
    print("🌐 Or from another device: http://[this-ip]:5000")
    print("\n🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)

