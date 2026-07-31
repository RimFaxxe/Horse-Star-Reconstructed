"""
Horse Star - Local Asset & Config Server
Bypasses CDN requests to assets01.horsestar.net and redirects them locally.
"""
import http.server
import socketserver
import os
import sys

PORT = 80
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLE_DIR = os.path.join(BASE_DIR, "bundles")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
BUILD_INFOS_DIR = os.path.join(BASE_DIR, "build_infos")

BUNDLE_PREFIX = "/r16/AssetBundleContents/"
CONFIG_PREFIX = "/r16/Config/"
ROOT_PREFIX = "/r16/"  # catches build_infos requested directly at root

class HorseStarHandler(http.server.BaseHTTPRequestHandler):

    def _serve_file(self, filepath, filename, label):
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"[{label}] {filename} ({size} bytes)")
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(size))
            self.end_headers()
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        else:
            print(f"[MISSING {label}] {filename} (looked in: {filepath})")
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"File not found")
    def do_GET(self):
        print(f"[REQUEST] {self.path}")

        if self.path.startswith(CONFIG_PREFIX):
            filename = self.path[len(CONFIG_PREFIX):]
            filepath = os.path.join(CONFIG_DIR, filename)
            self._serve_file(filepath, filename, "CONFIG")

        elif self.path.startswith(BUNDLE_PREFIX):
            filename = self.path[len(BUNDLE_PREFIX):]
            filepath = os.path.join(BUNDLE_DIR, filename)
            self._serve_file(filepath, filename, "BUNDLE")

        elif self.path.startswith(ROOT_PREFIX):
            # handles files requested directly at /r16/ root (Build_infos.xml, etc.)
            filename = self.path[len(ROOT_PREFIX):]
            if "/" in filename:
                print(f"[UNKNOWN PATH] {self.path}")
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not found")
                return
            filepath = os.path.join(BUILD_INFOS_DIR, filename)
            self._serve_file(filepath, filename, "BUILD_INFOS")

        else:
            print(f"[UNKNOWN PATH] {self.path}")
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")

    def log_message(self, format, *args):
        pass

def main():
    for d in [BUNDLE_DIR, CONFIG_DIR, BUILD_INFOS_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created directory: {d}")

    print("=========================================")
    print("Horse Star Local Asset Server")
    print("=========================================")
    print(f"Port: {PORT}")
    print("Watching for requests... (Ctrl+C to stop)")
    print("=========================================")

    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), HorseStarHandler) as httpd:
            httpd.serve_forever()
    except PermissionError:
        print("\nERROR: Port 80 requires Administrator privileges.")
        print("Please run this script from an elevated Command Prompt.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()

