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

class HintedEntry(Entry):
    def __init__(self, master, hintTxt="", hintColor="grey", **kwargs):
        super().__init__(master, **kwargs)
        self.hintTxt = hintTxt
        self.hintColor = hintColor
        self.origFgColor = self["fg"]

        self.bind("<FocusIn>", self.focusIn)
        self.bind("<FocusOut>", self.focusOut)

        self.insert(0, hintTxt)
        self["fg"] = hintColor

    def focusIn(self, *args):
        if self['fg'] == self.hintColor:
            self.delete("0", "end")
            self["fg"] = self.origFgColor

    def focusOut(self, *args):
        if not self.get():
            self.insert(0, self.hintTxt)
            self["fg"] = self.hintColor