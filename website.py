import RangeHTTPServer
import socketserver
import os
import time
import threading
import random
import json
import subprocess

PORT = int(os.getenv('PORT', 8008))

print("starting server")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class CustomRequestHandler(RangeHTTPServer.RangeRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')  # Add CORS header
        super().end_headers()

    def send_file(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(content.encode())

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        if self.path == '/get_pages':
            headers = self.headers
            manga = headers['manga']
            print(manga)
            pageCount = len(os.listdir("downloads/" + manga))
            self.send_json_response(200, pageCount)

        if self.path == '/get_mangas':
            print(os.listdir("downloads"))
            self.send_json_response(200, os.listdir("downloads"))

        if self.path == '/get_panels':
            headers = self.headers
            manga = headers['manga']
            chapter = int(headers['chapter'])
            print(manga, chapter)
            panels = os.listdir("downloads/" + manga + "/chapter-" + str(chapter))
            panelList = ["downloads/" + manga + "/chapter-" + str(chapter) + "/" + i for i in panels]
            panelList.sort(key=lambda x: int(x.split("-")[-1].split(".")[0]))
            self.send_json_response(200, panelList)

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

url = "http://localhost:" + str(PORT) + "/page.html"
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
command = [chrome_path, "--incognito", url]
subprocess.Popen(command)


with ThreadedHTTPServer(("", PORT), CustomRequestHandler) as httpd:
    print("serving at port", PORT)
    # Start a new thread for serving requests
    for i in range(10):
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True  # Daemonize the thread so it exits when the main thread exits
        server_thread.start()
        # Wait for the server thread to finish (if ever)
        server_thread.join()
