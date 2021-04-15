import socket


def start():
    host = str(input("Enter host: "))
    while True:
        try:
            port = input("Enter port: ")
            assert port.isdigit()
            port = int(port)
            assert 0 < port < 65535
            break
        except AssertionError:
            print("Incorrect port string")

    if host == '' or host is None:
        host = "localhost"

    working_client(host, port)


def working_client(host, port):
    while True:
        request = str(input('>')).strip()

        sock = socket.socket()
        sock.connect((host, port))
        sock.send(request.encode('utf-8'))

        response = sock.recv(1024).decode('utf-8')
        if response == 'end':
            print("Shutdown the system")
            sock.close()
            break

        print(response)

        sock.close()


if __name__ == '__main__':
    start()
