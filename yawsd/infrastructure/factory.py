import logging

from autobahn.twisted.websocket import WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory

log = logging.getLogger(__name__)


class DqWorkerFactory(WebSocketClientFactory, ReconnectingClientFactory):
    def __init__(self, url, headers):
        WebSocketClientFactory.__init__(self, url, headers=headers)

    def clientConnectionFailed(self, connector, reason):
        log.info("Client connection failed .. retrying ..")
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        log.info("Client connection lost .. retrying ..")
        self.retry(connector)
