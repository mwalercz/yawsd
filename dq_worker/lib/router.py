class Router:
    def __init__(self):
        self.controllers = {}

    def register(self, path, controller):
        self.controllers.update({
            path: controller
        })

    def find_responder(self, path):
        controller_path, method_path = self._get_paths(path)
        controller = self._get_controller(controller_path)
        return controller, self._find_responder(controller, method_path)

    def _get_paths(self, path):
        splitted_path = path.split('/')
        try:
            controller_path = splitted_path[0]
            method_path = splitted_path[1]
        except KeyError:
            raise Exception('Wrong path {0}'.format(path))
        else:
            if method_path.startswith('_'):
                raise Exception(
                    'Private method {0} cannot be accessed'.format(method_path))
            else:
                return controller_path, method_path

    def _get_controller(self, controller_path):
        try:
            return self.controllers[controller_path]
        except KeyError:
            raise Exception(
                'No controller with path {0}'.format(controller_path))

    def _find_responder(self, controller, method_path):
        try:
            method = getattr(controller, method_path)
        except AttributeError:
            raise Exception(
                'Method: {} in controller: {} not implemented'.format(
                    method_path, str(controller)))
        else:
            if callable(method):
                return method
