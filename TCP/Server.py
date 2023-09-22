import time as t
import pickle as pkl
import socket as skt
import threading as th

from .Common import *


class Server:
    def __init__(self, IP="127.0.0.1", PORT=8080, listenFor=10):
        self.__IP = IP                # IP address
        self.__CONN = []              # All connections
        self.__PORT = PORT            # Port listen on
        self.__listenFor = listenFor  # Maximum number of client will be accepted
        self.__GLOBALEXIT = False     # Global exit status for all thread
        self.__clientFunc = {}        # Functions with repective command for client
        self.__serverFunc = {}        # Functions with repective command for server

        self.__coreThreads = [
            th.Thread(target=self.__makeConnection), # Making connections
        ]

    # Threading - core
    def __makeConnection(self):
        # Keep accept til number of connection exceeded
        while not self.__GLOBALEXIT and len(self.__CONN) < self.__listenFor:
            conn = self.__Socket.accept() # (Socket, IP) of new connection
            self.__CONN.append(conn)      # Append into connection pool

            self.send(conn, b"Connected")
            self.announce(f"Connected to {conn[1][0]}:{conn[1][1]}")
            th.Thread(target=self.__listenClientCommand, args=[conn]).start()

            t.sleep(0.1) # Cooldown

    # Threading - each connection
    def __listenClientCommand(self, conn):
        # Forever listening
        while not self.__GLOBALEXIT:
            command = self.recvObj(conn)

            if command == "__END__":
                conn[0].close()
                self.__CONN.remove(conn)
                break

            self.announce(command.raw, f"client: {conn[1][0]}:{conn[1][1]}")

            if (tmp := self.__clientFunc.get(command.name, None)) is not None:
                # self.announce(command.raw, "DEBUG")
                try:              tmp(conn, *command.args)
                except TypeError: self.send(conn, b"Wrong syntax")

            else: self.send(conn, b"Command not found")

            t.sleep(0.1) # Cooldown

    # Add function for client command to call
    def addclientFunction(self, key):
        def decorator(func):
            self.__clientFunc[key] = func

        return decorator

    # Add function for server command to call
    def addServerFunction(self, key):
        def decorator(func):
            self.__serverFunc[key] = func

        return decorator

    # Start Server
    def start(self):
        self.__Socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.__Socket.bind((self.__IP, self.__PORT))
        self.__Socket.listen(self.__listenFor)

        for i in self.__coreThreads: i.start() # Start all core threads

        while not self.__GLOBALEXIT:
            command = Command(input("> "))
            if (tmp := self.__serverFunc.get(command.name, None)) is not None:
                try:              tmp(*command.args)
                except TypeError: self.announce(b"Wrong syntax")

            else: self.announce(b"Command not found")

            t.sleep(0.1) # Cooldown

        for i in self.__coreThreads: i.join()  # Wait for all core threads finished

    # Kill Server
    def end(self):
        self.__GLOBALEXIT = True
        while self.__CONN:
            self.__CONN.pop(0)[0].close()

        end = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        end.connect((self.__IP, self.__PORT))
        end.close()

    # Announce msg to Client console
    @staticmethod
    def announce(msg, From="System"):
        msg = msg if type(msg) != bytes else msg.decode()
        print(f"[{From}]", msg)

    # Announce respond
    def announceRespond(self, conn):
        tmp = self.recv(conn).decode()
        self.announce(tmp, "Server")
        return tmp

    # Send pickled obj
    def sendObj(self, conn, obj):
        conn[0].sendall(pkl.dumps(obj))

    # Send raw obj
    def send(self, conn, obj):
        conn[0].sendall(obj)

    # Receive pickled obj
    def recvObj(self, conn, bufferSize=32768):
        data = b""

        while 1:
            tmp = conn[0].recv(bufferSize)
            data += tmp

            if len(tmp) < bufferSize: break

        return pkl.loads(data)

    # Receive raw obj
    def recv(self, conn, bufferSize=32768):
        data = b""

        while 1:
            tmp = conn[0].recv(bufferSize)
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

    # Fetch CONN
    @property
    def connections(self):
        return self.__CONN

    # Fetch maximum connections
    @property
    def maxConnection(self):
        return self.__listenFor
