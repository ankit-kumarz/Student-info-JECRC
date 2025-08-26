from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

# Set CORS headers
class CORSRequestHandler(MyHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

# Make sure we serve files from the directory this script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

httpd = HTTPServer(('127.0.0.1', 5500), CORSRequestHandler)
print("Server started at http://127.0.0.1:5500")
httpd.serve_forever()