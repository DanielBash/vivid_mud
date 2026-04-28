import vivid_mud
import rpyc


class Server(vivid_mud.server.VividServer, rpyc.Service):
    messages = []

    def exposed_send(self, msg: str):
        self.messages.append(msg)
        return True

    def exposed_get_messages(self):
        return self.messages