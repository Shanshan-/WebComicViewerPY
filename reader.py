# using guide from http://effbot.org/tkinterbook/tkinter-classes.htm
from tkinter import *
from tkinter import ttk
from scraper import *
from widgets import *

class Viewer:
    def __init__(self, master):
        self.menu, self.recent_menu = self.gen_menu(master)
        self.cframe = Frame(master)
        self.eframe = Frame(master)
        self.isEmpty = True

        #generate and display empty frame
        Label(self.eframe, text="No images to display now", fg="gray").pack()
        Button(self.eframe, text="QUIT", command=master.destroy).pack()
        Button(self.eframe, text="Scrape", command=self.open_scrape).pack()
        Button(self.eframe, text="Switch", command=self.switch_frame).pack()
        self.eframe.pack()

        #generate canvas frame
        self.canvas = Canvas(self.cframe, confine=False, scrollregion=(0, 0, swidth, sheight))
        self.canvas.config(width=swidth/2, height=sheight/2)
        hbar = Scrollbar(self.cframe, orient=HORIZONTAL, command=self.canvas.xview)
        hbar.pack(side=BOTTOM, fill=X)
        vbar = Scrollbar(self.cframe, orient=VERTICAL, command=self.canvas.yview)
        vbar.pack(side=RIGHT, fill=Y)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)

    # Generate the menu to go on top, and link as needed
    def gen_menu(self, rootFrame):
        menuBar = Menu(rootFrame)
        rootFrame.config(menu=menuBar)

        # File Options
        fileOpts = Menu(menuBar, tearoff=0)
        recentFiles = Menu(fileOpts, tearoff=0)
        fileOpts.add_command(label="Scrape New", command=self.open_scrape)
        fileOpts.add_separator()
        fileOpts.add_cascade(label="Open Recent", menu=recentFiles)
        recentFiles.add_command(label="<no recent files>", state="disabled")
        fileOpts.add_command(label="Open Other", command=self.open_comic)

        # Viewer Options
        viewOpts = Menu(menuBar, tearoff=0)
        viewOpts.add_command(label="Switch Frames", command=self.switch_frame)
        viewOpts.add_command(label="<to be made>", command=NONE, state="disabled")
        viewOpts.add_command(label="Quit", command=rootFrame.destroy)

        # Put it all together and return
        menuBar.add_cascade(label="File Options", menu=fileOpts)
        menuBar.add_cascade(label="Viewer Options", menu=viewOpts)
        return menuBar, recentFiles

    def open_scrape(self):
        Scraper(self.cframe)
        #TODO: implement taking results from pop-up and implementing them

    def switch_frame(self):
        self.isEmpty = not self.isEmpty
        if not self.isEmpty:
            self.eframe.pack_forget()
            self.cframe.pack()
        else:
            self.cframe.pack_forget()
            self.eframe.pack()

    def open_comic(self):
        print("Opening new comic")

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
