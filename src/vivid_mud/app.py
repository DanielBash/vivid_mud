import threading
from .client import VividClient
from .exceptions import ServerMissing, ClientMissing
from .server import VividServer
from typing import Type
from textual_serve.server import Server as TextualServer


class VividApp:
    def __init__(self,
                server_port: int = 18861,
                server_host: str = 'localhost',

                web_client_port: int = 8080,
                web_client_host: str = 'localhost',

                server: Type[VividServer] = None,
                client: Type[VividClient] = None,

                title: str = 'Моё приложение'
        ):

        self.server_host = server_host
        self.server_port = server_port

        self.web_client_host = web_client_host
        self.web_client_port = web_client_port

        self.server = server
        self.client = client

        self.title = title

    def __call__(self, *args, **kwargs):
        self.run()

    def run_server(self):
        self.server().run()

    def run_client(self):
        module = self.client.__module__
        name = self.client.__name__

        cmd = f"python -m vivid_mud._runner {module}:{name} --port {self.server_port} --host {self.server_host}"

        web = TextualServer(
            cmd,
            host=self.web_client_host,
            port=self.web_client_port,
            title=self.title,
        )

        web.serve()

    def run(self):
        if self.client is None:
            return ClientMissing(
                'Для данного приложения не задан клиент.'
            )

        if self.server is None:
            return ServerMissing(
                'Для данного приложения не задан сервер.'
            )

        threading.Thread(target=self.run_server, daemon=True).start()
        self.run_client()
