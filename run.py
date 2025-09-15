#!/usr/bin/env python3
"""
Deployment runner for AI Game Bot
Handles both web and desktop modes with proper environment setup
"""

import os
import sys
import argparse

# Set environment variables for deployment
# Ensure SESSION_SECRET is available from production secrets or use fallback
if 'SESSION_SECRET' not in os.environ:
    os.environ['SESSION_SECRET'] = 'game_bot_secret_key_2024_production'

def main():
    parser = argparse.ArgumentParser(description='AI Game Bot Deployment Runner')
    parser.add_argument('--web', action='store_true', help='Run web interface')
    parser.add_argument('--desktop', action='store_true', help='Run desktop app')
    parser.add_argument('--port', type=int, default=5000, help='Port for web interface')
    
    args = parser.parse_args()
    
    if args.web:
        # Import and run web interface
        from main import GameBot
        from app import create_app
        
        # Create bot instance
        game_bot = GameBot()
        
        # Create and run web server (Python HTTP server, no Flask)
        app = create_app(game_bot)
        app.run(host='0.0.0.0', port=args.port, debug=False)
        
    elif args.desktop:
        # Run desktop application
        import subprocess
        subprocess.run([sys.executable, 'native_desktop_app.py'])
        
    else:
        # Default to desktop mode
        import subprocess
        subprocess.run([sys.executable, 'native_desktop_app.py'])

if __name__ == '__main__':
    main()