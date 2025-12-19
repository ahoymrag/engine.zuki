#!/usr/bin/env python3
"""
Simple startup script for Zuki Display
Run this to start the display server
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 Zuki Display - Starting...")
    print("=" * 50)
    print("\n📱 Open your browser to: http://localhost:8080")
    print("🌐 Or from another device: http://[this-ip]:8080")
    print("\n🛑 Press Ctrl+C to stop\n")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        print("\n\n👋 Zuki Display stopped. Goodbye!")
        sys.exit(0)

