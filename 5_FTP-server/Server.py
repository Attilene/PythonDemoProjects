import socket
import os
from config import Config
from commands import *


class Parse:
    def __init__(self):
        os.chdir(DIR)
        self.cmd = dict()
        self.cur_dir = []
        self.command = ""

    def readConsole(self, request):
        self.cur_dir = (Config.DIR.split('/')[-1] + os.getcwd().split(f"{Config.DIR.split('/')[-1]}")[-1])
        self.command = request
        res_args = []
        res_cmd, *args = self.command.split(" ", 1)
        res_flags = set()
        if len(args) > 0:
            args = args[0]
            if args.count("\"") % 2 != 0:
                raise TypeError
            q = False
            for item in args.split("\""):
                if q:
                    res_args.append(item)
                else:
                    for arg in item.split():
                        if arg[0] == "-":
                            res_flags.add(arg)
                        else:
                            res_args.append(arg)
                q = not q
        self.cmd = {"command": res_cmd, "arguments": res_args, "flags": res_flags}

    def execute(self) -> str:
        try:
            return eval(f'{Config.COMMANDS[self.cmd["command"]]}')(*self.cmd["arguments"], flags=self.cmd["flags"])
        except KeyError:
            return "Command does not exist!"
        except NameError:
            return "Command does not exist!"
        except TypeError:
            return "Incorrect number of parameters passed!"
        except FileNotFoundError:
            return "File or directory does not exist!"
        except FileExistsError:
            return "Directory is already exists!"


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

    working_server(host, port)


def working_server(host: str, port: int):
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen()

    file_manager = Parse()
    print("Start the coolest file manager!")
    while True:
        conn, addr = sock.accept()

        request = conn.recv(1024).decode('utf-8')
        if request == "end":
            conn.send("end".encode('utf-8'))
            break
        print(request)

        file_manager.readConsole(request)
        response = file_manager.execute()
        conn.send(response.encode('utf-8'))

    conn.close()


if __name__ == '__main__':
    start()