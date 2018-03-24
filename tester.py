from tkinter import *
from main import main_func

def func1():
    print("func1 was called")

def func2():
    print("func2 was called")

class MainWindow(Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        #self.new_button = Button(self, text="Create new window", command=self.create_window)
        #self.new_button.pack(side="top", pady=20)
        self.f1_button = Button(self, text="F1", command=func1).pack(side=TOP)
        self.hi_button = Button(self, text="HI", command=self.say_hi).pack(side=RIGHT)
        self.f2_button = Button(self, text="F2", command=main_func).pack(side=BOTTOM)
        self.new_button = Button(self, text="NEW", command=self.create_window).pack(side=LEFT)


    def create_window(self):
        self.counter += 1
        t = Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def say_hi(self):
        print("Window says hi!")

if __name__ == "__main__":
    root = Tk()
    root.wm_title("Base window")
    w = Label(root, text="Hello world!\nThis is a test!")
    w.pack(padx=100, pady=20) # fit this widget to its contents and become visible

    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()