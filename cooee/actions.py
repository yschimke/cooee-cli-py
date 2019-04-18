import webbrowser
from typing import Dict, Any


def launch_action(result: Dict[str, Any]):
    if "location" in result:
        webbrowser.open(result["location"])
    else:
        print(result)
