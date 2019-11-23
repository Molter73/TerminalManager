from paramiko import SSHClient
from threading import Thread
from socket import timeout
from tkinter import Text


class ConsoleComm(Thread):
    def __init__(self, output: Text, client=SSHClient(), timeout=5):
        super().__init__()
        self._running = True

        self.output = output

        self.client = client
        self.client.load_system_host_keys()
        try:
            self.client.connect(
                '192.168.50.10', username='vagrant', password='vagrant', port=22)
        except Exception as e:
            print(e)
            self.client.close()
            raise e

        self.channel = self.client.invoke_shell()
        self.channel.settimeout(1)

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            try:
                data = self.channel.recv(256)
            except timeout:
                continue

            if not data:
                self.output.insert('end', '\r\n *** Connection closed ***\r\n')
                self.client.close()
                break
            self.output.insert('end', data)
