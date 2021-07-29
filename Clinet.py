import socket


IP = "127.0.0.1"
PORT = 8080

clinetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clinetSocket.connect((IP, PORT))

print(clinetSocket.recv(1024))

while True:
    tmp = input(": ")

    clinetSocket.sendall(tmp.encode())

    if tmp == "q":
        break
