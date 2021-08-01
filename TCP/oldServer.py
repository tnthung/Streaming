import time
import pickle
import socket
import threading

from .Common import Command


class Server(object):
    def __init__(self, IP="127.0.0.1", PORT=8080, listenFor=10):
        self.IP = IP                # IP address
        self.CONN = []              # All connections
        self.PORT = PORT            # Port listen on
        self.listenFor = listenFor  # Maximum number of clinet will be accepted
        self.GLOBALEXIT = False     # Global exit status for all thread
        self.clinetFunc = {}        # Functions with repective command for clinet
        self.serverFunc = {}        # Functions with repective command for server

        # Core threads to start
        self.coreThreads = [
            threading.Thread(target=self.__makeConnection), # Making Connections
        ]

    # Threading - core
    def __makeConnection(self):
        # Keep accept til number of connection exceeded
        while not self.GLOBALEXIT and len(self.CONN) < self.listenFor:
            conn = self.Socket.accept()
            self.CONN.append(conn)

            conn[0].sendall(b"Connected",)
            self.announce("Connected")
            threading.Thread(target=self.__listenClientCommand, args=[conn]).start()

            time.sleep(0.1) # Cooldown

    # Threading - each connection
    def __listenClientCommand(self, conn):
        # Forever listening
        while not self.GLOBALEXIT:
            command = pickle.loads(conn[0].recv(10240))

            if command == "__END__":
                conn[0].close()
                self.__removeConnection(conn)
                break

            self.announce(command.raw, As=f"Clinet: {conn[1]}")

            if (tmp := self.clinetFunc.get(command.split[0], None)) is not None:
                self.announce(command.raw, As="DEBUG")
                try:              tmp(*conn, *command.split[1:])
                except TypeError: conn[0].sendall(b"Wrong syntax")

            else: conn[0].sendall(b"Command not found")

            time.sleep(0.1) # Cooldown

    # Remove disconnected socket
    def __removeConnection(self, conn):
        for i, j in enumerate(self.CONN):
            if j[1] == conn[1]:
                self.CONN.pop(i)
                break        

    # Print formated message
    @staticmethod
    def announce(msg, As="System"):
        print(f"[{As}]", (msg if type(msg) != bytes else msg.decode()))

    # Add function for clinet command to call
    def addClinetFunction(self, key):
        def decorator(func):
            self.clinetFunc[key] = func

        return decorator

    # Add function for server command to call
    def addServerFunction(self, key):
        def decorator(func):
            self.serverFunc[key] = func

        return decorator

    def start(self):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((self.IP, self.PORT))
        self.Socket.listen(self.listenFor)

        for i in self.coreThreads: i.start() # Start all core threads

        while not self.GLOBALEXIT:
            command = input("> ").split(" ")
            if (tmp := self.serverFunc.get(command[0], None)) is not None:
                try:              tmp(*command[1:])
                except TypeError: self.announce(b"Wrong syntax", As="Server")

            else: self.announce(b"Command not found", As="Server")

            time.sleep(0.1) # Cooldown

        for i in self.coreThreads: i.join()  # Wait for all core threads finished
            

    def end(self):
        self.GLOBALEXIT = True
        while self.CONN:
            self.CONN.pop(0)[0].close()
        
        end = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        end.connect((self.IP, self.PORT))
        end.close()


if __name__ == "__main__":
    Server().start()
