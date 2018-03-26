# using guide from http://effbot.org/tkinterbook/tkinter-classes.htm
from tkinter import *


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

class Scraper:
    def __init__(self, master):
        # create the window, and set base properties
        self.frame = Toplevel(master)
        self.frame.grab_set()
        self.frame.wm_title("Scraper Input")

        # setup variables to store info
        startURL = StringVar()
        endURL = StringVar()
        nextPage = StringVar()
        nextPageID = IntVar()
        nextPagePreB = BooleanVar()
        nextPagePre = StringVar()
        content = StringVar()
        contentID = IntVar()
        multPages = BooleanVar()
        titleLoc = StringVar()
        titleLocID = IntVar()
        filename = StringVar()
        fileFormat = IntVar()

        # populate the window 
        Label(self.frame, text="Scraper Input").grid(row=0, columnspan=2)
        Label(self.frame, text="Start URL").grid(row=1, column=0)
        Entry(self.frame, textvariable=startURL).grid(row=1, column=1)
        Label(self.frame, text="End URL").grid(row=2, column=0)
        Entry(self.frame, textvariable=endURL).grid(row=2, column=1)
        Label(self.frame, text="Next Page").grid(row=3, column=0)
        Entry(self.frame, textvariable=nextPage).grid(row=3, column=1)
        Label(self.frame, text="Content").grid(row=4, column=0)
        Entry(self.frame, textvariable=content).grid(row=4, column=1)
        Label(self.frame, text="Multiple Pages").grid(row=5, column=0)
        Label(self.frame, text="Title Location").grid(row=6, column=0)
        Entry(self.frame, textvariable=titleLoc).grid(row=6, column=1)
        Label(self.frame, text="Filename").grid(row=7, column=0)
        Entry(self.frame, textvariable=filename).grid(row=7, column=1)
        Label(self.frame, text="File Format").grid(row=8, column=0)
        #Label(self.frame, text="").grid(row=, column=0)
        #Entry(self.frame, textvariable=).grid(row=, column=1

        # create scrape and cancel buttons
        Button(self.frame, text="Scrape", command=None, state="disabled").grid(row=9, column=0)
        Button(self.frame, text="Cancel", command=self.frame.destroy).grid(row=9,column=1)

        # set global padding for window
        for child in self.frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

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
