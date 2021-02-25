import socket

sock = socket.socket()

host = str(input("Enter host: "))
while True:
    port = int(input("Enter port: "))
    if 0 < port < 65535:
        break
    else:
        print("Incorrect port string")

if host == '' or host is None:
    host = "localhost"

sock.connect((host, port))
print("Connected to the server")

while True:
    mes = str(input())
    sock.send(mes.encode('utf-8'))
    print("Send message to the server: " + mes)
    data = sock.recv(1024).decode('utf-8')
    print("Receive message from the server: " + data)
    if data == "end":
        break

sock.close()
print("Server disconnected")