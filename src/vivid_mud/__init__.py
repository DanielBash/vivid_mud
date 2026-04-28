"""Фреймворк для создания текстовых онлайн рпг дял браузера."""

from .server import VividServer as Server
from .client import VividClient as Client
from .app import VividApp as App
from . import exceptions
