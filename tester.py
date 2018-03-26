from tkinter import *
from tkinter import Tk, font
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
        Button(self, text="Font", command=self.font_window).pack(side=BOTTOM)
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

    def font_window(self):
        """
            root = Tk()
            fonts=list(font.families())
            fonts.sort()
            x = 0
            y = 0
            num = 36

            for item in fonts:
                w = Label(root, text=item, font=(item, 9))
                w.grid(row=x%num, column = int(x/num))
                x += 1
                y += 1

            root.mainloop()
        """
        t = Toplevel(self)
        fonts=list(font.families())
        fonts.sort()
        x = 0
        y = 0
        num = 36
        for item in fonts:
            txt = Label(t, text=item, font=(item, 9))
            txt.grid(row=x%num, column=int(x/num))
            x += 1
            y += 1


    def say_hi(self):
        print("Window says hi!")

class MainWindow2:
    counter = 0
    def __init__(self, master):
        self.mainFrame = Frame(master)
        Button(self.mainFrame, text="HI", command=self.say_hi).pack(side=RIGHT)
        Button(self.mainFrame, text="NEW", command=self.create_window).pack(side=LEFT)
        Button(self.mainFrame, text="MAIN", command=lambda:main_func()).pack(side=BOTTOM)
        Button(self.mainFrame, text="LF", command=lambda:print(loadFiles("./img/extras"))).pack(side=TOP)
        self.mainFrame.pack(padx=20, ipady=5, pady=10)

    def create_window(self):
        self.counter += 1
        t = Toplevel(self.mainFrame)
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
    test1 = True

    if test1:
        main = MainWindow(root)
        main.pack(side="top", fill="both", expand=True)
        root.mainloop()
    else:
        main = MainWindow2(root)
        root.mainloop()

"""
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
root = Tk()
root.wm_title("New Window")
app = App(root)
"""