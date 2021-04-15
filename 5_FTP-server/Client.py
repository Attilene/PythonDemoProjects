import socket
import os


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
        request = str(input('> ')).strip()

        sock = socket.socket()
        sock.connect((host, port))

        if 'upl' in request:
            request = uploadFile(request)
        sock.send(request.encode('utf-8'))

        response = sock.recv(1024).decode('utf-8')
        if response == 'end':
            print("Shutdown the system")
            sock.close()
            break

        if 'dnl' in request:
            downloadFile(request.split()[1], response)
        else:
            print(response)

        sock.close()


errors = [
        "Directory is not exist!",
        "Path is not exist!",
        "Going outside the file system border!"
    ]


def downloadFile(name, response):
    no_errors = True
    for error in errors:
        if error in response:
            print(error)
            no_errors = False
    if no_errors:
        with open(name, "w") as file:
            file.write(response)
            file.close()
        print('File downloaded')


def uploadFile(request) -> str:
    text = ""
    path = os.path.abspath(os.path.join(os.getcwd(), request.split()[1]))
    if not os.path.exists(path):
        print("File is not exist!")
    if not os.path.isfile(path):
        print("Path is not exist!")
    else:
        file = open(path, "r")
        for line in file:
            text += line
        file.close()
    return request + " \"" + text + "\""


if __name__ == '__main__':
    start()
