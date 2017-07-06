from dq_worker.controller import WorkerController


def worker_controller(c):
    return WorkerController(
        master_client=c('master_client'),
        loop=c('loop'),
    )


def register(c):
    c.add_service(worker_controller)
