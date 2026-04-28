# vivid_mud/examples/mmo_chat_client.py

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Input, Button, Static
from textual.reactive import reactive
import vivid_mud
import rpyc


class Client(vivid_mud.client.VividClient):
    messages = reactive([])

    def on_mount(self):
        # connect to server
        self.conn = rpyc.connect("localhost", self.port)

        # poll messages every 1 second
        self.set_interval(1, self.refresh_messages)

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical():
                yield Static("", id="chat")
                yield Input(placeholder="Введите сообщение...", id="cmd")
                yield Button("Отправить", id="send")

    def refresh_messages(self):
        self.messages = self.conn.root.get_messages()
        chat = self.query_one("#chat", Static)
        chat.update("\n".join(self.messages))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        value = self.query_one("#cmd", Input).value

        if value.strip():
            self.conn.root.send(value)
            self.query_one("#cmd", Input).value = ""