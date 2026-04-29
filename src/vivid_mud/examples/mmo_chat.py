import datetime
import vivid_mud
from textual.app import ComposeResult
from textual.containers import Center, Vertical, Middle, Horizontal
from textual.widgets import Input, Button, Static, TextArea, Markdown


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
    CSS = """
    #chat {
        height: 1fr;
        overflow-y: auto;
        padding: 1;
    }

    #input_row {
        height: auto;
    }

    #cmd {
        width: 1fr;
    }

    Button {
        width: auto;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Markdown("", id="chat")
            with Horizontal(id="input_row"):
                self.input_message = TextArea(
                    placeholder="Введите сообщение...",
                    id="cmd",
                )
                self.input_message.language = "markdown"
                yield self.input_message
                yield Button("Отправить", id="send")

    def on_mount(self):
        self.query_one("#cmd", TextArea).styles.height = 3
        self.set_interval(0.1, self.refresh_messages)

    def refresh_messages(self):
        messages = self.connection.root.get_messages()

        content = "\n\n".join(
            f"**{x['time']}** {x['message']}"
            for x in messages
        )

        self.query_one("#chat", Markdown).update(content)

    def on_button_pressed(self, _event: Button.Pressed) -> None:
        cmd = self.query_one("#cmd", TextArea)
        if cmd.text.strip():
            self.connection.root.send(cmd.text)
            cmd.text = ""

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        textarea = event.text_area

        lines = textarea.text.count("\n") + 3
        lines = min(lines, 8)

        textarea.styles.height = lines


vivid_mud.App(__name__, server=ChatServer, client=ChatClient, title="Онлайн чат").run()
