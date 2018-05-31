from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gen_scraper import Scraper
from widgets import *
from loader import loadFiles
from PIL import Image, ImageTk
from copy import deepcopy
from os.path import relpath
import codecs

# recent comic constants
NORECENT = "<no recent files>"
RECENTLIMIT = 10

# save file constants
SAVEPATH = "wcv.config"
SAVECATDIV = "$$\n"
SAVELINEDIV = "|"
FILE_ENC = 'base64'
STR_ENC = 'utf8'

# comic frame constants
EFRAME = 0
CFRAME = 1
FFRAME = 2

FavList = []

class Viewer:
    def __init__(self, master):
        self.menu, self.recent_menu = self.gen_menu(master)
        self.cframe = Frame(master) # frame 0
        self.eframe = Frame(master) # frame 1
        self.fframe = Frame(master) # frame 2
        self.curFrame = EFRAME # refers to the frame to be displayed
        self.switch_frame(self.curFrame)

        #generate empty frame
        photo = ImageTk.PhotoImage(Image.open("img/xkcd #3 - Hello, island.jpg"))
        l = Label(self.eframe, image=photo)
        l.image = photo # needed to prevent garbage collection
        l.pack()
        Button(self.eframe, text="Scrape", command=self.open_scrape).pack(pady=5)
        Button(self.eframe, text="Favorites", command=lambda:self.switch_frame(2)).pack(pady=2)
        Button(self.eframe, text="Open", command=self.open_comic).pack(pady=2)
        Button(self.eframe, text="OpenD", command=lambda:self.open_comic("./img/lyoko extras/")).pack(pady=2)
        Button(self.eframe, text="QUIT", command=master.destroy).pack(pady=2)
        Label(self.eframe, text="image from xkcd", fg="gray").pack(side=BOTTOM, anchor=SE)

        #generate canvas frame
        self.ccanvas = Canvas(self.cframe)
        self.ccanvas.config(width=self.cframe.winfo_vrootwidth())
        self.ccanvas.config(height=self.cframe.winfo_vrootheight())
        hbar = Scrollbar(self.cframe, orient=HORIZONTAL, command=self.ccanvas.xview)
        hbar.pack(side=BOTTOM, fill=X)
        vbar = Scrollbar(self.cframe, orient=VERTICAL, command=self.ccanvas.yview)
        vbar.pack(side=RIGHT, fill=Y)
        self.ccanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.ccanvas.pack(side=RIGHT, expand=True, fill=BOTH)

        #generate frame to go onto canvas
        self.canvas_frame = Frame(self.ccanvas)
        self.cframe.update()
        self.ccreated_frame = self.ccanvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        self.ccanvas.bind("<Configure>", self.CanvasFrameWidthHandler) # binding to center comic frame
        self.ccanvas.bind_all("<MouseWheel>", self.CanvasMouseWheelHandler) #binding for comic scrolling

        #generate favorites frame
        self.update_faves()

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
        viewOpts.add_command(label="<to be made>", command=NONE, state="disabled")
        viewOpts.add_command(label="Quit", command=rootFrame.destroy)
        viewOpts.add_command(label="Scroll Pos", command=lambda:print(self.comic_vbar.get()))
        viewOpts.add_command(label="Set Scroll", command=lambda:print(self.comic_vbar.set(0.5, 1.0)))

        # Frame Options
        gotoOpt = Menu(menuBar, tearoff=0)
        gotoOpt.add_command(label="Home", command=lambda:self.switch_frame(0))
        gotoOpt.add_command(label="Current Comic", command=lambda:self.switch_frame(1))
        gotoOpt.add_command(label="Favorites", command=lambda:self.switch_frame(2))
        gotoOpt.add_command(label="Scraper", command=lambda:self.switch_frame(3), state="disabled")
        gotoOpt.add_command(label="Settings", command=lambda:self.switch_frame(3), state="disabled")

        # Put it all together and return
        menuBar.add_cascade(label="Go To", menu=gotoOpt)
        menuBar.add_cascade(label="File Options", menu=fileOpts)
        menuBar.add_cascade(label="Viewer Options", menu=viewOpts)
        return menuBar, recentFiles

    # Generates a list of all items in the recently opened menu
    def get_recent(self):
        ans = []
        last = self.recent_menu.index("end")
        if last is None: # no recent comics
            return []
        for x in range(last+1):
            txt = self.recent_menu.entrycget(x, "label")
            ans.append(txt)
            x += 1
        return ans

    # Adds an item to the recently opened menu
    def add_recent(self, directory):
        #get basic info
        title = (directory.split("/"))[-2] + "/" + (directory.split("/"))[-1]
        if self.recent_menu.entrycget(0, "label") == NORECENT:
            self.recent_menu.delete(0)

        #delete duplicate entries and trim list
        entries = self.get_recent()
        for x in range(len(entries)-1, RECENTLIMIT-1, -1):
            self.recent_menu.delete(x)
        entries = self.get_recent()
        for x in range(len(entries)-1, -1, -1):
            if entries[x] == title:
                self.recent_menu.delete(x)

        self.recent_menu.insert(0, itemType="command", label=title, command=lambda:self.open_comic(directory))

    # Re-draw the favorites frame according to FavList
    def update_faves(self):
        for each in self.fframe.winfo_children():
            each.destroy()
        FavList.sort()
        for idx, entry in enumerate(FavList):
            b1 = Button(self.fframe, text=entry[0], command=lambda arg=entry[1]:self.open_comic(arg))
            b2 = Button(self.fframe, text="X", command=lambda arg=entry:self.del_fave(arg))
            b1.grid(row=idx, column=0)
            b2.grid(row=idx, column=1)
        for each in self.fframe.winfo_children():
            each.grid_configure(padx=10, pady=2, sticky="ew")
            each.configure(font=("Brittanic Bold", 14))
        b = Button(self.fframe, text="Add New Favorite", command=self.add_fave)
        b.grid(row=len(FavList), columnspan=2, padx=10, pady=20, sticky="ew")

    # Add a new favorite comic to the favorites frame
    def add_fave(self):
        prompt = "Please select a directory"
        absdir = filedialog.askdirectory(parent=self.fframe, initialdir="./img", title=prompt)
        directory = relpath(absdir, ".")
        title = (directory.split("/"))[-1]
        if not [title, directory] in FavList:
            FavList.append([title, directory])
        self.update_faves()

    # Delete a comic from the favorites page
    def del_fave(self, entry):
        FavList.remove(entry)
        self.update_faves()

    # Initialize the scraper
    def open_scrape(self):
        Scraper(self.cframe)
        #TODO: implement taking results from pop-up and implementing them

    # Switch to the frame indicated by nextFrame
    def switch_frame(self, nextFrame):
        #hide current frame
        if self.curFrame == EFRAME:
            self.eframe.pack_forget()
        elif self.curFrame == CFRAME:
            self.cframe.pack_forget()
        elif self.curFrame == FFRAME:
            self.fframe.pack_forget()

        #show next frame
        self.curFrame = nextFrame
        if nextFrame == EFRAME:
            self.eframe.pack(expand=True, fill=BOTH, side=TOP)
        elif nextFrame == CFRAME:
            self.cframe.pack(expand=True, fill=BOTH, side=TOP)
        elif nextFrame == FFRAME:
            self.fframe.pack(expand=True, side=TOP)

    # Load indicated comic
    def open_comic(self, directory=None):
        #clear all items currently in canvas
        for each in self.canvas_frame.winfo_children():
            each.destroy()

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
            l = Label(self.canvas_frame, image=page)
            l.image = page # needed to prevent garbage collection
            l.pack(anchor=CENTER)
        self.ccanvas.update()
        otherdim = self.ccanvas.bbox("all")
        self.ccanvas.config(scrollregion=otherdim)
        self.switch_frame(1)
        #TODO: add option of viewing up to ~50 pages at a time, with next/back buttons

    # Event Handlers
    def CanvasFrameWidthHandler(self, event):
        canvas_width = event.width
        self.ccanvas.itemconfig(self.ccreated_frame, width=canvas_width)

    def CanvasMouseWheelHandler(self, event):
        if self.curFrame == CFRAME:
            self.ccanvas.yview_scroll(-1*int(event.delta/60), "units")

# Load the save file from memory
def loadSave():
    from os.path import exists
    if not exists(SAVEPATH):
        return
    f = open(SAVEPATH, "r")
    section = -1
    for line in f:
        if line == SAVECATDIV:
            section += 1
            continue
        rline1 = codecs.encode(line, STR_ENC, 'strict')
        rline2 = codecs.decode(rline1, FILE_ENC, 'strict')
        rline3 = codecs.decode(rline2, STR_ENC, 'strict')
        rline = rline3.strip()
        tmp = rline.split(SAVELINEDIV)
        if section == 0: #favorites
            if not exists(tmp[1]):
                print("The favorite comic %s at \"%s\" does not exists. Removing..." % (tmp[0], tmp[1]))
                continue
            FavList.append(deepcopy(tmp))
    f.close()

# Generate a save file and save it
def makeSave():
    f = open(SAVEPATH, "w")
    f.write(SAVECATDIV)
    for each in FavList:
        fline0 = each[0] + SAVELINEDIV + each[1]
        fline1 = codecs.encode(fline0, STR_ENC, 'strict')
        fline2 = codecs.encode(fline1, FILE_ENC, 'strict')
        fline3 = codecs.decode(fline2, STR_ENC, 'strict')
        f.write(fline3)
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
    root.wm_iconbitmap('./img/icon1.ico')
    app = Viewer(root)

    # start program and open window
    root.mainloop()
    makeSave()
    try:
        root.destroy()
    except TclError:
        pass
    except Exception as e:
        print("Error occurred: %s" % e)
