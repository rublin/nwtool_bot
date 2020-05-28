from datetime import datetime
from http.server import BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    startedAt = None

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = 'The app started at {}\n' \
                  'Uptime: {:.2f} minutes\n\n' \
                  'https://t.me/nwtool_bot'.format(self.startedAt, (
                    datetime.now() - self.startedAt).total_seconds() / 60.0)
        self.wfile.write(message.encode("utf-8"))
