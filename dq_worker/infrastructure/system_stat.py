import os

import psutil


def get_system_info():
    return {
        'host_cpu_count': psutil.cpu_count(),
        'host_total_memory': psutil.virtual_memory()[0],
        'system_stat': get_system_stat()
    }


def get_system_stat():
    load_1, load_5, load_15 = os.getloadavg()
    return {
        'load_15': load_15,
        'available_memory': psutil.virtual_memory()[1],
    }
