from paramiko import SSHClient
from threading import Thread
from socket import timeout
from tkinter import Text, messagebox
import json
import re


class ConsoleComm(Thread):
    COLORS = ['black', 'red', 'green', 'yellow',
              'blue', 'violet', 'beige', 'white']

    color_pattern = re.compile(r'\x1b\[([0-9;]*)m')

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
        self.channel.settimeout(0.05)

    def stop(self):
        self._running = False

    def run(self):
        buffer = ''
        while self._running:
            try:
                data = self.channel.recv(256)
            except timeout:
                if buffer != '':
                    tags = ()
                    begin = 0
                    for it in self.color_pattern.finditer(buffer):
                        self.output.insert(
                            'end', buffer[begin:it.start()], tags)
                        tags = self.get_tags(it.group(1))
                        begin = it.end()

                    self.output.insert('end', buffer[begin:], tags)
                    self.output.see('end')

                    buffer = ''
                continue

            if not data:
                self.output.insert('end', '\r\n *** Connection closed ***\r\n')
                self.output.see('end')
                self.client.close()
                self.output.destroy()
                break

            buffer = ''.join([buffer, data.decode('ASCII')])

    def send_key(self, event):
        try:
            self.channel.send(event.char)
        except OSError:
            pass
        return 'break'

    def get_tags(self, command_list):
        format_list = list()
        for command in command_list.split(';'):
            c = int(command)
            if c == 0:
                return ()

            tag = ''
            group = int(c/10)
            color = c % 10
            if group == 3 or group == 9:
                tag = ''.join([tag, 'fg-', self.COLORS[color]])

            if group == 4 or group == 10:
                tag = ''.join([tag, 'bg-', self.COLORS[color]])

            if tag != '':
                format_list.append(tag)

        return tuple(format_list)
