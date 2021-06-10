import os
import socket

HOST = "localhost"
PORT = 8080
MAX_REQ_SIZE = 8192
CHARSET = 'UTF-8'  # Кодировка файла
WORK_DIRECTORY = os.getcwd()  # Папка, из которой скачиваются файлы
SEPARATOR = "\r\n"


class Response:  # Класс для создания ответа на запрос
    def __init__(
            self,
            protocol: str = "HTTP/1.1",
            code: int = 200,
            status: str = "OK",
            headers: dict = None,
            body: str = ""
    ):
        self.protocol = protocol
        self.code = code
        self.status = status
        self.headers = headers
        if self.headers is None:
            self.headers = dict()
        self.body = body

    def concatenating(self) -> str:  # Создание ответа на запрос
        try:
            ans = list()
            ans.append(f'{self.protocol} {self.code} {self.status}')
            ans.append(SEPARATOR.join(map(lambda k, v: f'{k}: {v}', self.headers.keys(), self.headers.values())))
            ans.append(SEPARATOR)
            ans.append(self.body)
            return SEPARATOR.join(ans)
        except TypeError:
            return ""


class Request:  # Класс для принятия запроса на сервер
    def __init__(
            self,
            method: str = "GET",
            url: str = "/",
            protocol: str = "HTTP/1.1",
            headers: dict = None,
            body: str = ""
    ):
        self.headers = headers
        if self.headers is None:
            self.headers = dict()
        self.method = method
        self.url = url
        self.protocol = protocol
        self.body = body

    @staticmethod
    def parse(request: str):  # Парсинг запроса
        try:
            ans = request.split(SEPARATOR)
            method, url, protocol = ans.pop(0).split()
            body_sep = ans.index("")
            headers = dict()
            for row in ans[:body_sep]:
                k, v = row.split(": ", 1)
                headers.update({k: v})
            body = SEPARATOR.join(ans[body_sep + 1:])
            return Request(method, url, protocol, headers, body)
        except ValueError:
            return None


def read_file(path: str) -> str:  # Считывание данных из файла
    response = ""
    if os.path.isfile(path):
        file = open(path, 'r')
        for line in file:
            response += line
    return response


def start_web_server():
    sock = socket.socket()
    sock.bind((HOST, PORT))  # Создаем сокет для принятия запросов
    sock.listen(1000)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(MAX_REQ_SIZE)  # Получаем запрос на сервер
        msg = data.decode(CHARSET)
        req = Request.parse(msg)
        body = None
        if req is not None:  # Формируем ответ на запрос
            code = 200
            status = 'OK'
            body = read_file(WORK_DIRECTORY + req.url.replace('/', '\\'))
        else:
            code = 404
            status = 'NOT_FOUND'
        response = Response(
            code=code,
            status=status,
            headers={"Content-type": f"text/html;charset={CHARSET}"},
            body=body
        )
        conn.send(response.concatenating().encode(CHARSET))  # Отправляем ответ на запрос
        conn.close()


if __name__ == '__main__':
    start_web_server()

