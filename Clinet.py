import socket


IP = "127.0.0.1"
PORT = 8080

CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONN.connect((IP, PORT))

# tell if connected
print(CONN.recv(1024))

while True:
    command = input(": ")
    _command = command.split(" ")

    CONN.sendall(command.encode()) # send command
    if command == "quit": break

    respond = CONN.recv(1024) # recv respond
    print(f"[Server] {respond}")

    if _command[0] == "play" and respond == b"File found":
        length = CONN.recv(1024)
        index = 1

        CONN.sendall(b"req")
        while (data := CONN.recv(5*1024*1024)) != b"EOF":
            with open(f"{index}.mp4", "wb") as f:
                f.write(data)
                index += 1

            CONN.sendall(b"req")

