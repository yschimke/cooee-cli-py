from typing import Dict, Optional

from prompt_toolkit.formatted_text import FormattedText


def todo_string(todo: Dict[str, any]):
    if todo.get("status_code") == 404:
        return FormattedText([('orange', todo["message"])])

    result = FormattedText([])

    if "line" in todo:
        result.append((todo.get('color', ''), todo['line']))

    if "description" in todo:
        if result:
            result.append(('', ': '))
        result.append(('', todo.get('description')))

    if "url" in todo:
        if result:
            result.append(('', '\n'))
        result.append(('blue', todo.get('url', '')))

    if "message" in todo:
        if result:
            result.append(('', '\n'))
        result.append(('', todo.get('message', '')))

    return result
