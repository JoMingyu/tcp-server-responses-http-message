import socketserver
from typing import Tuple, List, Dict


class Request:
    def parse_start_line(self, text: bytes) -> List[str]:
        return [elem.strip().decode() for elem in text.split()]

    def parse_headers(self, lines: List[bytes]) -> Dict[str, str]:
        headers = dict()

        for line in lines:
            k, v = line.split(b":", 1)

            headers[k.strip().decode()] = v.strip().decode()

        return headers

    def __init__(self, message: bytes):
        lines = message.split(b"\r\n")

        method, path, protocol = self.parse_start_line(lines[0])

        self.method = method
        self.path = path
        self.protocol = protocol

        body_exists = not bool(lines[-2])

        if body_exists:
            header_lines = lines[1:-2]
        else:
            header_lines = lines[1:]

        self.headers = self.parse_headers(header_lines)


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        req = Request(self.data)

        print(req.method)
        print(req.path)
        print(req.protocol)
        print(req.headers)

        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(
            b"""
        HTTP/1.1"""
        )


if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
