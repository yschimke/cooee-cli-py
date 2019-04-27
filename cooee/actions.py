import webbrowser
from typing import Dict, Any

from prompt_toolkit import print_formatted_text

from .format import todo_string


def launch_action(result: Dict[str, Any]):
    if "location" in result:
        webbrowser.open(result["location"])
    else:
        print_formatted_text(todo_string(result))
