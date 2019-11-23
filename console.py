from tkinter import Text


class Console(Text):
    def __init__(self, master=None, width=80, height=24):
        super().__init__(master=master, width=width, height=height)
        self.pack()
