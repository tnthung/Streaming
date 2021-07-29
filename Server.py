import socket


IP = "127.0.0.1"
PORT = 8080

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((IP, PORT))
serverSocket.listen(10)

print(f"Listening {IP=}, {PORT=}")


alive = True
CONN, ADDR = serverSocket.accept()

CONN.sendall(b"Connected")

while alive:
    tmp = CONN.recv(1024)

    print(tmp)

    if tmp == b"q":
        alive = False

CONN.close()

