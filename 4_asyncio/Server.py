import asyncio
import logging

logging.basicConfig(filename="asyncio.log", level=logging.INFO)


async def handle_echo(reader, writer):
    data = await reader.read(1000)
    message = data.decode('utf-8')
    logging.info(message)

    writer.write(data)
    await writer.drain()

    writer.close()


def start_server():
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

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, host, port, loop=loop)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    start_server()