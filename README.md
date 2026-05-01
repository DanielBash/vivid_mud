![image](https://github.com/DanielBash/vivid_mud/blob/main/.github/banner.png?raw=true)

# vivid-mud

Репозиторий разработки пакета pypi - vivid-mud. Участие в проекте приветствуется.
На данный момент актуальной документации не доступно.

## Установка
```bash
pip install vivid_mud
```

## Использование

> Пример простого работающего онлайн-чата

```python
import vivid_mud
from textual.app import ComposeResult
from textual.containers import Center
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
            yield Static("", id="chat")
            yield Input(placeholder="Введите сообщение...", id="cmd")
            yield Button("Отправить", id="send")

    def on_mount(self):
        self.set_interval(0.1, self.refresh_messages)

    def refresh_messages(self):
        messages = self.connection.root.get_messages()
        self.query_one("#chat", Static).update("\n".join(messages))

    def on_button_pressed(self, _event: Button.Pressed) -> None:
        cmd = self.query_one("#cmd", Input)
        self.connection.root.send(cmd.value)
        cmd.value = ""

        
    vivid_mud.App(__name__, server=ChatServer, client=ChatClient, title="Онлайн чат").run()
```

Модуль еще в разработке.
