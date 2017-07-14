import json

ENCODING = 'utf8'


def serialize(message):
    return json.dumps(message).encode(ENCODING)


def deserialize(message):
    return json.loads(message.decode(ENCODING))
