from tkinter import Menu
from console_settings import ConsoleSettings
from console import Console


class ManagerMenu(Menu):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        self.file = Menu(self)
        self.add_cascade(menu=self.file, label='File')
        self.file.add_command(label='New Console', command=self.new_console)
        self.file.add_command(label='Console Settings', command=self.new_settings)

        self.settings = None
        self.console = None

        master['menu'] = self

    def new_console(self):
        if self.console != None:
            self.console.destroy()
        self.console = Console(master=self.master)
        self.console.focus_force()

    def new_settings(self):
        if self.settings == None:
            self.settings = ConsoleSettings(master=self.master)

        if not self.settings.winfo_exists():
            self.settings = ConsoleSettings(master=self.master)

        self.settings.focus_force()
