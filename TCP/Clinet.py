import pickle
import socket

from .Common import Command


class Clinet(object):
    def __init__(self, IP="127.0.0.1", PORT=8080):
        self.IP = IP
        self.PORT = PORT
        self.__alive = True

        self.mode = {}
    
    # Print formated message
    @staticmethod
    def announce(msg, As="System"):
        print(f"[{As}]", (msg if type(msg) != bytes else msg.decode()))

    def addMode(self, key):
        def decorator(func):
            self.mode[key] = func

        return decorator

    def start(self):
        self.CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CONN.connect((self.IP, self.PORT))
        self.announce(self.CONN.recv(10240))

        while self.__alive:
            command = Command(input("> "))
            command.bytes = pickle.dumps(command)

            if (tmp := self.mode.get(command.split[0], None)) is not None:
                tmp(self.CONN, command)
                continue

            self.announce("Command not found")

        self.CONN.close()

    def end(self):
        self.CONN.sendall(pickle.dumps("__END__"))
        self.__alive = False
