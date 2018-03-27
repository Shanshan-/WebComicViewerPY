from tkinter import *

class Dialog:
    def __init__(self, master, labelTxt, dFrame=None, title="Dialog", btnTxt="OK"):
        self.dialog = Toplevel(master)
        self.dialog.grab_set()
        self.dialog.wm_title(title)
        self.frame = Frame(self.dialog)
        Label(self.frame, text=labelTxt).pack()
        if dFrame:
            Button(self.frame, text=btnTxt, command=dFrame.destroy).pack()
        else:
            Button(self.frame, text=btnTxt, command=self.dialog.destroy).pack()
        self.frame.pack(padx=10, pady=10)