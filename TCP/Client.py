import pickle as pkl
import socket as skt

from .Common import *


class Client:
    def __init__(self, IP='127.0.0.1', PORT=8080):
        self.__IP = IP
        self.__PORT = PORT
        
        self.__run = 0
        self.__mode = {}
        
    def addMode(self, key):
        def decorator(func):
            self.__mode[key] = func
            return func
            
        return decorator
        
    def start(self):
        pass
        
    def end(self):
        if self.__run:
            self.__run = 0
            self.send("__END__")
        
    @staticmethod
    def announce(msg, From="System"):
        msg = msg if type(msg) != bytes else msg.decode()
        print(f"[{From}]", msg)
        
    def send(self, obj):
        self.__CONN.sendall(pkl.dumps(obj))
        
    def recv(self, raw=False, buffer=1024):
        data = b""
        
        while 1:
            tmp = self.__CONN.recv(buffer)
            data += tmp
            
            if len(tmp) < buffer: break
            
        return data.encode() if raw else data
