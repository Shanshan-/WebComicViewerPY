# using guide from http://effbot.org/tkinterbook/tkinter-classes.htm
from tkinter import *
from tkinter import ttk

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
        self.startURL = StringVar(value="")
        self.endURL = StringVar(value="")
        self.nextPage = StringVar(value="")
        self.nextPageID = IntVar(value=0)
        self.nextPagePreB = BooleanVar(value=FALSE)
        self.nextPagePre = StringVar(value="")
        self.content = StringVar(value="")
        self.contentID = IntVar(value=0)
        self.multPages = BooleanVar(value=FALSE)
        self.titleLoc = StringVar(value="")
        self.titleLocID = IntVar(value=0)
        self.filename = StringVar(value="")
        self.filenameNum = BooleanVar(value=FALSE)
        self.fileFormat = StringVar(value=".jpg")

        # populate the window
        self.create_form()

        Button(self.frame, text="Scrape", command=None, state="disabled").grid(row=8, column=3, padx=10, pady=10, sticky="we")
        Button(self.frame, text="Cancel", command=self.frame.destroy).grid(row=8,column=5, padx=10, pady=10, sticky="we")

    def create_form(self):
        #TODO: figure out why radio buttons are buggy
        #scraping-related fields
        Label(self.frame, text="Start URL").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.startURL).grid(row=1, column=1, columnspan=3)
        Label(self.frame, text="End URL").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.endURL).grid(row=2, column=1, columnspan=3)

        Label(self.frame, text="Next Page").grid(row=3, column=0)
        Radiobutton(self.frame, text="div", variable=self.nextPageID, value=0).grid(row=3, column=1)
        Radiobutton(self.frame, text="class", variable=self.nextPageID, value=1).grid(row=3, column=2)
        Radiobutton(self.frame, text="id", variable=self.nextPageID, value=2).grid(row=3, column=3)
        Entry(self.frame, textvariable=self.nextPage).grid(row=4, column=1, columnspan=3)
        Checkbutton(self.frame, text="Prefix:", variable=self.nextPagePreB).grid(row=4, column=1)
        Entry(self.frame, textvariable=self.nextPagePre).grid(row=4, column=2, columnspan=2)

        Label(self.frame, text="Content").grid(row=5, column=0)
        Radiobutton(self.frame, text="div", variable=self.contentID, value=0).grid(row=5, column=1)
        Radiobutton(self.frame, text="class", variable=self.contentID, value=1).grid(row=5, column=2)
        Radiobutton(self.frame, text="id", variable=self.contentID, value=2).grid(row=5, column=3)
        Entry(self.frame, textvariable=self.content).grid(row=6, column=1, columnspan=3)
        Checkbutton(self.frame, text="Multiple Pages", variable=self.multPages)\
            .grid(row=7, column=1, columnspan=3)

        # saving-related fields
        Label(self.frame, text="Title Location").grid(row=1, column=5)
        Radiobutton(self.frame, text="div", variable=self.titleLocID, value=0).grid(row=1, column=6)
        Radiobutton(self.frame, text="class", variable=self.titleLocID, value=1).grid(row=1, column=7)
        Radiobutton(self.frame, text="id", variable=self.titleLocID, value=2).grid(row=1, column=8)
        Entry(self.frame, textvariable=self.titleLoc).grid(row=2, column=6, columnspan=3)

        Label(self.frame, text="Filename").grid(row=3, column=5)
        Checkbutton(self.frame, text="#", variable=self.filenameNum).grid(row=3, column=6)
        Entry(self.frame, textvariable=self.filename).grid(row=3, column=7, columnspan=2)

        Label(self.frame, text="File Format").grid(row=4, column=5)
        Radiobutton(self.frame, text=".jpg", variable=self.fileFormat, value=".jpg").grid(row=4, column=6)
        Radiobutton(self.frame, text=".png", variable=self.fileFormat, value=".png").grid(row=4, column=7)

        # set global padding for above items
        for child in self.frame.winfo_children():
            child.grid_configure(padx=8, pady=2, sticky="we")

        # other fields and elements
        Label(self.frame, text="Scraper Input", font=('Cooper Black', 24)).grid(row=0, columnspan=9, padx=10, pady=10, sticky="we")
        ttk.Separator(self.frame, orient=VERTICAL).grid(row=1, column=4, rowspan=7, sticky="ns")


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
