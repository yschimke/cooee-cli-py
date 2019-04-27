from typing import Dict, Optional

from prompt_toolkit.formatted_text import FormattedText


def todo_string(todo: Dict[str, any]):
    if todo.get("status_code") == 404:
        return FormattedText([('red', todo["message"])])

    result = FormattedText([
        (todo.get('color', ''), todo['line']),
        ('', ': '),
    ])

    if "description" in todo:
        result.extend([
            ('', ' '),
            ('', todo.get('description')),
        ])

    if "description" in todo:
        result.extend([
            ('', '\n'),
            ('blue', todo.get('location', '')),
        ])

    if "message" in todo:
        result.extend([
            ('', '\n'),
            ('', todo.get('message', '')),
        ])

    return result
