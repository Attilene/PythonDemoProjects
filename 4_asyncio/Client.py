import asyncio
import sys


async def tcp_echo_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    message = str(input("Enter new message: "))
    if message == "exit":
        sys.exit()

    writer.write(message.encode('utf-8'))
    await writer.drain()

    data = await reader.read(1000)
    writer.close()
    print(f"Server response: {data.decode('utf-8')}")
    await writer.wait_closed()


def start_client():
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
    while True:
        loop.run_until_complete(loop.create_task(tcp_echo_client(host, port)))


if __name__ == "__main__":
    start_client()