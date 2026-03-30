#!/usr/bin/env python3
"""
Duet Server — serves static files + proxies Calley API requests.
Runs on port 8787.

Static files: serves from the script's directory
Proxy: /calley-proxy/* → https://ex-api.getcalley.com/api/*
"""

import http.server
import json
import os
import urllib.request
import urllib.error
import urllib.parse

PORT = 8787
CALLEY_BASE = "https://ex-api.getcalley.com/api"
WEBROOT = os.path.dirname(os.path.abspath(__file__))

class DuetHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBROOT, **kwargs)

    def do_GET(self):
        if self.path.startswith('/calley-proxy/'):
            self._proxy_calley('GET')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/calley-proxy/'):
            self._proxy_calley('POST')
        else:
            self.send_error(405, 'POST only supported for /calley-proxy/')

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._add_cors_headers()
        self.end_headers()

    def _add_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, authToken')

    def _proxy_calley(self, method):
        """Forward request to Calley API"""
        # Build target URL: /calley-proxy/CallingLists → /api/CallingLists
        api_path = self.path[len('/calley-proxy/'):]
        target_url = f"{CALLEY_BASE}/{api_path}"

        # Read auth token from request header
        auth_token = self.headers.get('authToken', '')

        # Build headers for Calley
        headers = {
            'authToken': auth_token,
            'Content-Type': 'application/json'
        }

        # Read body for POST
        body = None
        if method == 'POST':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)

        try:
            req = urllib.request.Request(
                target_url,
                data=body,
                headers=headers,
                method=method
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self._add_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp_body)

        except urllib.error.HTTPError as e:
            error_body = e.read() if e.fp else b'{}'
            self.send_response(e.code)
            self._add_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_body)

        except Exception as e:
            self.send_response(502)
            self._add_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def log_message(self, format, *args):
        """Quieter logging — only log proxy requests and errors"""
        msg = format % args
        if '/calley-proxy/' in msg or '404' in msg or '500' in msg:
            super().log_message(format, *args)

if __name__ == '__main__':
    os.chdir(WEBROOT)
    with http.server.HTTPServer(('', PORT), DuetHandler) as httpd:
        print(f"Duet server running on http://localhost:{PORT}")
        print(f"Serving files from: {WEBROOT}")
        print(f"Calley proxy: /calley-proxy/* → {CALLEY_BASE}/*")
        httpd.serve_forever()
