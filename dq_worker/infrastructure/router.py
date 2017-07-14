from dq_worker.exceptions import RouteNotFound


class Router:
    def __init__(self, controller):
        self.controller = controller

    def find_responder(self, path):
        try:
            method = getattr(self.controller, path)
            if callable(method):
                return method
            else:
                raise Exception()
        except AttributeError:
            raise RouteNotFound(
                'Method: {} in controller: {} not implemented'.format(
                    path, str(self.controller)))
