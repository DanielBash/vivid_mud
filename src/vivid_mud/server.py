import rpyc
from rpyc.utils.server import ThreadedServer


class VividServer(rpyc.Service):
    def on_connect(self, conn):
        print("Клиент подключен")

    def on_disconnect(self, conn):
        print("Клиент отключен")

    def exposed_ping(self):
        return "pong"

    def run(self, host="localhost", port=18861):
        server = ThreadedServer(self.__class__, port=port, hostname=host)
        server.start()