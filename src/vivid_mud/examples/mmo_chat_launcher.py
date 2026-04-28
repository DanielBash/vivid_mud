import vivid_mud
from vivid_mud.examples.mmo_chat_server import Server
from vivid_mud.examples.mmo_chat_client import Client

vivid_mud.app.VividApp(
    server=Server,
    client=Client,
).run()