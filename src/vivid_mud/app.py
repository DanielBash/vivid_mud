import inspect
import logging
import threading
from .client import VividClient
from .exceptions import ServerMissing, ClientMissing
from .server import VividServer
from typing import Type
import sys
from textual_serve.server import Server as TextualServer
from ._logging import setup_logging, print_welcome_frase


class VividApp:
    def __init__(
            self,
            name: str = '__main__',
            server_port: int = 18861,
            server_host: str = "localhost",
            web_client_port: int = 8080,
            web_client_host: str = "localhost",
            server: Type[VividServer] = None,
            client: Type[VividClient] = None,
            title: str = "My App",
            module_log: str = 'vivid_mud.log',
            server_log: str = 'server.log',
            serve_log: str = 'serve.log'
    ):

        self.server_host = server_host
        self.server_port = server_port

        self.web_client_host = web_client_host
        self.web_client_port = web_client_port

        self.server = server
        self.client = client

        self.title = title
        self.name = name

        self.serve_log = serve_log
        self.module_log = module_log
        self.server_log = server_log

    def __call__(self, *args, **kwargs):
        self.run()

    def run_server(self):
        self.server().run(host=self.server_host, port=self.server_port)

    def run_client(self):
        file_path = inspect.getfile(self.client)
        name = self.client.__name__

        cmd = f"{sys.executable} -m vivid_mud._runner {file_path}:{name} --port {self.server_port} --host {self.server_host}"

        web = TextualServer(
            cmd,
            host=self.web_client_host,
            port=self.web_client_port,
            title=self.title,
        )

        web.serve()

    def run(self):
        if self.client is None:
            raise ClientMissing("Для приложения не задан клиент.")

        if self.server is None:
            raise ServerMissing("Для приложения не задан сервер.")

        setup_logging(server_log=self.server_log, client_log=self.module_log)

        if self.name == '__main__':
            print_welcome_frase()

            threading.Thread(target=self.run_server, daemon=True).start()
            self.run_client()
