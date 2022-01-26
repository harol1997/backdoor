from socket import socket


class Host:
    def __init__(self, id:int, sock:socket, address, name = "") -> None:
        self.__id = id
        self.__sock = sock
        self.__address = address
        self.__name = name

    @property
    def id(self):
        return self.__id

    def __eq__(self, host: "Host") -> bool:
        return self.__id == host.id

    def get_list(self):
        return [self.__id, self.__name]

    @property
    def sock(self):
        return self.__sock

    @property
    def name(self):
        return self.__name