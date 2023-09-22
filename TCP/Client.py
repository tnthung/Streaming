import pickle as pkl
import socket as skt

from .Common import *


class Client:
    def __init__(self, IP='127.0.0.1', PORT=8080):
        self.__IP = IP      # IP address
        self.__PORT = PORT  # Port to connect

        self.__run = False  # If Client is running
        self.__mode = {}    # Modes for client to handle communication

    # Add mode for Client to run on
    def addMode(self, key):
        def decorator(func):
            self.__mode[key] = func

        return decorator

    # Start Client
    def start(self):
        self.__CONN = skt.socket(skt.AF_INET, skt.SOCK_STREAM) # Create socket

        try: self.__CONN.connect((self.IP, self.PORT))         # Make connection
        except ConnectionRefusedError:                         # Can't connect to server
            self.announce("Can't connect to Server")
            exit()

        self.announceRespond()                                 # Announce Respound

        self.__run = True
        while self.__run:
            command = Command(input("> "))

            if (tmp := self.__mode.get(command.name, None)) is not None:
                tmp(command)
                continue

            self.announce("Command not found")

        self.__CONN.close()

    # Kill Client
    def end(self):
        if self.__run:
            self.__run = False
            self.sendObj("__END__")

    # Announce msg to Client console
    @staticmethod
    def announce(msg, From="System"):
        msg = msg if type(msg) != bytes else msg.decode()
        print(f"[{From}]", msg)

    # Announce respond
    def announceRespond(self):
        tmp = self.recv().decode()
        self.announce(tmp, "Server")
        return tmp

    # Send pickled obj
    def sendObj(self, obj):
        self.__CONN.sendall(pkl.dumps(obj))

    # Send raw obj
    def send(self, obj):
        self.__CONN.sendall(obj)

    # Receive pickled obj
    def recvObj(self, bufferSize=32768):
        data = b""

        while 1:
            tmp = self.__CONN.recv(bufferSize)
            data += tmp

            if len(tmp) < bufferSize: break

        return pkl.loads(data)

    # Receive raw obj
    def recv(self, bufferSize=32768):
        data = b""

        while 1:
            tmp = self.__CONN.recv(bufferSize)
            data += tmp

            if len(tmp) < bufferSize: break

        return data

    # Fetch IP
    @property
    def IP(self):
        return self.__IP

    # Fetch PORT
    @property
    def PORT(self):
        return self.__PORT

    # Fetch running status
    @property
    def isRunning(self):
        return self.__run
