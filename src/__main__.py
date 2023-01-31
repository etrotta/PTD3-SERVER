import dotenv
dotenv.load_dotenv()

from http.server import HTTPServer, BaseHTTPRequestHandler

from .request_handler import (
    Request,
    Response,
    handle_request,
)


class PTDHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # Not really used
        # print(self.command, self.path)
        # print(self.headers)
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        # if (size := self.headers.get("Content-Size")) is not None:
        #     print(self.rfile.read(size))

    def do_POST(self):
        # print(self.command, self.path)
        # print(self.headers)
        # path = pathlib.Path('data' + self.path.split('?')[0])
        # path.parent.mkdir(exist_ok=True, parents=True)
        body = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode('UTF-8')
        # with path.open('a') as file:
        #     file.write('\n')
        #     for thing in body.split("&"):
        #         file.write(unquote(thing) + '\n')
        #     file.write('\n')

        try:
            response: Response = handle_request(Request(self.command, self.path, body))
        except Exception:
            self.send_response(500, 'INTERNAL SERVER ERROR')
            self.end_headers()
            raise
        else:
            # print(response)
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write(response.encode())


def run(server_class=HTTPServer, handler_class=PTDHandler):
    server_address = ('', 1234)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
