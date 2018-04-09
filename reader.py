# using guide from http://effbot.org/tkinterbook/tkinter-classes.htm
from tkinter import *
from tkinter import ttk
from scraper import *
from widgets import *

class Viewer:
    def __init__(self, master):
        self.menu, self.recent_menu = self.gen_menu(master)
        self.frame = Frame(master)
        self.frame.pack() # to make the viewer visible

        #create image section
        #TODO: look up tkinter Scrollbar
        Label(self.frame, text="Images to go here later", fg="gray").pack()
        Button(self.frame, text="QUIT", command=master.destroy).pack()
        Button(self.frame, text="Scrape", command=self.open_scrape).pack()

    # Generate the menu to go on top, and link as needed
    def gen_menu(self, rootFrame):
        #ETC: look up tkinter Menu, MenuButton
        menuBar = Menu(rootFrame)
        rootFrame.config(menu=menuBar)

        # File Options
        fileOpts = Menu(menuBar, tearoff=0)
        recentFiles = Menu(fileOpts, tearoff=0)
        fileOpts.add_command(label="Scrape New", command=self.open_scrape)
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
        return menuBar, recentFiles

    def open_scrape(self):
        Scraper(self.frame)
        #TODO: implement taking results from pop-up and implementing them

if __name__ == "__main__":
    # create the root window which will hold all objects
    root = Tk()
    sheight = root.winfo_screenheight()
    swidth = root.winfo_screenwidth()
    root.geometry('%sx%s' % (int(swidth/2), int(sheight/2)))
    root.wm_title("WCV Reader")
    #genMenu(root)
    app = Viewer(root)

    # start program and open window
    root.mainloop()
    try:
        root.destroy()
    except:
        print("")
