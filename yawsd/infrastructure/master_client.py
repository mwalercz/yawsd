import logging

from twisted.internet import defer

from yawsd.infrastructure.serializers import serialize

log = logging.getLogger(__name__)


class MasterClient(object):
    master = NotImplemented

    def send(self, action_name, body=None):
        message = {
            'path': action_name,
            'body': body,
        }
        serialized_message = serialize(message)
        log.info('Sending message to master: %s', serialized_message)
        self.master.sendMessage(serialized_message)
