import os
import urllib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import ParseResult

from prompt_toolkit import print_formatted_text
from prompt_toolkit.completion import Completer, Completion, CompleteEvent, ThreadedCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.validation import Validator, ThreadedValidator, ValidationError

from .format import todo_string
from .actions import launch_action
from .apirequests import complete_request, todo_request
from .apirequests import launch_request

todos: Optional[List[Dict[str, Any]]] = None
updated_at: Optional[datetime] = None
selected: Optional[Dict[str, Any]] = {"message": "Todos"}


def update_todos():
    global todos
    global updated_at

    needs_update = False

    if updated_at is None or todos is None:
        needs_update = True
    else:
        since: timedelta = datetime.now() - updated_at

        if since > timedelta(seconds=10):
            needs_update = True

    if needs_update:
        todos = todo_request()
        updated_at = datetime.now()


class CooeeValidator(Validator):
    def validate(self, document: Document):
        global selected
        line = document.current_line

        if line == "":
            selected = {"message": "Todos"}
        else:
            result = launch_request(line)
            if result["status_code"] == 404:
                selected = None
                raise ValidationError(document.cursor_position, f"no match")
            else:
                selected = result


class CooeeCompleter(Completer):
    def __init__(self):
        self.loading = 0

    def get_completions(self, document: Document, complete_event: CompleteEvent):
        self.loading += 1

        try:
            if document.current_line == "":
                for c in todos:
                    completion = Completion(text=c["line"],
                                            display_meta=c["description"])
                    yield completion
            else:
                line = document.current_line_before_cursor

                results = complete_request([line])
                for c in results:
                    style = ""
                    selected_style = ""
                    if "color" in c:
                        color = c["color"]
                        style = f'fg:{color}'
                        selected_style = f'fg:white bg:{color}'

                    completion = Completion(text=c["line"],
                                            start_position=-len(line),
                                            display_meta=c["description"],
                                            style=style,
                                            selected_style=selected_style)

                    yield completion
        finally:
            self.loading -= 1


def launch(arguments: str):
    result: Dict[str, Any] = launch_request(arguments)
    launch_action(result)


def run_repl():
    global todos
    global selected

    update_todos()

    cooee_completer = CooeeCompleter()
    cooee_validator = CooeeValidator()

    def get_rprompt():
        global selected

        if selected is None:
            return ""

        if "location" in selected:
            url: str = selected["location"]
            parts: ParseResult = urllib.parse.urlparse(url)
            return parts.hostname + parts.path
        elif "message" in selected:
            return selected["message"]

        return f"{selected}"

    def bottom_toolbar():
        update_todos()
        num = len(todos) if todos is not None else 0
        todo_text = f'Todos: ({num})'
        loading_text = f' Loading completions... ' if cooee_completer.loading > 0 else ''
        return todo_text + loading_text

    history_file = os.path.expanduser("~/.cooee/repl.hist")
    session = PromptSession('> ',
                            completer=ThreadedCompleter(cooee_completer),
                            complete_while_typing=False,
                            bottom_toolbar=bottom_toolbar,
                            complete_style=CompleteStyle.MULTI_COLUMN,
                            history=FileHistory(history_file),
                            refresh_interval=5,
                            rprompt=get_rprompt,
                            validator=ThreadedValidator(cooee_validator),
                            validate_while_typing=True,
                            )

    while True:
        try:
            text = session.prompt()
            if text != "":
                launch(text)
            else:
                update_todos()
                print_formatted_text("Todos")
                for t in todos:
                    print_formatted_text(todo_string(t))
            selected = {"message": "Todos"}
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
