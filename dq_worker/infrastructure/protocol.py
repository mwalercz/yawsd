import logging

from autobahn.twisted.websocket import WebSocketClientProtocol

from dq_worker.exceptions import RouteNotFound
from dq_worker.infrastructure.serializers import deserialize
from dq_worker.infrastructure.system_stat import get_system_info, get_system_stat

log = logging.getLogger(__name__)


class WorkerProtocol(WebSocketClientProtocol):
    master_client = NotImplemented
    locked_master_client = NotImplemented
    controller = NotImplemented
    router = NotImplemented
    master_client_lock = NotImplemented

    def onConnect(self, response):
        log.info('Connected to master: %s', self.peer)
        self.factory.resetDelay()

    def onOpen(self):
        self.master_client.master = self
        self.master_client.send(
            action_name='worker_connected',
            body=get_system_info()
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
        log.info('Received ping from master')
        self.sendPong(payload)
        self.master_client.send(
            action_name='worker_system_stat',
            body=get_system_stat()
        )
