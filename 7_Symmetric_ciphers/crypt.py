import math
import random as rnd


def __rnd_key(length: int) -> str:
    return "".join((chr(rnd.randint(0, 65535)) for _ in range(length)))


def __repeat_gen(chars: str):
    while True:
        for i in chars:
            yield i


def cesar_encrypt(text: str, offset: int) -> str:
    return "".join(map(lambda c: chr((ord(c) + offset) % 65536), text))


def cesar_decrypt(crypted: str) -> str:
    chars = {c: crypted.count(c) for c in set(crypted)}
    return cesar_encrypt(crypted, ord(' ') - ord(max(chars, key=chars.get)))


def vigner(text: str, key: str) -> str:
    return "".join(map(lambda k, c: chr((ord(c) ^ ord(k)) % 65536), __repeat_gen(key), text))


def vernam(text: str, key: str) -> str:
    return "".join(map(lambda k, c: chr(ord(c) ^ ord(k)), text, __repeat_gen(key)))


def otp(text: str) -> tuple[str, str]:
    key = __rnd_key(len(text))
    return vernam(text, key), key


def blockchain(text: str, func: callable, key, block_len: int = 5) -> tuple[str, str]:
    res = []
    v = __rnd_key(block_len)
    blocks = [text[i:i+block_len] for i in range(0, len(text), block_len)]
    res.append(func(vernam(blocks.pop(0), v), key))
    while len(blocks) > 0:
        res.append(func(vernam(blocks.pop(0), res[-1]), key))
    return "".join(res), v


def blockchain_rev(text: str, v: str, de_func: callable, key, block_len: int = 5) -> str:
    res = []
    blocks = [text[i:i+block_len] for i in range(0, len(text), block_len)]
    while len(blocks) > 1:
        res.append(vernam(de_func(blocks.pop(-1), key), blocks[-1]))
    res.append(vernam(de_func(blocks.pop(-1), key), v))
    return "".join(reversed(res))


def feistel_cell(text: str, func: callable, K) -> str:
    sep = math.ceil(len(text) / 2)
    L = text[:sep]
    R = text[sep:]
    return R + vernam(func(L, K), R)


def feistel_cell_rev(text: str, de_func: callable, K) -> str:
    sep = math.ceil(len(text) / 2)
    L = text[:sep]
    R = text[sep:]
    return de_func(vernam(R, L), K) + L


def feistel_web(crypted: str, func: callable, K, iterations: int) -> str:
    for _ in range(iterations):
        crypted = feistel_cell(crypted, func, K)
    return crypted


def feistel_web_rev(crypted: str, de_func: callable, K, iterations: int) -> str:
    for _ in range(iterations):
        crypted = feistel_cell_rev(crypted, de_func, K)
    return crypted


if __name__ == "__main__":
    pass
