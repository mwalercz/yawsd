import functools
import logging
import signal

from dq_worker.dependencies.container import register
from knot import Container


def make_app(config_path):
    logging.basicConfig(level=logging.INFO)
    c = Container(dict(config_path=config_path))
    register(c)
    return WorkerApp(
        host=c('conf')['broker']['host'],
        port=c('conf')['broker']['port'],
        factory=c('factory'),
        loop=c('loop'),
        controller=c('worker_controller'),
        ssl_context=c('ssl_context')
    )


class WorkerApp:
    def __init__(self, host, port, factory, loop, controller, ssl_context):
        self.host = host
        self.port = port
        self.factory = factory
        self.loop = loop
        self.controller = controller
        self.ssl_context = ssl_context
        self.register_signal_handlers()

    def run(self):
        coro = self.loop.create_connection(
            protocol_factory=self.factory,
            host=self.host,
            port=self.port,
            ssl=self.ssl_context
        )
        self.loop.run_until_complete(coro)
        self.loop.run_forever()
        self.loop.close()

    def register_signal_handlers(self):
        for signame in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(self.clean_up, signame)
            )

    def clean_up(self, signame):
        self.controller.clean_up()
        self.loop.stop()


if __name__ == "__main__":
    app = make_app(config_path='conf/develop.ini')
    app.run()
