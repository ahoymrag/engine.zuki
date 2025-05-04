from flask import Flask, render_template, request, jsonify
from chat_brain import EnhancedChatBrain
import webbrowser
import threading
import time

app = Flask(__name__)
chat_brains = {}  # Store chat brains for different sessions

def launch_browser():
    """Wait for server to start, then launch browser"""
    time.sleep(1.5)  # Give the server time to start
    webbrowser.open('http://127.0.0.1:5001')

def start_chat_server():
    """Start the Flask server and launch browser"""
    threading.Thread(target=launch_browser).start()
    app.run(debug=False, port=5001)  # Changed debug to False for production

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id', 'default')
    message = data.get('message', '')
    
    # Get or create chat brain for this session
    if session_id not in chat_brains:
        chat_brains[session_id] = EnhancedChatBrain()
    
    # Get response
    response = chat_brains[session_id].process_input(message)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    start_chat_server() 