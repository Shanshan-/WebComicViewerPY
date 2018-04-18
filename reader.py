# using guide from http://effbot.org/tkinterbook/tkinter-classes.htm
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from scraper import *
from widgets import *
from loader import loadFiles
from PIL import Image, ImageTk
from copy import deepcopy

NORECENT = "<no recent files>"
RECENTLIMIT = 10

SAVEPATH = "wcv.config"
SAVECATDIV = "$$\n"
SAVELINEDIV = "|"

fave_list = []

class Viewer:
    def __init__(self, master):
        self.menu, self.recent_menu = self.gen_menu(master)
        self.cframe = Frame(master)
        self.eframe = Frame(master)
        self.isEmpty = True

        #generate and display empty frame
        photo = ImageTk.PhotoImage(Image.open("img/xkcd #3 - Hello, island.jpg"))
        l = Label(self.eframe, image=photo)
        l.image = photo # needed to prevent garbage collection
        l.pack()
        Label(self.eframe, text="No images to display now", fg="gray").pack()
        Button(self.eframe, text="QUIT", command=master.destroy).pack()
        Button(self.eframe, text="Scrape", command=self.open_scrape).pack()
        Button(self.eframe, text="Switch", command=self.switch_frame).pack()
        Button(self.eframe, text="Open", command=self.open_comic).pack()
        self.eframe.pack()

        #generate canvas frame
        self.scroll_canvas = Canvas(self.cframe)
        self.scroll_canvas.config(width=self.cframe.winfo_vrootwidth(), height=self.cframe.winfo_vrootheight())
        hbar = Scrollbar(self.cframe, orient=HORIZONTAL, command=self.scroll_canvas.xview)
        hbar.pack(side=BOTTOM, fill=X)
        vbar = Scrollbar(self.cframe, orient=VERTICAL, command=self.scroll_canvas.yview)
        vbar.pack(side=RIGHT, fill=Y)
        self.scroll_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.scroll_canvas.pack(side=TOP, expand=True, fill=BOTH)
        self.canvas = Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0,0), window=self.canvas, anchor="nw")

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
        recentFiles.add_command(label=NORECENT, state="disabled")
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

    def get_recent(self):
        ans = []
        last = self.recent_menu.index("end")
        if last is None:
            return []
        for x in range(last+1):
            txt = self.recent_menu.entrycget(x, "label")
            ans.append(txt)
            x += 1
        return ans

    def add_recent(self, directory):
        #get basic info
        #title = (directory.split("/"))[-1]
        title = directory
        if self.recent_menu.entrycget(0, "label") == NORECENT:
            self.recent_menu.delete(0)

        #delete duplicate entries
        entries = self.get_recent()
        for x in range(len(entries)-1, RECENTLIMIT-1, -1):
            self.recent_menu.delete(x)
        entries = self.get_recent()
        for x in range(len(entries)-1, -1, -1):
            if entries[x] == title:
                self.recent_menu.delete(x)

        self.recent_menu.insert(0, itemType="command", label=title, command=lambda:self.open_comic(directory))

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

    def open_comic(self, directory=None):
        #clear all items currently in canvas
        for each in self.canvas.winfo_children():
            each.pack_forget()

        if not directory:
            #open dialog to let user choose a directory, and use loader to load
            prompt = "Please select a directory"
            directory = filedialog.askdirectory(parent=self.eframe, initialdir="./img", title=prompt)
        files = loadFiles(directory)
        self.add_recent(directory)
        print("Displaying %s" % directory)

        #display in canvas
        for key, value in files.items():
            page = ImageTk.PhotoImage(Image.open(value.path))
            l = Label(self.canvas, image=page)
            l.image = page # needed to prevent garbage collection
            l.pack()
        #self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
        reqdim = (0, 0, self.scroll_canvas.winfo_reqheight(), self.scroll_canvas.winfo_width())
        otherdim = self.scroll_canvas.bbox("all")
        self.scroll_canvas.config(scrollregion=otherdim)
        print(reqdim, otherdim)
        #TODO: fix problems with scrollbar
        if self.isEmpty:
            self.switch_frame()

def loadSave():

    f = open(SAVEPATH, "r")
    section = -1
    for line in f:
        if line == SAVECATDIV:
            section += 1
            continue
        line = line.strip()
        tmp = line.split(SAVELINEDIV)
        if section == 0: #favorites
            fave_list.append(deepcopy(tmp))
    f.close()

def makeSave():
    f = open(SAVEPATH, "w")
    f.write(SAVECATDIV)
    for each in fave_list:
        f.write(each[0] + SAVELINEDIV + each[1] + "\n")
    f.write(SAVECATDIV)
    f.close()

if __name__ == "__main__":
    # create the root window which will hold all objects
    loadSave()
    root = Tk()
    sheight = int(root.winfo_screenheight() * 0.7)
    swidth = int(root.winfo_screenwidth() * 0.7)
    root.geometry('%sx%s' % (swidth, sheight))
    root.wm_title("WCV Reader")
    #genMenu(root)
    app = Viewer(root)

    # start program and open window
    root.mainloop()
    makeSave()
    try:
        root.destroy()
    except Exception as e:
        print("Error occured:%s" % e)
