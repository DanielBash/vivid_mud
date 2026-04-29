import logging
import pathlib


def setup_logging(client_log, server_log):
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    client_logger = logging.getLogger("client_log")
    client_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(client_log)
    file_handler.setFormatter(fmt)
    client_logger.addHandler(file_handler)
    client_logger.propagate = False

    server_logger = logging.getLogger("server_log")
    server_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(server_log)
    file_handler.setFormatter(fmt)
    server_logger.addHandler(file_handler)
    server_logger.propagate = False

def print_welcome_frase(file_path='banner.txt'):
    print((pathlib.Path(__file__).parent / pathlib.Path(f'assets/{file_path}')).read_text())