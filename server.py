from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote
from json import dumps, loads

import traceback

import model

class Server(BaseHTTPRequestHandler):
    def _success(self):
        self.send_response(200)
        self.send_header("content-type", "text/json")
        self.end_headers()

    def _400(self):
        self.send_response(400)
        self.send_header("content-type", "text/html")
        self.end_headers()
    
    def _404(self):
        self.send_response(404)
        self.send_header("content-type", "text/html")
        self.end_headers()

    def do_HEAD(self):
        self._success()

    def do_GET(self):
        response = {"success": True}

        try:
            url = urlparse(self.path)

            path = url.path
            if path == "/emote" or path == "/emote/":
                query = unquote(url.query)
                qd = dict(q.split("=", 1) for q in query.split("&"))

                if "sentences" in qd:
                    l = loads(qd["sentences"])
                    if isinstance(l, list):
                        response["emoji"] = model.emojify_sentences([str(x) for x in l])
                    else:
                        response["success"] = False
                else:
                    response["success"] = False

                self._success()
                self.wfile.write(bytes(dumps(response), "utf-8"))
            else:
                self._404()
        except:
            traceback.print_exc()
            self._400()

if __name__ == "__main__":
    httpd = HTTPServer(("", 8080), Server)
    print("Server is running!")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()