class SimpleRouter:
    def __init__(self, controller):
        self.controller = controller

    def get_responder(self, path):
        method_path = self._get_method_path(path)
        return self._find_responder(method_path)

    def _get_method_path(self, path):
        splitted_path = path.split('/')
        try:
            method_path = splitted_path[1]
        except KeyError:
            raise Exception('Wrong path {0}'.format(path))
        else:
            if method_path.startswith('_'):
                raise Exception(
                    'Private method {0} cannot be accessed'.format(method_path))
            else:
                return method_path

    def _find_responder(self, method_path):
        try:
            method = getattr(self.controller, method_path)
        except AttributeError:
            raise Exception(
                'Method: {} in controller: {} not implemented'.format(
                    method_path, str(
                        self.controller)))
        else:
            if callable(method):
                return method
