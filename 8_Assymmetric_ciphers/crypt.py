import key
import random


def create_param(start=10000, end=1000000) -> int:
    return random.randint(start, end)


def write_key(path: str, params: list):
    file = open(path, 'w')
    for param in params:
        file.write(str(param) + '\n')
    file.close()


def read_key(path: str) -> str:
    ans = ""
    file = open(path, 'r')
    for line in file:
        ans += line
    file.close()
    return ans


def create_sym_key(ab: int, AB: int, p: int) -> int:
    return round(AB ** ab % p)


def cipher(key: str, text: str) -> str:
    return "".join(map(lambda k, c: chr((ord(c) ^ ord(k)) % 65536), __repeat_gen(key), text))


def __repeat_gen(chars: str):
    while True:
        for i in chars:
            yield i
