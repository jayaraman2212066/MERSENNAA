#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Handle API endpoints
        if parsed_path.path == '/api/images':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            images = []
            # Check archived_png_files directory
            if os.path.exists('archived_png_files'):
                for file in os.listdir('archived_png_files'):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        images.append({
                            'name': file,
                            'path': f'archived_png_files/{file}'
                        })
            
            response = {'images': images}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Handle other API endpoints with demo responses
        elif parsed_path.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Demo mode - full functionality requires complete backend'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Serve index.html for root path
        elif parsed_path.path == '/':
            self.path = '/templates/index.html'
        
        # Default file serving
        super().do_GET()
    
    def do_POST(self):
        # Handle POST API endpoints
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Demo mode - full functionality requires complete backend'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        super().do_POST()

def start_server(port=8000):
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"Server running at http://localhost:{port}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is already in use. Trying port {port+1}")
            start_server(port+1)
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    start_server()