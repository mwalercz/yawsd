from twisted.internet import defer

from dq_worker.infrastructure.serializers import serialize


class MasterClient(object):
    master = NotImplemented

    def send(self, action_name, body=None):
        message = {
            'path': action_name,
            'body': body,
        }
        serialized_message = serialize(message)
        self.master.sendMessage(serialized_message)


class LockedMasterClient(MasterClient):
    lock = NotImplemented

    @defer.inlineCallbacks
    def send(self, action_name, body=None):
        yield self.lock.acquire()
        super(LockedMasterClient, self).send(action_name, body)
        self.lock.release()
