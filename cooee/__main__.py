import webbrowser
from typing import List, Dict, Any

import click

from .actions import launch_action
from .apirequests import complete_request, launch_request, todo_request
from .connection import web_path
from .repl import run_repl


def set_local(ctx, param, value):
    global local
    local = value


@click.command()
@click.option('--login', is_flag=True, help='Login to coo.ee')
@click.option('--local', '-l', is_flag=True, help='Use local services', callback=set_local, expose_value=False)
@click.option('--fish-complete', is_flag=True, help='Fish shell completion')
@click.option('--repl', is_flag=True, help='Show Repl')
@click.argument('arguments', nargs=-1)
def main(login: bool = False, fish_complete: bool = False, repl: bool = False, arguments: List[str] = None):
    """https://coo.ee command line."""
    if login:
        webbrowser.open(web_path())
    elif fish_complete:
        complete_cli(arguments, fish=fish_complete)
    elif repl:
        run_repl()
    elif not arguments:
        todo()
    else:
        launch(arguments)


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
            print(f"{s['line']}\t{s['description']}")
        else:
            print(f"{s['line']}")


if __name__ == '__main__':
    main()
