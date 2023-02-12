from twisted.internet import protocol, reactor
from twisted.python import failure
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint
import configparser
import json
import os

# Путь до конфигурационного файла сервера.
# Должен находиться в переменной среды PATH_SERVER_CONFIG.
PATH_SERVER_CONFIG = os.environ.get("PATH_SERVER_CONFIG")

# Чтение конфигурационного файла.
SERVER_CONFIG = configparser.ConfigParser()
SERVER_CONFIG.read(PATH_SERVER_CONFIG, "UTF-8")


class GameService(protocol.Protocol):
    def __init__(self, list_client, id_client):
        self.id_client = id_client
        self.list_client = list_client

    def connectionMade(self):
        self.list_client[self.id_client] = self
        print("Connection: " + str(self.id_client))

    def connectionLost(self, reason: failure.Failure = connectionDone):
        del self.list_client[self.id_client]

    def dataReceived(self, data: bytes):
        try:
            data = json.loads(data.decode("utf-8"))
        except UnicodeDecodeError:
            self.sendMessage(b"Cannot decode, use utf-8")
            return
        except json.JSONDecodeError:
            self.sendMessage(b"Cannot decode, use json")
            return

        self.sendMessage(b"Hello")
    def sendMessage(self,  data: bytes):
        self.transport.write(data)

class SrvFactory(ServerFactory):
    def __init__(self):
        self.list_client = dict()
        self.id_client = 0

    def buildProtocol(self, addr):
        self.id_client += 1
        return GameService(self.list_client, self.id_client)

if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, SERVER_CONFIG.getint("SERVER", "PORT"))
    endpoint.listen(SrvFactory())
    reactor.run()
