from pathlib import Path

from src.request_handler import (
    Request,
    Response,
    handle_request,
)

_static_files = (
    'index.html',
    'style.css',
    'mod_instructions.txt',
)
path = Path(__file__).parent

class App:
    def __call__(self, data, start_response):
        """
        Handles incoming interaction data
        (WSGI)
        """
        data["path"] = data.get("PATH_INFO").removeprefix('/') or 'index.html'
        data["body"] = data['wsgi.input'].read().decode('UTF-8')

        try:
            # Save/Load/Delete/List saves, meant to speak with the game client
            if data['path'].startswith('ptd3save'):  # Manage (PTD3 Story) Save
                    response: Response = handle_request(Request(data['body']))
                    result = response.encode()
                    start_response('200 OK', [])
                    return [result]
            # Documentation
            elif data['path'] in _static_files:
                with open(path / data['path'], 'rb') as file:
                    start_response('200 OK', [])
                    return [file.read()]
            # TODO IMPLEMENT MYSTERY GIFT?
            elif data['path'] == 'mystery_gift':  
                start_response('200 OK', [])
                return []
            # 404 Not Found
            else:
                start_response('404 NOT FOUND', [])
                return ['Page not found'.encode('UTF-8')]

        except Exception as err:
            raise
            import sys
            error_message = f"Error {err}   Environ {data}"
            sys.stdout.write(error_message)
            sys.stderr.write(error_message)
            start_response('500 INTERNAL SERVER ERROR', [])
            return [error_message.encode('UTF-8')]


app = App()
