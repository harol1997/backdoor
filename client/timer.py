from datetime import date, datetime
from threading import Thread

class Timer:

    def __init__(self, time:int) -> None:
        self.__time = time
        self.__on = False
        self.__time_start = None

    def __count_time(self):
    
        while True:
            time_final = datetime.utcnow()
            if (time_final - self.__time_start).seconds > self.__time:
                break
        self.__on = False

    @property
    def number(self):
        return self.__number    

    @property 
    def on(self):
        return self.__on

    def start(self, thread=False):
        self.__on = True
        self.__time_start = datetime.utcnow()
        if thread:
            Thread(target=self.__count_time).start()
        else:
            self.__count_time()