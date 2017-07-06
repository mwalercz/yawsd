class MasterClient:
    master = NotImplemented

    def __init__(self, serializer):
        self.serializer = serializer

    def send(self, action_name, body=None):
        message = {
            'path': action_name,
            'body': body,
        }
        serialized_message = self.serializer.serialize(message)
        self.master.sendMessage(serialized_message)
