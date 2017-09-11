import os

import psutil


class SystemStatGatherer:
    def get_system_stat(self):
        load_1, load_5, load_15 = os.getloadavg()
        return {
            'cpu': {
                'count': psutil.cpu_count(),
                'load_1': load_1,
                'load_5': load_5,
                'load_15': load_15,
            },
            'memory': {
                'total': psutil.virtual_memory()[0],
                'available': psutil.virtual_memory()[1]
            }
        }