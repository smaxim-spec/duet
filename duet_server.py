#!/usr/bin/env python3
"""
Duet Server — serves static files + proxies Calley API + Google Calendar API.
Runs on port 8787.

Static files: serves from the script's directory
Proxy: /calley-proxy/* → https://ex-api.getcalley.com/api/*
Calendar: /calendar/busy?start=YYYY-MM-DD&days=5
          /calendar/create (POST with JSON body)
"""

import http.server
import json
import os
import urllib.request
import urllib.error
import urllib.parse
import traceback

PORT = 8787
CALLEY_BASE = "https://ex-api.getcalley.com/api"
WEBROOT = os.path.dirname(os.path.abspath(__file__))

# Add script dir to path so we can import calendar_api
import sys
sys.path.insert(0, WEBROOT)

class DuetHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBROOT, **kwargs)

    def do_GET(self):
        if self.path.startswith('/calley-proxy/'):
            self._proxy_calley('GET')
        elif self.path.startswith('/calendar/busy'):
            self._calendar_busy()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/calley-proxy/'):
            self._proxy_calley('POST')
        elif self.path.startswith('/calendar/create'):
            self._calendar_create()
        else:
            self.send_error(405, 'POST only supported for /calley-proxy/ and /calendar/')

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._add_cors_headers()
        self.end_headers()

    def _add_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, authToken')

    def _send_json(self, code, data):
        self.send_response(code)
        self._add_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # ── Calendar endpoints ──

    def _calendar_busy(self):
        """GET /calendar/busy?start=YYYY-MM-DD&days=5"""
        try:
            from calendar_api import get_busy_times
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            start = params.get('start', [None])[0]
            days = int(params.get('days', [5])[0])
            if not start:
                from datetime import date
                start = date.today().strftime('%Y-%m-%d')
            busy = get_busy_times(start, days)
            self._send_json(200, {'busy': busy})
        except Exception as e:
            traceback.print_exc()
            self._send_json(500, {'error': str(e)})

    def _calendar_create(self):
        """POST /calendar/create with JSON: {title, date, time, duration, location, description}"""
        try:
            from calendar_api import create_event
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length)) if content_length else {}

            title = body.get('title', 'Meeting')
            date = body.get('date')
            time = body.get('time')
            duration = body.get('duration', 30)
            location = body.get('location', '')
            description = body.get('description', '')

            if not date or not time:
                self._send_json(400, {'error': 'date and time are required'})
                return

            result = create_event(title, date, time, duration, location, description)
            self._send_json(200, result)
        except Exception as e:
            traceback.print_exc()
            self._send_json(500, {'error': str(e)})

    # ── Calley proxy ──

    def _proxy_calley(self, method):
        """Forward request to Calley API"""
        api_path = self.path[len('/calley-proxy/'):]
        target_url = f"{CALLEY_BASE}/{api_path}"

        auth_token = self.headers.get('authToken', '')
        headers = {
            'authToken': auth_token,
            'Content-Type': 'application/json'
        }

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
        """Quieter logging — only log proxy/calendar requests and errors"""
        msg = format % args
        if '/calley-proxy/' in msg or '/calendar/' in msg or '404' in msg or '500' in msg:
            super().log_message(format, *args)

if __name__ == '__main__':
    os.chdir(WEBROOT)
    with http.server.HTTPServer(('', PORT), DuetHandler) as httpd:
        print(f"Duet server running on http://localhost:{PORT}")
        print(f"Serving files from: {WEBROOT}")
        print(f"Calley proxy: /calley-proxy/* → {CALLEY_BASE}/*")
        print(f"Calendar API: /calendar/busy, /calendar/create")
        httpd.serve_forever()
