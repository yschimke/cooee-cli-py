import os
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from logging import DEBUG
from typing import List, Dict, Any

import click

from .actions import launch_action
from .apirequests import complete_request, launch_request, todo_request
from .connection import web_path, write_token, set_local
from .repl import run_repl


@click.command()
@click.option('--login', is_flag=True, help='Login to coo.ee')
@click.option('--logout', is_flag=True, help='Logout from coo.ee')
@click.option('--version', is_flag=True, help='Show version')
@click.option('--local', '-l', is_flag=True, help='Use local services', callback=set_local, expose_value=False)
@click.option('--fish-complete', is_flag=True, help='Fish shell completion')
@click.option('--repl', is_flag=True, help='Show Repl')
@click.option('--debug', is_flag=True, help='Debug')
@click.argument('arguments', nargs=-1)
def main(login: bool = False, fish_complete: bool = False, repl: bool = False, arguments: List[str] = None,
         logout: bool = False, version: bool = False, debug: bool = False):
    """https://coo.ee command line."""
    if debug:
        enable_debug()

    if login:
        login_and_store()
    elif logout:
        logout_token()
    elif version:
        show_version()
    elif fish_complete:
        complete_cli(arguments, fish=fish_complete)
    elif repl:
        run_repl()
    elif not arguments:
        todo()
    else:
        launch(arguments)


# noinspection PyUnresolvedReferences
def enable_debug():
    import requests
    import logging
    from http.client import HTTPConnection

    logging.basicConfig(
        level=DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    HTTPConnection.debuglevel = 1
    req_log = logging.getLogger('requests')
    req_log.setLevel(logging.DEBUG)
    req_log.propagate = True


def logout_token():
    os.remove(os.expanduser("~/.cooee/token"))


def show_version():
    print("Version x.x")


def login_and_store():
    class LoginHandler(BaseHTTPRequestHandler):
        def log_request(self, code='-', size='-'):
            if code != 200:
                super().log_request(code, size)

        # noinspection PyPep8Naming
        def do_GET(s):
            import urllib

            s.send_response(200)
            s.end_headers()

            url = urllib.parse.urlparse(s.path)
            query = urllib.parse.parse_qs(url.query)

            write_token(query['code'][0])
            s.server.shutdown()

    callback = 'http://localhost:3000/callback'
    webbrowser.open(web_path(f"/user/jwt?callback={callback}"))

    server = ThreadingHTTPServer(('', 3000), LoginHandler)
    server.serve_forever()


def launch(arguments: List[str]):
    result: Dict[str, Any] = launch_request(arguments)

    launch_action(result)


def todo():
    todos: List[Dict[str, Any]] = todo_request()

    print(todos)


def complete_cli(arguments: List[str], fish: bool = False):
    suggestions: List[Dict[str, Any]] = complete_request(arguments)

    for s in suggestions:
        if fish:
            description: str = s.get('description', "")[:20]
            print(f"{s['line']}\t{description}")
        else:
            print(f"{s['line']}")


if __name__ == '__main__':
    main()
