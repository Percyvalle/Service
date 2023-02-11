import socket
import socketserver
import configparser
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
        self._SERVER_SOCKET.close()


if __name__ == '__main__':
    socket_server = SocketService()
