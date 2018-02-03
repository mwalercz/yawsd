import logging

from enum import Enum
from twisted.internet import defer
from twisted.internet import threads

from yawsd.infrastructure.validator import validate
from yawsd.schema import Work


log = logging.getLogger(__name__)


class Status(Enum):
    FREE = 'FREE'
    BUSY = 'BUSY'
    WAITING_FOR_ACK = 'WAITING_FOR_ACK'


class WorkerController:
    def __init__(
            self, master_client, worker_factory
    ):
        self.master_client = master_client
        self.worker_factory = worker_factory
        self.status = Status.FREE
        self.worker = None
        self.deferred_task = None
        self.current_work = None
        self.work_is_done_msg = None

    @defer.inlineCallbacks
    def work_is_ready(self, message):
        if self.status == Status.FREE:
            yield self.master_client.send(
                action_name='worker_requests_work',
            )

    @validate(schema=Work)
    def work_to_be_done(self, message):
        if self.status == Status.FREE:
            self.status = Status.BUSY
            self.current_work = message
            self.worker = self.worker_factory.get(work=self.current_work)
            self.deferred_task = threads.deferToThread(self.worker.do_work)
            self.deferred_task.addCallback(self.work_completed)

    def cancel_work(self, message):
        if self.status == Status.BUSY:
            d = threads.deferToThread(self.worker.kill_work)
            d.addCallback(self.work_killed)
            self.deferred_task.callbacks = []

    @defer.inlineCallbacks
    def work_is_done_ack(self, message):
        if self.status == Status.WAITING_FOR_ACK:
            self.deferred_task = None
            self.current_work = None
            self.work_is_done_msg = None
            self.status = Status.FREE
            yield self.master_client.send(
                action_name='worker_requests_work'
            )

    @defer.inlineCallbacks
    def work_killed(self, result):
        self.status = Status.WAITING_FOR_ACK
        if result == 0:
            self.work_is_done_msg = dict(
                action_name='work_is_done',
                body={
                    'work_id': self.current_work.work_id,
                    'status': 'CANCELLED',
                }
            )
        else:
            log.error('Unable to kill work, work_id %s', self.current_work.work_id)
        self.master_client.send(**self.work_is_done_msg)

    @defer.inlineCallbacks
    def work_completed(self, result):
        self.status = Status.WAITING_FOR_ACK
        self.work_is_done_msg = dict(
            action_name='work_is_done',
            body={
                'work_id': self.current_work.work_id,
                'status': 'FINISHED',
                'output': result['output'],
                'exit_code': result['exit_code']
            }
        )
        yield self.master_client.send(**self.work_is_done_msg)

    def clean_up(self):
        if self.deferred_task:
            self.deferred_task.callbacks = []
            threads.deferToThread(self.worker.kill_work)
