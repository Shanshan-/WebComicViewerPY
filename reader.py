# using guide from http://effbot.org/tkinterbook/tkinter-classes.htm
from tkinter import *

def genMenu(rootFrame):
    #ETC: look up tkinter Menu, MenuButton
    menuBar = Menu(rootFrame)
    rootFrame.config(menu=menuBar)

    # File Options
    fileOpts = Menu(menuBar, tearoff=0)
    recentFiles = Menu(fileOpts, tearoff=0)
    fileOpts.add_command(label="Scrape New", command=NONE)
    fileOpts.add_separator()
    fileOpts.add_cascade(label="Open Recent", menu=recentFiles)
    recentFiles.add_command(label="<no recent files>", state="disabled")
    fileOpts.add_command(label="Open New", command=NONE)

    # Viewer Options
    viewOpts = Menu(menuBar, tearoff=0)
    viewOpts.add_command(label="<to be made>", command=NONE, state="disabled")
    viewOpts.add_command(label="Quit", command=rootFrame.destroy)

    # Put it all together and return
    menuBar.add_cascade(label="File Options", menu=fileOpts)
    menuBar.add_cascade(label="Viewer Options", menu=viewOpts)
    return menuBar

class Viewer:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack() # to make the viewer visible

        #create image section
        #TODO: look up tkinter Scrollbar

        Label(self.frame, text="Test label").pack()
        self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.pack(side=LEFT) # item will be placed as far left as possible; default is TOP

        Button(self.frame, text="Hello", command=self.say_hi).pack(side=LEFT)

    def say_hi(self):
        print("Window says hi!")
        t = Toplevel(self.frame)

if __name__ == "__main__":
    # create the root window which will hold all objects
    root = Tk()
    sheight = root.winfo_screenheight()
    swidth = root.winfo_screenwidth()
    root.geometry('%sx%s' % (int(swidth/2), int(sheight/2)))
    root.wm_title("WCV Reader")
    genMenu(root)
    app = Viewer(root)

    # start program and open window
    root.mainloop()
    try:
        root.destroy()
    except:
        print("")
