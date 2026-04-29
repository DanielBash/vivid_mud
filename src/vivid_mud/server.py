import rpyc
from rpyc.utils.server import ThreadedServer
import logging

logger = logging.getLogger('server_log')


class VividServer(rpyc.Service):
    def vivid_log(self, text):
        logger.info(text)

    def on_connect(self, conn):
        self.vivid_log('К серверу подключен клиент')

    def on_disconnect(self, conn):
        self.vivid_log('Клиент отключен')

    def run(self, host="localhost", port=18861):
        server = ThreadedServer(self.__class__, port=port, hostname=host)
        server.start()

    def exposed_ping(self):
        return "pong"
