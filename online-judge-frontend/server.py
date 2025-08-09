import http.server
import socketserver
import os

PORT = 8000

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # Default behavior first
        mimetype = super().guess_type(path)

        # If it's a .js file, ensure it's served as application/javascript
        if path.endswith(".js"):
            return "application/javascript"
        return mimetype

# Change to the directory where your static files are located
# This is crucial if your npm script runs from a different location
# For example, if your static files are in a 'public' folder
# os.chdir('public') # Uncomment and modify if needed

with socketserver.TCPServer(("", PORT), CustomHTTPHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()