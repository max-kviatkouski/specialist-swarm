#!/usr/bin/env python3
"""Serve the dashboard locally and open it in a browser. Cross-platform.

Usage:  python serve.py        (Windows: py serve.py)
Or just double-click index.html — the dashboard needs no server (offline-ready).
"""
import http.server
import os
import socketserver
import threading
import webbrowser

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}/index.html")).start()
with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f"Serving the Case Console at http://localhost:{PORT}/index.html  (Ctrl+C to stop)")
    httpd.serve_forever()
