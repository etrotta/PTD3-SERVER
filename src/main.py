try:
    import dotenv
    dotenv.load_dotenv('local.env')
except ImportError:
    pass

from request_handler import (
    Request,
    Response,
    handle_request,
)

class App:
    def __call__(self, data, start_response):
        """
        Handles incoming interaction data
        (WSGI)
        """
        data["path"] = data.get("PATH_INFO") or '/'

        if data['path'] == '/mystery_gift':  # TODO IMPLEMENT MYSTERY GIFT?
            start_response('200 OK', [])
            return []

        assert data['path'] == '/save'

        response: Response = handle_request(Request.from_wsgi(data))

        result = response.encode_wsgi()
        start_response(result['code'], result['headers'])
        return [result['output']]

app = App()
