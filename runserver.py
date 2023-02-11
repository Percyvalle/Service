import socket
import socketserver
import configparser
import asyncio
import os



class SocketService:
    def __init__(self):
        # Путь до конфигурационного файла сервера.
        # Должен находиться в переменной среды PATH_SERVER_CONFIG.
        self._PATH_SERVER_CONFIG = os.environ.get("PATH_SERVER_CONFIG")

        # Чтение конфигурационного файла.
        self._SERVER_CONFIG = configparser.ConfigParser()
        self._SERVER_CONFIG.read(self._PATH_SERVER_CONFIG, "UTF-8")

        # Инициализация серверного сокета.
        # Адрес и порт берется из конфигурационного файла.
        self._SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._SERVER_SOCKET.bind((self._SERVER_CONFIG.get("SERVER", "ADDRESS"),
                                  self._SERVER_CONFIG.getint("SERVER", "PORT")))
        self._SERVER_SOCKET.listen(5)
        self._SERVER_SOCKET.setblocking(False)

        self._LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(self._LOOP)
        self._LOOP.run_until_complete(self.waiting_accept())

    async def handle_connection(self, socket_c, address_c):
        request = (await self._LOOP.sock_recv(socket_c, 1024)).decode("utf-8")
        try:
            while request != 'quit':
                request = (await self._LOOP.sock_recv(socket_c, 255)).decode('utf8')
                if not request:
                    break
                print(request)
        except:
            self._SERVER_SOCKET.close()

    async def waiting_accept(self):
        while True:
            socket_c, address_c = await self._LOOP.sock_accept(self._SERVER_SOCKET)
            self._LOOP.create_task(self.handle_connection(socket_c, address_c))


if __name__ == '__main__':
    socket_server = SocketService()
