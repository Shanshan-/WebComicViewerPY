# using guide from http://effbot.org/tkinterbook/tkinter-classes.htm
from tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack(padx=100, pady=20)
        self.counter = 0

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT) # item will be placed as far left as possible; default is TOP

        Button(frame, text="Hello", command=self.say_hi).pack(side=LEFT)

    def say_hi(self):
        print("Window says hi!")

if __name__ == "__main__":
    # create the root window which will hold all objects
    root = Tk()
    root.wm_title("Base window")

    # create objects to go into the root window
    w = Label(root, text="Hello world!\nThis is a test!")
    w.pack() # fit this widget to its contents and become visible
    app = App(root)

    # start program and open window
    root.mainloop()
    try:
        root.destroy()
    except:
        print("")
