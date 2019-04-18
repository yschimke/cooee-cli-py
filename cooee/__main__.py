import asyncio
import os
import webbrowser
from typing import List, Dict, Any

import click
import requests
from requests.auth import AuthBase

from .bearer import HTTPBearerAuth

headers = {'user-agent': 'cooee/0.0.1'}
auth: AuthBase = None
local: bool = False


def set_local(ctx, param, value):
    global local
    local = value


@click.command()
@click.option('--login', is_flag=True, help='Login to coo.ee')
@click.option('--local', '-l', is_flag=True, help='Use local services', callback=set_local, expose_value=False)
@click.option('--fish-complete', is_flag=True, help='Fish shell completion')
@click.argument('arguments', nargs=-1)
def main(login: bool = False, fish_complete: bool = False, arguments: List[str] = None):
    """https://coo.ee command line."""
    global auth

    token_file = os.path.expanduser("~/.cooee/token")
    if os.path.isfile(token_file):
        with open(token_file, 'r') as f:
            auth = HTTPBearerAuth(f.read().strip())

    if login:
        webbrowser.open(web_path())
    elif fish_complete:
        complete(arguments, fish=fish_complete)
    elif not arguments:
        todo()
    else:
        launch(arguments)


def launch(arguments: List[str]):
    path = api_path(f"/api/v0/goinfo?q={'+'.join(arguments)}")
    r = requests.get(path, headers=headers, auth=auth)

    r.raise_for_status()

    result: Dict[str, Any] = r.json()

    if "location" in result:
        webbrowser.open(result["location"])
    else:
        print(result)


def todo():
    path = api_path(f"/api/v0/todo")
    r = requests.get(path, headers=headers, auth=auth)

    r.raise_for_status()

    result: Dict[str, Any] = r.json()

    print(result)


def complete(arguments: List[str], fish: bool = False):
    path = api_path(f"/api/v0/completion?q={'+'.join(arguments)}")
    r = requests.get(path, headers=headers, auth=auth)

    r.raise_for_status()

    result: Dict[str, Any] = r.json()
    suggestions: List[Dict[str, Any]] = result["suggestions"]

    for s in suggestions:
        if fish:
            print(f"{s['line']}\t{s['description']}")
        else:
            print(f"{s['line']}")


def web_path(path: str = "/"):
    host = "http://localhost:5000" if local else "https://www.coo.ee"
    return f"{host}{path}"


def api_path(path: str = "/"):
    host = "http://localhost:8080" if local else "https://api.coo.ee"
    return f"{host}{path}"


if __name__ == '__main__':
    asyncio.run(main())
