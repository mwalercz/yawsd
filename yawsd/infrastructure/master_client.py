from twisted.internet import defer

from yawsd.infrastructure.serializers import serialize


class MasterClient(object):
    master = NotImplemented

    def send(self, action_name, body=None):
        message = {
            'path': action_name,
            'body': body,
        }
        serialized_message = serialize(message)
        self.master.sendMessage(serialized_message)
