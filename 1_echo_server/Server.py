import socket
import logging

logging.basicConfig(filename="echo.log", level=logging.INFO)


def check_name(addr):
    with open("client_name.txt", "r") as f:
        for line in f:
            if f"{addr[0]}:{addr[1]}" in line:
                return 1


def write_name():
    pass


sock = socket.socket()
logging.info("Server is started")

host = str(input("Enter host: "))
while True:
    port = int(input("Enter port: "))
    if 0 < port < 65535:
        try:
            sock.bind((host, port))
            break
        except OSError:
            logging.error(f"Port {port} in used")
    else:
        logging.warning("Incorrect port string")

if host == '' or host is None:
    host = "localhost"

while True:
    sock.listen(1)
    logging.info("Listening port " + str(port))
    conn, addr = sock.accept()
    print(conn)
    print(addr)
    logging.info("Client connected")
    while True:
        data = conn.recv(1024).decode('utf-8')
        logging.info("Receive message from the client: " + data)
        if data == "end":
            conn.send("end".encode('utf-8'))
            logging.info("Disconnect the client")
            break
        conn.send(data.upper().encode('utf-8'))
        logging.info("Send message to the client: " + data)
    conn.close()

sock.close()
logging.info("Stop the server")
