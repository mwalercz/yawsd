from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types.compound import DictType


class Work(Model):
    work_id = IntType(required=True)
    command = StringType(required=True)
    cwd = StringType(required=True)
    username = StringType(required=True)
    password = StringType(required=True)
    env = DictType(StringType, default={})
