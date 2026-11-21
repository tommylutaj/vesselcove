#!/usr/bin/env python3
"""Minimal localhost server for VesselCove interactive demo on 127.0.0.1:8090."""
import http.server
import os
from functools import partial

PORT = int(os.environ.get("PORT", "8090"))
DIR = os.path.dirname(os.path.abspath(__file__))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    handler = partial(QuietHandler, directory=DIR)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    print(f"VesselCove Demo serving at http://127.0.0.1:{PORT}/", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
