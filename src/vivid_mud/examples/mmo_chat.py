import vivid_mud
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Input, Button, Static


class ChatServer(vivid_mud.Server):
    messages = []

    def exposed_send(self, msg: str):
        self.messages.append(msg)

    def exposed_get_messages(self):
        return self.messages


class ChatClient(vivid_mud.Client):
    def compose(self) -> ComposeResult:
        with Center():
            with Vertical():
                yield Static("", id="chat")
                yield Input(placeholder="Type a message...", id="cmd")
                yield Button("Send", id="send")

    def on_mount(self):
        self.set_interval(1, self.refresh_messages)

    def refresh_messages(self):
        messages = self.connection.root.get_messages()
        self.query_one("#chat", Static).update("\n".join(messages))

    def on_button_pressed(self, _event: Button.Pressed) -> None:
        cmd = self.query_one("#cmd", Input)
        if cmd.value.strip():
            self.connection.root.send(cmd.value)
            cmd.value = ""


if __name__ == "__main__":
    vivid_mud.App(server=ChatServer, client=ChatClient, title="MMO Chat").run()
