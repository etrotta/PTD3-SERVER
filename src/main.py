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
        data["body"] = data['wsgi.input'].read().decode('UTF-8')

        if data['path'] == '/mystery_gift':  # TODO IMPLEMENT MYSTERY GIFT?
            start_response('200 OK', [])
            return []


        try:
            response: Response = handle_request(Request.from_wsgi(data))

            result = response.encode_wsgi()
        except Exception as err:
            result = {
                'code': '500 UH OH',
                'headers': [],
                'output': (
                    f"Error {err}\n"
                    f"Environ: {data}\n"
                ).encode("UTF-8")
            }
            import sys
            import json
            sys.stdout.write(str(err) + str(data))
            sys.stderr.write(str(err) + str(data))
        start_response(result['code'], result['headers'])
        return [result['output']]

app = App()
