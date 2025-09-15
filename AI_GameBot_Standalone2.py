#!/usr/bin/env python3
"""
AI Game Bot - Complete Standalone Desktop Application
Includes all web features plus local game interaction capabilities
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import time
import threading
import pyautogui
import importlib
import psutil
import typing
import keyboard
import cv2
import numpy as np
import ctypes
from ctypes import wintypes
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import subprocess
from pathlib import Path
from utils.logger import Logger

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# get the .env configuration to load the openai_api key 

# check for and detect the active roblox process or open from path C:\Users\dommy\AppData\Local\Roblox\Versions\version-65664807ac1d4e85\RobloxPlayerBeta.exe

try:
    from main import GameBot
    from multi_instance_launcher import MultiInstanceLauncher
    import app  # Web interface module
except ImportError as e:
    print(f"Import error: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class StandaloneGameBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Game Bot - Complete Standalone")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')

        self.game_bot = None
        self.web_server_thread = None
        self.web_server_running = False
        self.frame_handlers["CONTINUOUS_LEARNING"] = self.handle_play
                                                   

        self.setup_ui()

    def setup_ui(self):
        """Setup the complete standalone interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🤖 AI Game Bot - Complete Standalone", 
            font=("Arial", 20, "bold"),
            bg='#2b2b2b', 
            fg='white'
        )
        title_label.pack(pady=20)

        # Status frame
        status_frame = tk.Frame(self.root, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=20, pady=10)

        self.status_label = tk.Label(
            status_frame, 
            text="Status: Ready to start", 
            font=("Arial", 12),
            bg='#2b2b2b', 
            fg='#00ff00'
        )
        self.status_label.pack()

        # Main buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2b2b2b')
        buttons_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Initialize Game Bot
        init_btn = tk.Button(
            buttons_frame,
            text="🚀 Initialize AI Game Bot",
            command=self.initialize_gamebot,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            height=2,
            width=30
        )
        init_btn.pack(pady=10)

        # Start Web Interface
        web_btn = tk.Button(
            buttons_frame,
            text="🌐 Start Web Interface",
            command=self.start_web_interface,
            font=("Arial", 12, "bold"),
            bg='#2196F3',
            fg='white',
            height=2,
            width=30
        )
        web_btn.pack(pady=10)

        # Open Web Dashboard
        dashboard_btn = tk.Button(
            buttons_frame,
            text="📊 Open Web Dashboard",
            command=self.open_dashboard,
            font=("Arial", 12, "bold"),
            bg='#FF9800',
            fg='white',
            height=2,
            width=30
        )
        dashboard_btn.pack(pady=10)

        # Multi_Instance Manager
        multi_btn = tk.Button(
            buttons_frame,
            text="🎮 Multi-Instance Manager",
            command=self.open_multi_instance,
            font=("Arial", 12, "bold"),
            bg='#9C27B0',
            fg='white',
            height=2,
            width=30
        )
        multi_btn.pack(pady=10)

        # Game Window Detection
        detect_btn = tk.Button(
            buttons_frame,
            text="🎯 Detect Game Windows",
            command=self.detect_windows,
            font=("Arial", 12, "bold"),
            bg='#E91E63',
            fg='white',
            height=2,
            width=30
        )
        detect_btn.pack(pady=10)

        # Settings and Data
        settings_btn = tk.Button(
            buttons_frame,
            text="⚙️ Settings & Data Management",
            command=self.open_settings,
            font=("Arial", 12, "bold"),
            bg='#607D8B',
            fg='white',
            height=2,
            width=30
        )
        settings_btn.pack(pady=10)

    def initialize_gamebot(self):
        """Initialize the Game Bot with all systems"""
        try:
            self.status_label.config(text="Status: Initializing AI Game Bot...", fg='#ffff00')
            self.root.update()

            self.game_bot = GameBot()

            self.status_label.config(text="Status: AI Game Bot initialized successfully!", fg='#00ff00')
            messagebox.showinfo("Success", "AI Game Bot initialized with all advanced systems!")

        except Exception as e:
            self.status_label.config(text=f"Status: Error - {str(e)}", fg='#ff0000')
            messagebox.showerror("Error", f"Failed to initialize Game Bot: {str(e)}")

    def start_web_interface(self):
        """Start the embedded web interface"""
        if self.web_server_running:
            messagebox.showinfo("Info", "Web interface is already running!")
            return

        try:
            self.status_label.config(text="Status: Starting web interface...", fg='#ffff00')
            self.root.update()

            def run_web_server():
                try:
                    app.run(host='127.0.0.1', port=5000, debug=False)
                except Exception as e:
                    print(f"Web server error: {e}")

            self.web_server_thread = threading.Thread(target=run_web_server, daemon=True)
            self.web_server_thread.start()
            self.web_server_running = True

            self.status_label.config(text="Status: Web interface running on http://127.0.0.1:5000", fg='#00ff00')
            messagebox.showinfo("Success", "Web interface started! Click 'Open Web Dashboard' to access it.")

        except Exception as e:
            self.status_label.config(text=f"Status: Web interface error - {str(e)}", fg='#ff0000')
            messagebox.showerror("Error", f"Failed to start web interface: {str(e)}")

    def open_dashboard(self):
        """Open the web dashboard in default browser"""
        try:
            webbrowser.open('http://127.0.0.1:5000')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard: {str(e)}")

    def open_multi_instance(self):
        """Open multi-instance management window"""
        try:
            launcher = MultiInstanceLauncher()
            # Create embedded multi-instance window
            multi_window = tk.Toplevel(self.root)
            multi_window.title("Multi-Instance Manager")
            multi_window.geometry("600x400")
            multi_window.configure(bg='#2b2b2b')

            # Add multi-instance controls here
            tk.Label(
                multi_window, 
                text="Multi-Instance Manager", 
                font=("Arial", 16, "bold"),
                bg='#2b2b2b', 
                fg='white'
            ).pack(pady=20)

            tk.Label(
                multi_window, 
                text="Launch and manage multiple game instances", 
                bg='#2b2b2b', 
                fg='white'
            ).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open multi-instance manager: {str(e)}")

    def detect_windows(self):
        """Detect and list game windows"""
        try:
            if not self.game_bot:
                messagebox.showwarning("Warning", "Please initialize Game Bot first!")
                return

            # Use the window detector from the game bot
            windows = self.game_bot.window_detector.detect_roblox_windows()

            window_info = tk.Toplevel(self.root)
            window_info.title("Detected Game Windows")
            window_info.geometry("500x300")
            window_info.configure(bg='#2b2b2b')

            tk.Label(
                window_info, 
                text="Detected Roblox Windows:",
                font=("Arial", 14, "bold"),
                bg='#2b2b2b', 
                fg='white'
            ).pack(pady=10)

            for i, window in enumerate(windows):
                tk.Label(
                    window_info, 
                    text=f"{i+1}. {window.get('title', 'Unknown')} (PID: {window.get('pid', 'N/A')})",
                    bg='#2b2b2b', 
                    fg='white'
                ).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect windows: {str(e)}")

    def open_settings(self):
        """Open settings and data management window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings & Data Management")
        settings_window.geometry("600x500")
        settings_window.configure(bg='#2b2b2b')

        tk.Label(
            settings_window, 
            text="Settings & Data Management", 
            font=("Arial", 16, "bold"),
            bg='#2b2b2b', 
            fg='white'
        ).pack(pady=20)

        # Data directories info
        tk.Label(
            settings_window, 
            text="Data Storage Locations:",
            font=("Arial", 12, "bold"),
            bg='#2b2b2b', 
            fg='white'
        ).pack(pady=10)

        data_dirs = ["data/", "logs/", "core/"]
        for dir_name in data_dirs:
            if os.path.exists(dir_name):
                tk.Label(
                    settings_window, 
                    text=f"✅ {dir_name} - {len(os.listdir(dir_name))} files",
                    bg='#2b2b2b', 
                    fg='#00ff00'
                ).pack(pady=2)

    def run(self):
        """Run the standalone application"""
        self.root.mainloop()


if __name__ == "__main__":
    print("🤖 Starting AI Game Bot - Complete Standalone...")

    # Check for required files
    required_files = ["main.py", "app.py"]
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        input("Press Enter to exit...")
        sys.exit(1)

    # Start the application
    try:
        standalone_app = StandaloneGameBot()
        standalone_app.run()
    except Exception as e:
        print(f"❌ Application error: {e}")
        input("Press Enter to exit...")


def _perform_deep_analysis(self):
    self.logger.info("Starting deep analysis of experience data...")
    # Example: Analyze experience logs to find common failure points
    failures = self._identify_common_failure_points()
    # Generate commands or strategies based on failures
    commands = self._generate_commands_for_failures(failures)
    # Execute commands
    for cmd in commands:
        self._execute_command(cmd)
    self.logger.info("Deep analysis and command execution completed.")


def _execute_command(self, command):
    self.logger.info(f"Executing command: {command}")
    # For example, run a script, call an API, or execute a shell command
    try:
        # Example using subprocess
        import subprocess
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.logger.info(f"Command output: {result.stdout.decode()}")
    except Exception as e:
        self.logger.error(f"Failed to execute command: {e}")

# if runninng from flask
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)