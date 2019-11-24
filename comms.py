from paramiko import SSHClient
from threading import Thread
from socket import timeout
from tkinter import Text, messagebox
import json


class ConsoleComm(Thread):
    def __init__(self, output: Text, client=SSHClient(), timeout=5, config_file='./settings.json'):
        super().__init__()
        self._running = True

        self.output = output

        with open(config_file, 'r') as fp:
            config = json.load(fp)

        self.client = client
        self.client.load_system_host_keys()

        try:
            ip = config['server']['ip']
        except KeyError as e:
            messagebox.showerror(
                'Error', 'Server IP is not configured, please go into Console Settings and add one')
            raise e

        try:
            port = config['server']['port']
        except KeyError:
            port = 22

        try:
            self.client.connect(
                ip, username='vagrant', password='vagrant', port=port)
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
                self.output.see('end')
                self.client.close()
                break
            self.output.insert('end', data)
            self.output.see('end')

    def send_key(self, event):
        try:
            self.channel.send(event.char)
        except OSError:
            pass
        return 'break'
