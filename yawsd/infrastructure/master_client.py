import logging


from yawsd.infrastructure.serializers import serialize
from yawsd.infrastructure.utils import clear_passwords_from_message

log = logging.getLogger(__name__)


class MasterClient(object):
    master = NotImplemented

    def send(self, action_name, body=None):
        message = {
            'path': action_name,
            'body': body,
        }
        log.info('Sending message to master: %s', repr(clear_passwords_from_message(message)))
        serialized_message = serialize(message)
        self.master.sendMessage(serialized_message)
