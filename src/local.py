"HTTP to WSGI adapter for running locally (not recommended for use when hosting online!)"
try:
    import dotenv
    dotenv.load_dotenv('local.env')
except ImportError:
    print("Failed to import dotenv ; will not load `local.env` even if it is present")

from io import BytesIO
from http.server import HTTPServer, BaseHTTPRequestHandler

from src.main import app


class PTDHandler(BaseHTTPRequestHandler):
    def send_request_to_app(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        environ = {
            "CONTENT_LENGTH": str(len(body)),
            "PATH_INFO": self.path,
            "REMOTE_ADDR": "127.0.0.1",
            "wsgi.input": BytesIO(body),
        }
        print(environ)
        def _start_response(code: str, headers: list[tuple[str, str]]):
            code_number, code_reason = code.split(' ', 1)
            code_number = int(code_number)
            self.send_response(code_number, code_reason)
            for header in headers:
                self.send_header(*header)
        output = app(environ, _start_response)
        self.end_headers()
        for out in output:
            self.wfile.write(out)

    def do_GET(self):
        return self.send_request_to_app()

    def do_POST(self):
        return self.send_request_to_app()


def run(server_class=HTTPServer, handler_class=PTDHandler):
    server_address = ('', 1234)
    server = server_class(server_address, handler_class)
    server.serve_forever()

if __name__ == '__main__':
    print("Running PTD3 Server locally on port 1234")
    run()
