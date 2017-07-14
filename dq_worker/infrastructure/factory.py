from autobahn.twisted.websocket import WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory


class WorkerFactory(WebSocketClientFactory, ReconnectingClientFactory):
    def __init__(self, url, headers):
        WebSocketClientFactory.__init__(self, url, headers=headers)

    def clientConnectionFailed(self, connector, reason):
        print("Client connection failed .. retrying ..")
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        print("Client connection lost .. retrying ..")
        self.retry(connector)
