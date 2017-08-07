import psutil


class SystemStatGatherer:
    def get_system_stat(self):
        return {
            'cpu': {
                'count': psutil.cpu_count(),
                'percent': psutil.cpu_percent(),
            },
            'memory': {
                'total': psutil.virtual_memory()[0],
                'available': psutil.virtual_memory()[1]
            }
        }