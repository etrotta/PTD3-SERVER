class Request:
    def __init__(self, path: str, data: dict[str, str]):
        self.path = path
        self.data = data

    @classmethod
    def from_http(cls, url: str, body: str) -> 'Request':
        path = url.split('?', 1)[0]
        data = {k: v for k, v in (x.split('=') for x in body.split('&'))}
        return cls(
            path.removeprefix('/'),
            data,            
        )

    @classmethod
    def from_wsgi(cls, environ: dict[str, str]) -> 'Request':
        path = environ['path']
        body = environ['body']

        print(environ)
        print(body)

        data = {k: v for k, v in (x.split('=') for x in body.split('&'))}
        return cls(
            path.removeprefix('/'),
            data,            
        )

    def __repr__(self) -> str:
        return f"Request({self.path=}, {self.data=})"

class Response:
    def __init__(self, **kwargs):
        self.data = '&'.join(f'{k}={v}' for k, v in kwargs.items())

    def __repr__(self) -> str:
        return f"Response({self.data=})"

    def encode_http(self) -> bytes:
        return self.data.encode("utf-8")
    
    def encode_wsgi(self) -> dict:
        'Returns a {code: ..., headers: ..., output: ...} dict'
        return {
            'code': '200 OK',
            'headers': [],
            'output': self.data.encode("utf-8"),
        }
