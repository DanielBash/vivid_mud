from textual.app import App
import rpyc


class VividClient(App):
    def __init__(self, host, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = port
        self.host = host
        self.conn = rpyc.connect(host, port)