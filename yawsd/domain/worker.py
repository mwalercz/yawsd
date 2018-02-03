import paramiko


class WorkerFactory:
    def __init__(self, hostname):
        self.hostname = hostname

    def get(self, work):
        return Worker(
            hostname=self.hostname,
            work=work,
        )


class Worker:
    INVOKE_BASH = r"bash -c"
    ECHO_PID = r"echo $$"
    GOTO_DIR = r"cd {}"
    EXEC_CMD = r"exec {}"

    def __init__(self, hostname, work):
        self.hostname = hostname
        self.work = work
        self.pid = None

    def do_work(self):
        try:
            command = self._get_command()
            client = self._get_client()
            chan = self._prepare_channel(client)
            return self._exec_command(chan, command)
        finally:
            if client:
                client.close()

    def kill_work(self):
        if self.pid:
            try:
                command = self._get_kill_command()
                client = self._get_client()
                chan = self._prepare_channel(client)
                return self._exec_kill_command(chan, command)
            finally:
                if client:
                    client.close()
        else:
            return None

    def _prepare_channel(self, ssh):
        tran = ssh.get_transport()
        chan = tran.open_session()
        chan.get_pty()
        return chan

    def _get_command(self):
        cmd_to_exec = self.EXEC_CMD.format(self.work.command)
        goto_dir = self.GOTO_DIR.format(self.work.cwd)
        return r"{invoke_bash} '{echo_pid}; {goto_dir}; {exec_cmd};'".format(
            invoke_bash=self.INVOKE_BASH,
            echo_pid=self.ECHO_PID,
            goto_dir=goto_dir,
            exec_cmd=cmd_to_exec,
        ).strip()

    def _get_kill_command(self):
        return r"kill -9 {pid}".format(pid=self.pid).strip()

    def _get_client(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.hostname,
            username=self.work.username,
            password=self.work.password
        )
        return client

    def _exec_command(self, chan, command):
        f = chan.makefile()
        chan.exec_command(command)
        self.pid = f.readline()
        return {
            'output': f.read().decode("utf-8"),
            'exit_code': chan.recv_exit_status(),
        }

    def _exec_kill_command(self, chan, command):
        chan.exec_command(command)
        status = chan.recv_exit_status()
        return status
