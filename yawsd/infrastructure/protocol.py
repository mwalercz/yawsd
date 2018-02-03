import logging

from autobahn.twisted.websocket import WebSocketClientProtocol
from twisted.internet import task

from yawsd.exceptions import RouteNotFound
from yawsd.infrastructure.controller import Status
from yawsd.infrastructure.serializers import deserialize
from yawsd.infrastructure.system_stat import get_system_info, get_system_stat
from yawsd.infrastructure.utils import clear_passwords_from_message

log = logging.getLogger(__name__)


class WorkerProtocol(WebSocketClientProtocol):
    master_client = NotImplemented
    controller = NotImplemented
    router = NotImplemented
    master_client_lock = NotImplemented
    sending_stats_task = None
    stats_sending_interval = 30  # in seconds

    def onConnect(self, response):
        log.info('Connected to master: %s', self.peer)
        self.factory.resetDelay()

    def onOpen(self):
        self.master_client.master = self
        self.master_client.send(
            action_name='worker_connected',
            body=get_system_info()
        )
        if (
            self.controller.status == Status.BUSY or
            self.controller.status == Status.WAITING_FOR_ACK
        ):
            self.master_client.send(
                action_name='worker_has_work',
                body=self.controller.current_work.to_primitive()
            )
        if self.controller.status == Status.WAITING_FOR_ACK:
            self.master_client.send(**self.controller.work_is_done_msg)

        if self.sending_stats_task and self.sending_stats_task.running:
            self.sending_stats_task.stop()
        self.sending_stats_task = task.LoopingCall(self.send_stats_to_master)
        self.sending_stats_task.start(self.stats_sending_interval)

    def onMessage(self, payload, isBinary):
        message = deserialize(payload)
        log.info('Received message from master: %s', repr(clear_passwords_from_message(message)))
        try:
            responder = self.router.find_responder(message.get('path'))
            responder(message)
        except RouteNotFound as exc:
            log.exception(exc)
        except Exception as exc:
            log.exception(exc)

    def onClose(self, wasClean, code, reason):
        if self.sending_stats_task and self.sending_stats_task.running:
            self.sending_stats_task.stop()
        self.master_client.master = None
        log.info('Disconnected from master, reason: %s, status_code: %s', reason, code)

    def onPing(self, payload):
        log.debug('Received ping from master')
        self.sendPong(payload)

    def send_stats_to_master(self):
        self.master_client.send(
            action_name='worker_system_stat',
            body=get_system_stat()
        )