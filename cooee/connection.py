import os
from typing import Optional

from requests.auth import AuthBase

from .bearer import HTTPBearerAuth

headers = {'user-agent': 'cooee/0.0.1'}
auth: Optional[AuthBase] = None
local: bool = False


def set_local(ctx, param, value):
    global local
    local = value


token_file = os.path.expanduser("~/.cooee/token")
if os.path.isfile(token_file):
    with open(token_file, 'r') as f:
        auth = HTTPBearerAuth(f.read().strip())


def write_token(token: str):
    os.makedirs(os.path.expanduser("~/.cooee"), exist_ok=True)
    token_file = os.path.expanduser("~/.cooee/token")
    with open(token_file, 'w') as f:
        f.write(token)


def get_auth() -> Optional[AuthBase]:
    return auth


def web_path(path: str = "/"):
    host = "http://localhost:5000" if local else "https://www.coo.ee"
    return f"{host}{path}"


def api_path(path: str = "/"):
    host = "http://localhost:8080" if local else "https://api.coo.ee"
    return f"{host}{path}"
