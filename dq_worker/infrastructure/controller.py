from twisted.internet import defer
from twisted.internet import threads

from dq_worker.infrastructure.validator import validate
from dq_worker.schema import Work


class WorkerController:
    def __init__(
            self, master_client, worker_factory
    ):
        self.master_client = master_client
        self.worker_factory = worker_factory
        self.worker = None
        self.deferred_task = None
        self.current_work = None

    @defer.inlineCallbacks
    def work_is_ready(self, message):
        if self.deferred_task:
            pass
        else:
            yield self.master_client.send(
                action_name='worker_requests_work',
            )

    @validate(schema=Work)
    def work_to_be_done(self, message):
        if self.deferred_task:
            pass
        else:
            self.current_work = message
            self.worker = self.worker_factory.get(work=self.current_work)
            self.deferred_task = threads.deferToThread(self.worker.do_work)
            self.deferred_task.addCallback(self._work_completed)

    def kill_work(self, message):
        if self.deferred_task:
            d = threads.deferToThread(self.worker.kill_work)
            d.addCallback(self._work_was_killed)
            self.deferred_task.callbacks = []

    @defer.inlineCallbacks
    def _work_was_killed(self, result):
        if result == 0:
            yield self.master_client.send(
                action_name='work_is_done',
                body={
                    'work_id': self.current_work.work_id,
                    'status': 'killed',
                }
            )
            self.deferred_task = None
            self.current_work = None
            yield self.master_client.send(
                action_name='worker_requests_work'
            )
        else:
            yield self.master_client.send(
                action_name='work_is_done',
                body={
                    'work_id': self.current_work.work_id,
                    'status': 'work_not_killed',
                }
            )

    @defer.inlineCallbacks
    def _work_completed(self, result):
        if result['status'] == 0:
            status = 'finished_with_success'
        else:
            status = 'finished_with_failure'
        yield self.master_client.send(
            action_name='work_is_done',
            body={
                'work_id': self.current_work.work_id,
                'status': status,
                'output': result['output']
            }
        )
        self.deferred_task = None
        self.current_work = None
        yield self.master_client.send(
            action_name='worker_requests_work'
        )

    def clean_up(self):
        if self.deferred_task:
            self.deferred_task.callbacks = []
            threads.deferToThread(self.worker.kill_work)
