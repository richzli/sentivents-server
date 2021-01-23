from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from json import dumps, loads

class Server(BaseHTTPRequestHandler):
    def _success(self):
        self.send_response(200)
        self.send_header("content-type", "text/json")
        self.end_headers()

    def _400(self):
        self.send_response(400)
        self.send_header("content-type", "text/html")
        self.end_headers()

    def do_HEAD(self):
        self._success()

    def do_GET(self):
        try:
            query = urlparse(self.path).query
            print(query)
            qd = dict(q.split("=") for q in query.split("&"))
            print(qd)

            self._success()
            self.wfile.write(bytes(dumps(qd), "utf-8"))
        except:
            self._400()

if __name__ == "__main__":
    httpd = HTTPServer(("", 8080), Server)
    print("Server is running!")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()