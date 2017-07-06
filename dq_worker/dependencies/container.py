import asyncio
import ssl
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

from dq_worker.lib.serializers import JsonDeserializer, JsonSerializer
from dq_worker.dependencies import components
from dq_worker.dependencies import controller


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def deserializer(c):
    return JsonDeserializer()


def serializer(c):
    return JsonSerializer()


def thread_pool_executor(c):
    return ThreadPoolExecutor(max_workers=2)


def loop(c):
    loop = asyncio.get_event_loop()
    loop.set_default_executor(c('thread_pool_executor'))
    loop.set_debug(True)
    return loop


def ssl_context(c):
    return ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23)





def register(c):
    c.add_service(conf)
    c.add_service(deserializer)
    c.add_service(serializer)
    c.add_service(thread_pool_executor)
    c.add_service(loop)
    c.add_service(ssl_context)

    components.register(c)
    controller.register(c)
