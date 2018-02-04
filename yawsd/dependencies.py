import base64

import os
from ConfigParser import SafeConfigParser

from twisted.internet import ssl

from yawsd.domain.worker import WorkerFactory
from yawsd.infrastructure.controller import WorkerController
from yawsd.infrastructure.factory import DqWorkerFactory
from yawsd.infrastructure.master_client import MasterClient
from yawsd.infrastructure.protocol import WorkerProtocol
from yawsd.infrastructure.router import Router
from yawsd.infrastructure.ssh import SSHService


def master_client(c):
    return MasterClient()


def router(c):
    return Router(c('worker_controller'))


def protocol(c):
    protocol = WorkerProtocol
    protocol.master_client = c('master_client')
    protocol.router = c('router')
    protocol.controller = c('worker_controller')
    return protocol


def headers(c):
    return {
        'Authorization': ' '.join([
            'Basic',
            base64.b64encode(
                ':'.join([c('username'), c('password')])
            ).decode()
        ])
    }


def ssl_context(c):
    return ssl.ClientContextFactory()


def factory(c):
    factory = DqWorkerFactory(
        url=c('conf').get('broker', 'url'),
        headers=c('headers'),
    )
    factory.protocol = c('protocol')
    return factory


def conf(c):
    conf = SafeConfigParser(os.environ)
    conf.read(c('config_path'))
    return conf


def reactor(c):
    from twisted.internet import reactor

    return reactor


def worker_factory(c):
    return WorkerFactory(
        hostname=c('conf').get('ssh', 'host')
    )


def worker_controller(c):
    return WorkerController(
        master_client=c('master_client'),
        worker_factory=c('worker_factory')
    )


def ssh(c):
    return SSHService(
        hostname=c('conf').get('ssh', 'host')

    )


def register(c):
    c.add_service(conf)
    c.add_service(reactor)
    c.add_service(master_client)
    c.add_service(worker_factory)
    c.add_service(worker_controller)
    c.add_service(router)
    c.add_service(headers)
    c.add_service(protocol)
    c.add_service(factory)
    c.add_service(ssl_context)
    c.add_service(ssh)
