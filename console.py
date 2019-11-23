from tkinter import Text
from paramiko import Transport, SSHClient


class Console(Text):
    def __init__(self, master=None, width=80, height=24):
        super().__init__(master=master, width=width, height=height)
        self.pack()

        self.client = SSHClient()
        self.client.load_system_host_keys()
        try:
            self.client.connect('192.168.50.10', username='vagrant', password='vagrant', port=22)
        except Exception as e:
            print(e)
            self.client.close()
        
        self.channel = self.client.invoke_shell()
        # self.stdout = self.channel.makefile(mode='r')

        self.insert('1.0', self.channel.recv(1024))

    def __del__(self):
        self.client.close()

