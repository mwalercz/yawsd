import logging

from autobahn.asyncio import WebSocketClientProtocol

log = logging.getLogger(__name__)


class WorkerProtocol(WebSocketClientProtocol):
    serializer = NotImplemented
    deserializer = NotImplemented
    master_client = NotImplemented
    router = NotImplemented

    def onConnect(self, response):
        log.info('Connected to master: %s', self.peer)
        self.master_client.master = self

    def onOpen(self):
        self.master_client.send(
            action_name='worker_connected',
        )

    def onMessage(self, payload, isBinary):
        message = self.deserializer.deserialize(payload)
        log.info(message)
        controller, responder = self.router.find_responder(message['path'])
        responder(message)

    def onClose(self, wasClean, code, reason):
        log.info('Reason: %s, status_code: %s', reason, code)
