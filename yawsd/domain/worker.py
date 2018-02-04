import logging

import paramiko

log = logging.getLogger(__name__)


class WorkerFactory:
    def __init__(self, hostname):
        self.hostname = hostname

    def get(self, work):
        return Worker(
            hostname=self.hostname,
            work=work,
        )


class Worker:
    def __init__(self, hostname, work):
        self.hostname = hostname
        self.work = work
        self.pid = None

    def do_work(self):
        try:
            client = self._get_client()
            tran = client.get_transport()
            chan = tran.open_session()
            chan.get_pty()
            file = chan.makefile()
            command = r"echo $$ && cd {} && exec {}".format(
                self.work.cwd,
                self.work.command,
            ).strip()
            log.info(command)
            chan.exec_command(command)
            self.pid = int(file.readline())
            return {
                'output': file.read().decode('utf-8'),
                'exit_code': chan.recv_exit_status(),
            }
        finally:
            if client:
                client.close()

    def kill_work(self):
        if self.pid:
            try:
                client = self._get_client()
                tran = client.get_transport()
                chan = tran.open_session()
                file = chan.makefile()
                chan.exec_command(r'kill -9 {pid}'.format(pid=str(self.pid)).strip())
                return {
                    'output': file.read().decode('utf-8'),
                    'exit_code': chan.recv_exit_status(),
                }
            finally:
                if client:
                    client.close()
        else:
            return None

    def _get_client(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.hostname,
            username=self.work.username,
            password=self.work.password
        )
        return client
