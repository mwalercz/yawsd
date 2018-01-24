import paramiko
from paramiko import SSHClient, SSHException


class SSHService:
    def __init__(self, hostname):
        self.hostname = hostname

    def try_to_login(self, username, password):
        with SSHClient() as client:
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            try:
                client.connect(
                    hostname=self.hostname,
                    username=username,
                    password=password,
                )
                return True
            except SSHException:
                return False
