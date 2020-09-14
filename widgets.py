from tkinter import *
from PIL import ImageTk, Image

class Dialog:
    def __init__(self, master, labelTxt, dFrame=None, title="Dialog", btnTxt="OK", grab=True):
        self.dialog = Toplevel(master)
        self.dialog.grab_set() if grab else None
        self.dialog.wm_title(title)
        self.frame = Frame(self.dialog)
        self.dFrame = dFrame
        Label(self.frame, text=labelTxt).pack()
        if dFrame:
            Button(self.frame, text=btnTxt, command=dFrame.destroy).pack()
            self.dialog.bind("<Return>", self.destroySelf)
        else:
            Button(self.frame, text=btnTxt, command=self.dialog.destroy).pack()
            self.dialog.bind("<Return>", self.destroySelf)
        self.frame.pack(padx=10, pady=10)

    def destroySelf(self, event=None):
        if self.dFrame:
            self.dFrame.destroy()
        else:
            self.dialog.destroy()

class ImageDialog:
    def __init__(self, master, imageLoc, dFrame=None, title="Dialog"):
        #Initial variables
        WIDTH = 300
        HEIGHT = 300
        self.dialog = Toplevel(master)
        self.dialog.wm_title(title)
        self.dFrame = dFrame
        self.frame = Frame(self.dialog)

        #Setup and display the image (must save image as class variable, else garbage collection)
        self.img = ImageTk.PhotoImage(Image.open(imageLoc).resize((WIDTH, HEIGHT)))
        canvas = Canvas(self.frame, width=WIDTH, height=HEIGHT)
        canvas.create_image(0, 0, anchor=NW, image=self.img)
        canvas.pack()

        #Setup and display the feedback for buttons
        Label(self.frame, text="Is this image correct?").pack()
        self.correct = BooleanVar(value=FALSE)
        buttonFrame = Frame(self.frame)
        if dFrame:
            Button(buttonFrame, text="Yes", command=self.validImg).pack(side=LEFT, padx=10)
            Button(buttonFrame, text="No", command=self.destroySelf).pack(side=LEFT, padx=10)
        else:
            Button(buttonFrame, text="Yes", command=self.validImg).pack(side=LEFT, padx=10)
            Button(buttonFrame, text="No", command=self.destroySelf).pack(side=LEFT, padx=10)
        buttonFrame.pack(side=TOP, pady=5)
        self.frame.pack(padx=10, pady=10)

    def validImg(self, event=None): #used to handle branching from buttons
        self.correct.set(value=TRUE)
        self.destroySelf(event)

    def destroySelf(self, event=None):
        if self.dFrame:
            self.dFrame.destroy()
        else:
            self.dialog.destroy()

    def show(self): #used to return contents of self.correct to caller
        self.dialog.grab_set()
        self.dialog.wait_window()
        return self.correct.get()

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

    def insert(self, *args):
        super().insert(*args)
        if str(args[1]) != self.hintTxt:
            self["fg"] = self.origFgColor

    def focusIn(self, *args):
        if self.get() != self.hintTxt:
            self["fg"] = self.origFgColor
        elif self['fg'] == self.hintColor:
            self.delete("0", "end")
            self["fg"] = self.origFgColor

    def focusOut(self, *args):
        if not self.get():
            self.insert(0, self.hintTxt)
            self["fg"] = self.hintColor