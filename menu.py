from tkinter import Menu


class ManagerMenu(Menu):
    def __init__(self, master=None):
        super().__init__(master)

        self.file = Menu(self)
        self.add_cascade(menu=self.file, label='File')

        master['menu'] = self
