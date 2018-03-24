from tkinter import *
from main import main_func
from loader import loadFiles

def func1():
    print("func1 was called")

class MainWindow(Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        Button(self, text="HI", command=self.say_hi).pack(side=RIGHT)
        Button(self, text="NEW", command=self.create_window).pack(side=LEFT)
        Button(self, text="MAIN", command=lambda:main_func()).pack(side=BOTTOM)
        Button(self, text="LF", command=lambda:print(loadFiles("./img/extras"))).pack(side=TOP)
        self.pack(padx=20, ipady=5, pady=10)

    def create_window(self):
        self.counter += 1
        t = Toplevel(self)
        t.grab_set() #deactivate other window
        t.wm_title("Window #%s" % self.counter)
        f = Frame(t) #for padding purposes
        l = Label(f, text="This is window #%s" % self.counter).pack(side=TOP)
        Button(f, text="QUIT", fg="red", command=t.destroy).pack(side=BOTTOM)
            #create a button to close top level
        f.pack(side="top", fill="both", expand=True, padx=50, pady=50)

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