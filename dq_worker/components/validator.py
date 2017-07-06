def validate(schema):
    def validate_decorator(func):
        def func_wrapper(self, message):
            schema_instance = schema(message['body'])
            schema_instance.validate()
            func(self, schema_instance)
        return func_wrapper
    return validate_decorator
