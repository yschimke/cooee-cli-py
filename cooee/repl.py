import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from prompt_toolkit.completion import Completer, Completion, CompleteEvent, ThreadedCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.validation import Validator, ThreadedValidator, ValidationError

from .actions import launch_action
from .apirequests import complete_request, todo_request
from .apirequests import launch_request

todos: List[Dict[str, Any]] = []
updated_at: datetime = datetime.now()
selected: Optional[Dict[str, Any]] = None


def update_todos():
    global todos
    global updated_at

    since: timedelta = datetime.now() - updated_at

    if since > timedelta(seconds=10):
        todos = todo_request()
        updated_at = datetime.now()


class CooeeValidator(Validator):
    def validate(self, document):
        global selected
        selected = document.current_line
        result = launch_request(selected)
        # print(f"'{selected}' {result}")
        if result["message"] == "no match":
            selected = None
            raise ValidationError(0, f"no match")
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


def launch(arguments: List[str]):
    if arguments != [] and arguments != [""]:
        result: Dict[str, Any] = launch_request(arguments)

        launch_action(result)


def run_repl():
    global todos
    global selected

    cooee_completer = CooeeCompleter()
    cooee_validator = CooeeValidator()

    def get_rprompt():
        return f"> {selected}"

    def bottom_toolbar():
        update_todos()
        todo_text = f'Todos: ({len(todos)})'
        loading_text = f' Loading completions... ' if cooee_completer.loading > 0 else ''
        return todo_text + loading_text

    history_file = os.path.expanduser("~/.cooee/repl.hist")
    session = PromptSession('> ',
                            completer=ThreadedCompleter(cooee_completer),
                            complete_while_typing=True,
                            bottom_toolbar=bottom_toolbar,
                            complete_style=CompleteStyle.MULTI_COLUMN,
                            history=FileHistory(history_file),
                            refresh_interval=5,
                            rprompt=get_rprompt(),
                            validator=ThreadedValidator(cooee_validator),
                            )

    while True:
        try:
            text = session.prompt()
            launch([text])
            update_todos()
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
