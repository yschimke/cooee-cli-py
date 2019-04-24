from typing import List, Dict, Any, Union

import requests

from .connection import headers, api_path, get_auth


def complete_request(arguments: List[str]) -> List[Dict[str, Any]]:
    path = api_path(f"/api/v0/completion?q={'+'.join(arguments)}")
    r = requests.get(path, headers=headers, auth=get_auth())

    r.raise_for_status()

    result: Dict[str, Any] = r.json()
    suggestions: List[Dict[str, Any]] = result["suggestions"]

    return suggestions


def launch_request(arguments: Union[str,List[str]]) -> Dict[str, Any]:
    if type(arguments) == str:
        arguments = [arguments]

    path = api_path(f"/api/v0/goinfo?q={'+'.join(arguments)}")
    r = requests.get(path, headers=headers, auth=get_auth())

    if r.status_code != 404:
        r.raise_for_status()

    result: Dict[str, Any] = r.json()
    result["status_code"] = r.status_code

    return result


def todo_request():
    path = api_path(f"/api/v0/todo")
    r = requests.get(path, headers=headers, auth=get_auth())

    r.raise_for_status()

    result: Dict[str, Any] = r.json()
    todos: List[Dict[str, Any]] = result["todos"]

    return todos
