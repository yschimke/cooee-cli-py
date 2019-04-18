from prompt_toolkit.completion import Completer, Completion, CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.shortcuts import PromptSession

from .apirequests import complete_request, todo_request
from typing import List, Dict, Any
from .apirequests import launch_request
from .actions import launch_action

todos = []


class CooeeCompleter(Completer):
    def __init__(self):
        self.loading = 0

    def get_completions(self, document: Document, complete_event: CompleteEvent):
        self.loading += 1

        try:
            if document.current_line == "":
                for c in todo_request():
                    completion = Completion(text=c["line"], display_meta=c["description"])
                    yield completion
            else:
                line = document.current_line_before_cursor

                for c in complete_request([line]):
                    completion = Completion(text=c["line"], start_position=-len(c["line"]),
                                            display_meta=c["description"])
                    yield completion
        finally:
            self.loading -= 1


def launch(arguments: List[str]):
    result: Dict[str, Any] = launch_request(arguments)

    launch_action(result)


async def run_repl():
    global todos
    cooee_completer = CooeeCompleter()

    def bottom_toolbar():
        todo_text = f'Todos: ({len(todos)})'
        loading_text = f' Loading completions... ' if cooee_completer.loading > 0 else ''
        return todo_text + loading_text

    session = PromptSession('Say something: ', completer=cooee_completer,
                            complete_in_thread=True, complete_while_typing=True,
                            bottom_toolbar=bottom_toolbar,
                            complete_style=CompleteStyle.MULTI_COLUMN)

    while True:
        try:
            text = session.prompt('> ')
            launch([text])
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
