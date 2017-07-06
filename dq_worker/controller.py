from dq_worker.schema import Work
from dq_worker.components.master_client import MasterClient
from dq_worker.components.validator import validate
from dq_worker.components.worker import Worker


class WorkerController:
    def __init__(
            self, master_client: MasterClient, loop
    ):
        self.master_client = master_client
        self.loop = loop
        self.worker = None
        self.current_task = None

    def work_is_ready(self, message):
        if self.current_task:
            pass
        else:
            self.master_client.send(
                action_name='worker_requests_work',
            )

    def no_work_to_be_done(self, message):
        if self.current_task:
            pass
        else:
            pass

    @validate(schema=Work)
    def work_to_be_done(self, message):
        if self.current_task:
            pass
        else:
            self.worker = Worker(work=message)
            self.current_task = self.loop.run_in_executor(self.worker.do_work)
            self.current_task.add_done_callback(self._work_completed)

    def kill_work(self, message):
        if self.current_task:
            future = self.loop.run_in_executor(self.worker.kill_work)
            self.current_task.remove_done_callback(self._work_completed)
            future.add_done_callback(self._work_was_killed)

    def _work_was_killed(self, future):
        result = future.result()
        if result == 0:
            self.current_task = None
            self.master_client.send(
                action_name='work_is_done',
                body={
                    'work_id': self.worker.work.work_id,
                    'status': 'work_killed',
                }
            )
            self.master_client.send(
                action_name='worker_requests_work'
            )
        else:
            self.master_client.send(
                action_name='work_is_done',
                body={
                    'work_id': self.worker.work.work_id,
                    'status': 'work_not_killed',
                }
            )

    def _work_completed(self, future):
        result = future.result()
        if result['status'] == 0:
            status = 'finished_with_success'
        else:
            status = 'finished_with_failure'
        self.current_task = None
        self.master_client.send(
            action_name='work_is_done',
            body={
                'work_id': self.worker.work.work_id,
                'status': status,
                'output': result['output']
            }
        )
        self.master_client.send(
            action_name='worker_requests_work'
        )

    def clean_up(self):
        if self.current_task:
            self.current_task.remove_done_callback(self._work_completed)
            self.loop.run_in_executor(self.worker.kill_work)
            # self.thread_pool.shutdown(wait=True)
