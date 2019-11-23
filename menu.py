from tkinter import Menu
from console import Console


class ManagerMenu(Menu):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        self.file = Menu(self)
        self.add_cascade(menu=self.file, label='File')
        self.file.add_command(label='New Console', command=self.new_console)

        master['menu'] = self

    def new_console(self):
        Console(master=self.master)
