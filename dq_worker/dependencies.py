from ConfigParser import ConfigParser

from twisted.internet import ssl
from twisted.internet.defer import DeferredLock

from dq_worker.infrastructure.controller import WorkerController
from dq_worker.infrastructure.factory import WorkerFactory
from dq_worker.infrastructure.master_client import MasterClient, LockedMasterClient
from dq_worker.infrastructure.protocol import WorkerProtocol
from dq_worker.infrastructure.router import Router


def lock(c):
    return DeferredLock()


def master_client(c):
    return MasterClient()


def locked_master_client(c):
    client = LockedMasterClient()
    client.lock = c('lock')
    return client


def router(c):
    return Router(c('worker_controller'))


def protocol(c):
    protocol = WorkerProtocol
    protocol.master_client = c('master_client')
    protocol.locked_master_client = c('locked_master_client')
    protocol.router = c('router')
    protocol.controller = c('worker_controller')
    protocol.master_client_lock = c('lock')
    return protocol


def headers(c):
    return {
        'username': c('username'),
        'password': c('password'),
    }


def ssl_context(c):
    return ssl.ClientContextFactory()


def factory(c):
    factory = WorkerFactory(
        url=c('conf').get('broker', 'url'),
        headers=c('headers'),
    )
    factory.protocol = c('protocol')
    return factory


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def reactor(c):
    from twisted.internet import reactor

    return reactor


def worker_controller(c):
    return WorkerController(
        master_client=c('locked_master_client'),
    )


def register(c):
    c.add_service(conf)
    c.add_service(reactor)
    c.add_service(lock)
    c.add_service(master_client)
    c.add_service(locked_master_client)
    c.add_service(worker_controller)
    c.add_service(router)
    c.add_service(headers)
    c.add_service(protocol)
    c.add_service(factory)
    c.add_service(ssl_context)
