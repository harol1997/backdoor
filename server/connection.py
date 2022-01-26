from socket import socket, AF_INET, SOCK_STREAM
from os import path
from functools import wraps


class Connector(socket):

    __BUFFER = 4096

    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None) -> None:
        super().__init__(family, type, proto, fileno)

    def recv_bytes(self, con:socket=None):
        con:socket = con if con else self
        data = b''
        while True:
            data += con.recv(self.__BUFFER)
            if b'-' in data:
                break
        index = data.index(b'-')
        size = int(data[:index])
        data = data[index+1:]
        yield data
        size -= len(data)
        while size > 0:
            data = con.recv(self.__BUFFER)
            size -= len(data)
            yield data

    def recv_file(self, path_file:str, conn:socket=None):
        """[summary]

        :param path_file: [description]
        :type path_file: str
        :param conn: [description], defaults to None
        :type conn: socket, optional
        """
        with open(path_file, "wb") as f:
            for data in self.recv_bytes(con=conn):
                f.write(data)

    def recv_str(self, conn:socket=None):
        for data in self.recv_bytes(con=conn):
            try:
                print(data.decode())
            except:
                print(data.decode("windows-1252"))

    def get_str(self, conn:socket=None):
        string = ""
        for data in self.recv_bytes(con=conn):
            try:
                string += data.decode()
            except:
                string += data.decode("windows-1252")
        return string

    def send_bytes(self, data:bytes, con:socket=None, just_bytes:bool=False) -> None:
        con:socket = con if con else self
        if just_bytes:
            con.sendall(data)
        else:
            con.sendall(bytes(str(len(data)) + '-', "utf-8")+data)

    def send_str(self, string:str, con:socket=None)->None:
        self.send_bytes(bytes(string, "utf-8"), con)
    
    def send_file(self, filename:str, con:socket=None)->None:
        if path.isfile(filename):
            con = con if socket else self
            size = path.getsize(filename)
            self.send_bytes(bytes(str(size)+"-", "utf-8"), con, just_bytes=True)
            with open(filename, "rb") as f:
                while True:
                    data = f.read(self.__BUFFER)
                    if not data:
                        
                        break
                    self.send_bytes(data, con, just_bytes=True)
        else:
            raise FileNotFoundError()
