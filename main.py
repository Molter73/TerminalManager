from tkinter import Tk, Button, Frame, Toplevel
from console import Console
from menu import ManagerMenu


class Application (Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = Button(self)
        self.hi_there['text'] = 'Hello world!\n(click me)'
        self.hi_there['command'] = self.say_hi
        self.hi_there.pack(side='top')

        self.quit = Button(self, text='QUIT', fg='red',
                           command=self.master.destroy)
        self.quit.pack(side='bottom')

    def say_hi(self):
        print('Hi there!')


def main():
    root = Tk()
    root.option_add('*tearOff', False)  # No tearing off menus please

    app = ManagerMenu(root)

    app.mainloop()


if __name__ == '__main__':
    main()
