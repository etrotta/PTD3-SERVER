class Request:
    def __init__(self, method: str, url: str, body: str):
        if '?' in url:
            path, query = url.split('?', 1)
        else:
            path, query = url, ''

        self.method = method.removeprefix('/')
        self.path = path.removeprefix('/')
        if query:
            self.query = {k: v for k, v in (x.split('=') for x in query.split('&'))}
        else:
            self.query = None
        self.data = {k: v for k, v in (x.split('=') for x in body.split('&'))}

    def __repr__(self) -> str:
        return f"Request({self.path=}, {self.query=}, {self.method=}, {self.data=})"

class Response:
    def __init__(self, **kwargs):
        self.data = '&'.join(f'{k}={v}' for k, v in kwargs.items())

    def __repr__(self) -> str:
        return f"Response({self.data=})"

    def encode(self):
        return self.data.encode("utf-8")
