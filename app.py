#!/usr/bin/env python3
"""
Web Application for AI Game Bot - NO FLASK VERSION
Provides a web interface without Flask dependencies using Python's built-in HTTP server
"""

import json
import logging
import os
from datetime import datetime
import base64
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import threading

def create_app(game_bot):
    """Create web application without Flask dependencies"""
    
    class GameBotWebServer:
        def __init__(self, game_bot):
            self.game_bot = game_bot
            # Get session secret from environment with production fallback
            session_secret = os.environ.get('SESSION_SECRET')
            if not session_secret:
                session_secret = 'game_bot_secret_key_2024_development'
                self.logger.warning("Using development session secret. Set SESSION_SECRET environment variable for production.")
            
            self.config = {
                'SECRET_KEY': session_secret,
                'GAME_BOT': game_bot
            }
            self.logger = logging.getLogger(__name__)
        
        def run(self, host='0.0.0.0', port=5000, debug=False):
            """Start the web server using Python's built-in HTTP server"""
            self.logger.info(f"🚀 Starting AI Game Bot web server on {host}:{port}")
            self.logger.info(f"📊 Session secret configured: {'✅' if self.config['SECRET_KEY'] else '❌'}")
            self.logger.info(f"🤖 Game bot initialized: {'✅' if self.game_bot else '❌'}")
            
            # Create custom request handler
            class GameBotRequestHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    self.game_bot = game_bot
                    super().__init__(*args, **kwargs)
                
                def do_GET(self):
                    if self.path == '/':
                        self.serve_index()
                    elif self.path == '/multi_instance_launcher':
                        self.serve_multi_instance_launcher()
                    elif self.path == '/api/status':
                        self.serve_status()
                    elif self.path == '/api/macros':
                        self.serve_macros()
                    elif self.path == '/api/instances/list':
                        self.serve_instances_list()
                    elif self.path == '/api/mutex/status':
                        self.serve_mutex_status()
                    elif self.path == '/api/sync/status':
                        self.serve_sync_status()
                    elif self.path.startswith('/static/'):
                        self.serve_static()
                    else:
                        self.send_error(404)
                
                def serve_index(self):
                    """Serve the main dashboard"""
                    try:
                        with open('templates/index.html', 'r') as f:
                            content = f.read()
                            # Replace Flask template functions with static content
                            content = content.replace("{{ url_for('static', filename='style.css') }}", "/static/style.css")
                            content = content.replace("{{ url_for('static', filename='script.js') }}", "/static/script.js")
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(content.encode())
                    except Exception as e:
                        self.send_error(500, str(e))
                
                def serve_status(self):
                    """Serve bot status API"""
                    try:
                        status = {
                            'timestamp': datetime.now().isoformat(),
                            'vision_active': self.game_bot.vision_system.is_active(),
                            'automation_active': self.game_bot.automation_engine.is_active(),
                            'learning_stats': self.game_bot.learning_system.get_stats(),
                            'knowledge_count': self.game_bot.knowledge_manager.get_knowledge_count(),
                            'macro_count': len(self.game_bot.macro_system.list_macros()),
                            'screen_capture': None,
                            'last_command': getattr(self.game_bot.command_processor, 'last_command', 'None'),
                            'last_result': getattr(self.game_bot.command_processor, 'last_result', 'None')
                        }
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(status).encode())
                    except Exception as e:
                        self.send_error(500, str(e))
                
                def serve_macros(self):
                    """Serve macros API"""
                    try:
                        macros = self.game_bot.macro_system.list_macros()
                        response = {'macros': macros}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode())
                    except Exception as e:
                        self.send_error(500, str(e))
                
                def serve_multi_instance_launcher(self):
                    """Serve the multi-instance launcher page"""
                    try:
                        with open('templates/multi_instance_launcher.html', 'r') as f:
                            content = f.read()
                            # Replace Flask template functions with static content
                            content = content.replace("{{ url_for('static', filename='style.css') }}", "/static/style.css")
                            content = content.replace("{{ url_for('static', filename='script.js') }}", "/static/script.js")
                            content = content.replace("{{ url_for('static', filename='multi_instance_launcher.js') }}", "/static/multi_instance_launcher.js")
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(content.encode())
                    except Exception as e:
                        self.send_error(500, str(e))
                
                def serve_instances_list(self):
                    """Serve instances list API"""
                    try:
                        instances = []
                        if hasattr(self.game_bot, 'multi_instance_launcher'):
                            instances = self.game_bot.multi_instance_launcher.get_instance_list()
                        
                        response = {
                            'success': True,
                            'instances': instances,
                            'count': len(instances)
                        }
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode())
                    except Exception as e:
                        self.send_error(500, str(e))
                
                def serve_mutex_status(self):
                    """Serve mutex status API"""
                    try:
                        mutex_status = {
                            'success': True,
                            'active': False,
                            'methods_available': ['registry', 'process', 'file'],
                            'current_method': 'registry',
                            'bypassed_count': 0
                        }
                        
                        if hasattr(self.game_bot, 'multi_instance_launcher'):
                            mutex_status = self.game_bot.multi_instance_launcher.get_mutex_status()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(mutex_status).encode())
                    except Exception as e:
                        self.send_error(500, str(e))
                
                def serve_sync_status(self):
                    """Serve sync status API"""
                    try:
                        sync_status = {
                            'success': True,
                            'active': False,
                            'synchronized_instances': 0,
                            'sync_commands': [],
                            'last_sync': None
                        }
                        
                        if hasattr(self.game_bot, 'multi_instance_launcher'):
                            sync_status = self.game_bot.multi_instance_launcher.get_sync_status()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(sync_status).encode())
                    except Exception as e:
                        self.send_error(500, str(e))
                
                def serve_static(self):
                    """Serve static files"""
                    try:
                        file_path = self.path[1:]  # Remove leading slash
                        with open(file_path, 'rb') as f:
                            content = f.read()
                        
                        # Determine content type
                        if file_path.endswith('.css'):
                            content_type = 'text/css'
                        elif file_path.endswith('.js'):
                            content_type = 'application/javascript'
                        else:
                            content_type = 'text/plain'
                        
                        self.send_response(200)
                        self.send_header('Content-type', content_type)
                        self.end_headers()
                        self.wfile.write(content)
                    except Exception as e:
                        self.send_error(404, str(e))
            
            # Start server with improved error handling and deployment readiness
            try:
                server = HTTPServer((host, port), GameBotRequestHandler)
                self.logger.info(f"✅ AI Game Bot web server ready on http://{host}:{port}")
                self.logger.info(f"🌐 Deployment-ready (no Flask dependencies)")
                self.logger.info(f"📱 Web interface accessible at port {port}")
                
                # Signal that server is ready for deployment health checks
                print(f"SERVER_READY: AI Game Bot listening on {host}:{port}")
                
                server.serve_forever()
            except KeyboardInterrupt:
                self.logger.info("Server stopped by user")
            except Exception as e:
                self.logger.error(f"❌ Server error: {e}")
                raise
    
    return GameBotWebServer(game_bot)