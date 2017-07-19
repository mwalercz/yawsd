import argparse
import logging
import os

from autobahn.websocket.util import parse_url
from knot import Container

from definitions import ROOT_DIR
from dq_worker.dependencies import register


def check_if_credentials_are_ok(c):
    if not c('ssh').try_to_login(
        username=c('username'),
        password=c('password'),
    ):
        raise Exception('Wrong credentials!')


def make_app(
        config_path='conf/develop.ini',
        username='test',
        password='test'
):
    logging.basicConfig(level=logging.INFO)
    c = Container(dict(
        config_path=config_path,
        username=username,
        password=password
    ))
    register(c)

    check_if_credentials_are_ok(c)
    return WorkerApp(
        url=c('conf').get('broker', 'url'),
        reactor=c('reactor'),
        factory=c('factory'),
        controller=c('worker_controller'),
        ssl_context=c('ssl_context')
    )


class WorkerApp:
    def __init__(self, url, factory, reactor, controller, ssl_context):
        self.url = url
        self.factory = factory
        self.reactor = reactor
        self.ssl_context = ssl_context
        self.controller = controller
        self.register_signal_handlers()

    def run(self):
        is_secure, host, port, resource, path, params = (
            parse_url(self.url)
        )
        self.reactor.connectSSL(
            host=host,
            port=port,
            factory=self.factory,
            contextFactory=self.ssl_context

        )
        self.reactor.run()

    def register_signal_handlers(self):
        self.reactor.addSystemEventTrigger('before', 'shutdown', self.clean_up)

    def clean_up(self):
        self.controller.clean_up()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='config_path', default='develop.ini')
    parser.add_argument('-u', dest='username', default='test')
    parser.add_argument('-p', dest='password', default='test')
    args = parser.parse_args()
    app = make_app(
        config_path=os.path.join(ROOT_DIR, 'dq_worker/conf', args.config_path),
        username=args.username,
        password=args.password,
    )
    app.run()


if __name__ == "__main__":
    main()
