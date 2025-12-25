"""
Simple HTTP Server to run InfoDemics
Just double-click this file or run: python3 start_server.py
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = Path(__file__).parent.parent  # Point to project root

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

def start_server():
    print("=" * 70)
    print("🦠 InfoDemics - Starting Web Server")
    print("=" * 70)
    print(f"\nServer directory: {DIRECTORY}")
    print(f"Server URL: http://localhost:{PORT}")
    print(f"\nOpening InfoDemics.html in your browser...")
    print("\n" + "=" * 70)
    print("INSTRUCTIONS:")
    print("=" * 70)
    print("1. Your browser will open automatically")
    print("2. Use the controls on the left to adjust parameters")
    print("3. Click '▶️ Run Simulation' to start")
    print("4. Watch the network and charts update!")
    print("\nTo stop the server: Press Ctrl+C")
    print("=" * 70 + "\n")
    
    # Start server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        # Open browser
        webbrowser.open(f"http://localhost:{PORT}/InfoDemics.html")
        
        print(f"✅ Server running at http://localhost:{PORT}")
        print(f"✅ Browser opened to InfoDemics.html\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print("🛑 Server stopped. Thank you for using InfoDemics!")
            print("=" * 70)

if __name__ == "__main__":
    start_server()
