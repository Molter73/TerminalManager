from tkinter import Text
from comms import ConsoleComm


class Console(Text):
    def __init__(self, master=None, width=80, height=24):
        super().__init__(master=master, width=width, height=height)

        try:
            self.comms = ConsoleComm(output=self)
        except Exception:
            return

        self.comms.start()

        self.bind('<Key>', lambda key: self.comms.send_key(key))

        # Define all supported formatting
        self.tag_configure('fg-black', foreground='black')
        self.tag_configure('fg-red', foreground='red')
        self.tag_configure('fg-green', foreground='green')
        self.tag_configure('fg-yellow', foreground='yellow')
        self.tag_configure('fg-blue', foreground='blue')
        self.tag_configure('fg-violet', foreground='violet')
        self.tag_configure('fg-beige', foreground='beige')
        self.tag_configure('fg-white', foreground='blue')

        self.tag_configure('bg-black', background='black')
        self.tag_configure('bg-red', background='red')
        self.tag_configure('bg-green', background='green')
        self.tag_configure('bg-yellow', background='yellow')
        self.tag_configure('bg-blue', background='blue')
        self.tag_configure('bg-violet', background='violet')
        self.tag_configure('bg-beige', background='beige')
        self.tag_configure('bg-white', background='blue')

        self.configure(background='black', foreground='white')

        self.pack()

    def destroy(self):
        print(__name__ + ': destroy')
        self.comms.stop()
        super().destroy()
