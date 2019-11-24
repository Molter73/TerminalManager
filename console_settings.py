from tkinter import Toplevel, Label, Button, Entry, StringVar
import json


class ConsoleSettings(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master

        with open('./settings.json', 'r') as config_file:
            self.config = json.load(config_file)

        Label(master=self, text='Server IP:').grid(column=0, row=0)

        self.server_ip = Entry(master=self)
        self.server_ip.grid(column=1, row=0)

        try:
            ip = self.config['server']['ip']
        except KeyError:
            ip = '127.0.0.1'

        try:
            port = self.config['server']['port']
        except KeyError:  # no port configured, use default
            port = 22

        self.server_ip.insert('0', '{}:{}'.format(ip, port))

        Button(master=self, text='Accept',
               command=self.accept_config).grid(column=10, row=10)
        Button(master=self, text='Cancel',
               command=self.destroy).grid(column=9, row=10)

    def dump_config(self):
        server_ip = self.server_ip.get()
        if ':' in server_ip:
            server = server_ip.split(':')
        else:
            server = [server_ip, 22]

        self.config['server'] = {'ip': server[0], 'port': server[1]}

        with open('./settings.json', 'w') as config_file:
            json.dump(self.config, config_file)

    def accept_config(self):
        self.dump_config()
        self.destroy()
