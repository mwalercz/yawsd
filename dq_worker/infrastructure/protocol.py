import logging

from autobahn.twisted.websocket import WebSocketClientProtocol

from dq_worker.exceptions import RouteNotFound
from dq_worker.infrastructure.serializers import deserialize

log = logging.getLogger(__name__)


class WorkerProtocol(WebSocketClientProtocol):
    master_client = NotImplemented
    locked_master_client = NotImplemented
    controller = NotImplemented
    router = NotImplemented
    master_client_lock = NotImplemented
    system_stat_gatherer = NotImplemented

    def onConnect(self, response):
        log.info('Connected to master: %s', self.peer)
        self.factory.resetDelay()

    def onOpen(self):
        self.master_client.master = self
        self.master_client.send(
            action_name='worker_connected',
        )
        if self.controller.current_work:
            self.master_client.send(
                action_name='worker_has_work',
                body=self.controller.current_work.to_primitive()
            )

        self.locked_master_client.master = self
        if self.master_client_lock.locked:
            self.master_client_lock.release()

    def onMessage(self, payload, isBinary):
        message = deserialize(payload)
        log.info(message)
        try:
            responder = self.router.find_responder(message.get('path'))
            responder(message)
        except RouteNotFound as exc:
            log.exception(exc)
        except Exception as exc:
            log.exception(exc)

    def onClose(self, wasClean, code, reason):
        self.master_client_lock.acquire()
        self.master_client.master = None
        self.locked_master_client.master = None
        log.info('Reason: %s, status_code: %s', reason, code)

    def onPing(self, payload):
        stat = self.system_stat_gatherer.get_system_stat()
        self.sendPong(deserialize(stat))
