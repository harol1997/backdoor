import base64
import cv2
import pyautogui
import host
import pynput
import timer
import connection
import start_run
import subprocess
import win32
import win32api

from pathlib import Path
def encode(data):
    try:
        # Standard Base64 Encoding
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        return str(encodedBytes, "utf-8")
    except:
        return ""

def decode(data):
    try:
        message_bytes = base64.b64decode(data)
        return message_bytes.decode('utf-8')
    except:
        return ""

path_main = Path(__file__).parent.absolute().joinpath("main.py").as_posix()

with open(path_main, "r") as f:
    your_code = encode(f.read())

try:
    exec(decode(your_code))
except Exception as e:
    print(e)

input()