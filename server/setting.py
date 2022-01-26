from json import load
from pathlib import Path
from typing import Dict, Union

setting:Dict[str, Union[str, int, Path]] = dict

with open("setting.json", "rb") as f:
    setting = load(f)

if not setting:
    setting.update({
        "title": "backdoor",
        "host": "localhost",
        "port": 9998,
        "name_app_client":"windows"
    })

path_server = Path(".").absolute()
path_client = path_server.parent / "client"

setting["path_client"] = path_client.absolute()
setting["path_server"] = path_server