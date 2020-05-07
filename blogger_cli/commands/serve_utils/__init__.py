import os
import socket
import socketserver
import http.server


def is_port_occupied(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", port))
    return True if result == 0 else False


def serve_locally(given_dir, PORT):
    os.chdir(given_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    httpd.serve_forever()


def get_free_port():
    for port_no in range(8000, 9000):
        if not is_port_occupied(port_no):
            return port_no
