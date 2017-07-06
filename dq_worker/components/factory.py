from autobahn.asyncio import WebSocketClientFactory


class WorkerFactory(WebSocketClientFactory):
    def __init__(self, wss_uri, headers):
        WebSocketClientFactory.__init__(self, wss_uri, headers=headers)
