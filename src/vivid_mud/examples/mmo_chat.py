import datetime

import vivid_mud
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Input, Button, Static


class ChatServer(vivid_mud.Server):
    messages = []

    def exposed_send(self, msg: str):
        send_time = datetime.datetime.time(datetime.datetime.now()).replace(microsecond=0)
        self.messages.append({
            'time': send_time,
            'message': msg
        })

    def exposed_get_messages(self):
        return self.messages


class ChatClient(vivid_mud.Client):
    def compose(self) -> ComposeResult:
        with Center():
            with Vertical():
                yield Static("", id="chat")
                yield Input(placeholder="Введите сообщение...", id="cmd")
                yield Button("Отправить", id="send")

    def on_mount(self):
        self.set_interval(0.1, self.refresh_messages)

    def refresh_messages(self):
        messages = self.connection.root.get_messages()
        self.query_one("#chat", Static).update("\n".join(map(lambda x: f'{x['time']} {x['message']}', messages)))

    def on_button_pressed(self, _event: Button.Pressed) -> None:
        cmd = self.query_one("#cmd", Input)
        if cmd.value.strip():
            self.connection.root.send(cmd.value)
            cmd.value = ""


if __name__ == "__main__":
    vivid_mud.App(server=ChatServer, client=ChatClient, title="Онлайн чат").run()
