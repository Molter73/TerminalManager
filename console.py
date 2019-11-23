from tkinter import Text
from comms import ConsoleComm


class Console(Text):
    def __init__(self, master=None, width=80, height=24):
        super().__init__(master=master, width=width, height=height)

        self.comms = ConsoleComm(output=self)
        self.comms.start()

        self.pack()

    def destroy(self):
        print(__name__ + ': destroy')
        self.comms.stop()
