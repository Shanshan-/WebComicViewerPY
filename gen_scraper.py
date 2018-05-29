import requests, bs4, os
from tkinter import ttk, filedialog
from widgets import *
from tkinter import *

DEFAULTLOC = "./img/"

class Scraper:
    def __init__(self, master, nested=True):
        # create the window, and set base properties
        self.frame = master
        self.master = master
        if nested:
            self.frame = Toplevel(master)
            self.frame.grab_set()
        self.frame.wm_title("Scraper Input")
        self.frame.config(padx=20, pady=10)
        self.last_save = DEFAULTLOC

        # setup variables to store info
        self.startURL = StringVar(value="")
        self.endURL = StringVar(value="")
        self.nextPage = StringVar(value="")
        self.nextPageID = StringVar(value="")
        self.nextPagePreB = BooleanVar(value=FALSE)
        self.nextPagePre = StringVar(value="")
        self.content = StringVar(value="")
        self.contentID = StringVar(value="")
        self.contentPreB = BooleanVar(value=FALSE)
        self.contentPre = StringVar(value="")
        self.multPages = BooleanVar(value=FALSE)
        self.titleLoc = StringVar(value="")
        self.titleLocID = StringVar(value="")
        self.comicname = StringVar(value="")
        self.filenameNum = BooleanVar(value=FALSE)
        self.filenameStartNum = IntVar(value=1)
        self.saveLoc = StringVar(value="")
        self.saveLocField = None #these last two used to dynamically update directory entry
        self.comicLoc = ""
        self.startURLEntry, self.endURLEntry = (None,)*2

        #add pre-built profile support
        self.defOption = StringVar(value="None")
        self.defChoices = ["None", "Code: Game Night", "Friendship is Dragons", "Royal Tutor", "Crystal GMs", "XKCD"]
        self.defMenu = OptionMenu(self.frame, self.defOption, *self.defChoices)
        self.defMenu.grid(row=10, column=7, columnspan=2, sticky="")
        self.defOption.trace('w', self.chooseDefault)

        # populate the window
        #TODO: allow for use of pre-built profiles
        useHinted = True
        self.create_form_hinted() if useHinted else self.create_form()

    def create_form_hinted(self):
        #scraping-related fields
        Label(self.frame, text="Start URL").grid(row=1, column=0)
        self.startURLEntry = HintedEntry(self.frame, hintTxt="Starting URL", textvariable=self.startURL)
        self.startURLEntry.grid(row=1, column=1, columnspan=3)
        Label(self.frame, text="End URL").grid(row=2, column=0)
        self.endURLEntry = HintedEntry(self.frame, hintTxt="Ending URL", textvariable=self.endURL)
        self.endURLEntry.grid(row=2, column=1, columnspan=3)

        Label(self.frame, text="Next Page\nSelector").grid(row=3, column=0)
        Radiobutton(self.frame, text="class(.)", variable=self.nextPageID, value=".", tristatevalue="x").grid(row=3, column=1)
        Radiobutton(self.frame, text="id(#)", variable=self.nextPageID, value="#", tristatevalue="x").grid(row=3, column=2)
        Radiobutton(self.frame, text="other", variable=self.nextPageID, value="", tristatevalue="x").grid(row=3, column=3)
        HintedEntry(self.frame, hintTxt="Next Page Selector", textvariable=self.nextPage).grid(row=4, column=1, columnspan=3)
        Checkbutton(self.frame, text="URL Prefix:", variable=self.nextPagePreB).grid(row=5, column=1)
        HintedEntry(self.frame, hintTxt="URL Prefix", textvariable=self.nextPagePre).grid(row=5, column=2, columnspan=2)

        Label(self.frame, text="Content\nSelector").grid(row=6, column=0)
        Radiobutton(self.frame, text="class(.)", variable=self.contentID, value=".", tristatevalue="x").grid(row=6, column=1)
        Radiobutton(self.frame, text="id(#)", variable=self.contentID, value="#", tristatevalue="x").grid(row=6, column=2)
        Radiobutton(self.frame, text="other", variable=self.contentID, value="", tristatevalue="x").grid(row=6, column=3)
        HintedEntry(self.frame, hintTxt="Image Selector", textvariable=self.content).grid(row=7, column=1, columnspan=3)
        Checkbutton(self.frame, text="URL Prefix:", variable=self.contentPreB).grid(row=8, column=1)
        HintedEntry(self.frame, hintTxt="URL Prefix", textvariable=self.contentPre).grid(row=8, column=2, columnspan=2)
        Checkbutton(self.frame, text="Multiple Pages", variable=self.multPages).grid(row=9, column=1, columnspan=3)

        # saving-related fields
        Label(self.frame, text="Page Title\nSelector").grid(row=1, column=5)
        Radiobutton(self.frame, text="class(.)", variable=self.titleLocID, value=".", tristatevalue="x").grid(row=1, column=6)
        Radiobutton(self.frame, text="id(#)", variable=self.titleLocID, value="#", tristatevalue="x").grid(row=1, column=7)
        Radiobutton(self.frame, text="other", variable=self.titleLocID, value="", tristatevalue="x").grid(row=1, column=8)
        HintedEntry(self.frame, hintTxt="Title Selector", textvariable=self.titleLoc).grid(row=2, column=6, columnspan=3)

        Label(self.frame, text="Filename").grid(row=3, column=5)
        HintedEntry(self.frame, hintTxt="Comic Name", textvariable=self.comicname).grid(row=3, column=6, columnspan=3)
        Checkbutton(self.frame, text="Add #", variable=self.filenameNum).grid(row=4, column=6)
        HintedEntry(self.frame, hintTxt="Starting Num, eg. ", textvariable=self.filenameStartNum).grid(row=4, column=7, columnspan=2)
        self.filenameStartNum.set(-1)

        Label(self.frame, text="Save Location").grid(row=5, column=5)
        self.saveLocField = HintedEntry(self.frame, hintTxt="\"./img/\" by default", textvariable=self.saveLoc)
        self.saveLocField.grid(row=5, column=6, columnspan=3)
        Button(self.frame, text="Choose Directory", command=self.setSaveLoc).grid(row=6, column=6, columnspan=2)

        # set global padding for above items
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=2, sticky="we")

        # other fields and elements
        title = Label(self.frame, text="Scraper Input", font=('Cooper Black', 24))
        title.grid(row=0, columnspan=9, padx=10, pady=10, sticky="we")
        ttk.Separator(self.frame, orient=VERTICAL).grid(row=1, column=4, rowspan=9, sticky="ns", padx=10)
        cancel = Button(self.frame, text="Cancel", command=self.frame.destroy)
        cancel.grid(row=10,column=5, padx=10, pady=10, sticky="we")
        scrape = Button(self.frame, text="Scrape", command=self.start_scrape)
        scrape.grid(row=10, column=3, padx=10, pady=10, sticky="we", ipadx=10)

    def create_form(self):
        #scraping-related fields
        Label(self.frame, text="Start URL").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.startURL).grid(row=1, column=1, columnspan=3)
        Label(self.frame, text="End URL").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.endURL).grid(row=2, column=1, columnspan=3)

        Label(self.frame, text="Next Page\nSelector").grid(row=3, column=0)
        Radiobutton(self.frame, text="class(.)", variable=self.nextPageID, value=".", tristatevalue="x").grid(row=3, column=1)
        Radiobutton(self.frame, text="id(#)", variable=self.nextPageID, value="#", tristatevalue="x").grid(row=3, column=2)
        Radiobutton(self.frame, text="other", variable=self.nextPageID, value="", tristatevalue="x").grid(row=3, column=3)
        Entry(self.frame, textvariable=self.nextPage).grid(row=4, column=1, columnspan=3)
        Checkbutton(self.frame, text="URL Prefix:", variable=self.nextPagePreB).grid(row=5, column=1)
        Entry(self.frame, textvariable=self.nextPagePre).grid(row=5, column=2, columnspan=2)

        Label(self.frame, text="Content\nSelector").grid(row=6, column=0)
        Radiobutton(self.frame, text="class(.)", variable=self.contentID, value=".", tristatevalue="x").grid(row=6, column=1)
        Radiobutton(self.frame, text="id(#)", variable=self.contentID, value="#", tristatevalue="x").grid(row=6, column=2)
        Radiobutton(self.frame, text="other", variable=self.contentID, value="", tristatevalue="x").grid(row=6, column=3)
        Entry(self.frame, textvariable=self.content).grid(row=7, column=1, columnspan=3)
        Checkbutton(self.frame, text="URL Prefix:", variable=self.contentPreB).grid(row=8, column=1)
        Entry(self.frame, textvariable=self.contentPre).grid(row=8, column=2, columnspan=2)
        Checkbutton(self.frame, text="Multiple Pages", variable=self.multPages).grid(row=9, column=1, columnspan=3)

        # saving-related fields
        Label(self.frame, text="Page Title\nSelector").grid(row=1, column=5)
        Radiobutton(self.frame, text="class(.)", variable=self.titleLocID, value=".", tristatevalue="x").grid(row=1, column=6)
        Radiobutton(self.frame, text="id(#)", variable=self.titleLocID, value="#", tristatevalue="x").grid(row=1, column=7)
        Radiobutton(self.frame, text="other", variable=self.titleLocID, value="", tristatevalue="x").grid(row=1, column=8)
        Entry(self.frame, textvariable=self.titleLoc).grid(row=2, column=6, columnspan=3)

        Label(self.frame, text="Filename").grid(row=3, column=5)
        Entry(self.frame, textvariable=self.comicname).grid(row=3, column=6, columnspan=3)
        Checkbutton(self.frame, text="Add #", variable=self.filenameNum).grid(row=4, column=6)
        Entry(self.frame, textvariable=self.filenameStartNum).grid(row=4, column=7, columnspan=2)
        self.filenameStartNum.set(-1)

        Label(self.frame, text="Save Location").grid(row=5, column=5)
        self.saveLocField = Entry(self.frame, textvariable=self.setSaveLoc)
        self.saveLocField.grid(row=5, column=6, columnspan=3)
        Button(self.frame, text="Choose Directory", command=self.setSaveLoc).grid(row=6, column=6, columnspan=2)

        # set global padding for above items
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=2, sticky="we")

        # other fields and elements
        title = Label(self.frame, text="Scraper Input", font=('Cooper Black', 24))
        title.grid(row=0, columnspan=9, padx=10, pady=10, sticky="we")
        ttk.Separator(self.frame, orient=VERTICAL).grid(row=1, column=4, rowspan=9, sticky="ns", padx=10)
        cancel = Button(self.frame, text="Cancel", command=self.frame.destroy)
        cancel.grid(row=10,column=5, padx=10, pady=10, sticky="we")
        scrape = Button(self.frame, text="Scrape", command=self.start_scrape)
        scrape.grid(row=10, column=3, padx=10, pady=10, sticky="we", ipadx=10)

    def chooseDefault(self, *args):
        choice = self.defOption.get()
        print(self.startURL.get())
        if choice == self.defChoices[0]: #None option
            self.startURL.set(value="")
            self.endURL.set(value="")
            self.nextPage.set(value="")
            self.nextPageID.set(value="")
            self.nextPagePreB.set(value=FALSE)
            self.nextPagePre.set(value="")
            self.content.set(value="")
            self.contentID.set(value="")
            self.contentPreB.set(value=FALSE)
            self.contentPre.set(value="")
            self.multPages.set(value=FALSE)
            self.titleLoc.set(value="")
            self.titleLocID.set(value="")
            self.comicname.set(value="")
            self.filenameNum.set(value=FALSE)
            self.filenameStartNum.set(value=-1)
            self.saveLoc.set(value="")
        elif choice == self.defChoices[1]: #Code Game Night Option
            self.startURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.endURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.nextPage.set('a[rel="next"]')
            self.nextPageID.set("")
            self.nextPagePreB.set(TRUE)
            self.nextPagePre.set("http://codegamenight.thecomicseries.com")
            self.content.set("#comicimage")
            self.contentID.set("")
            self.contentPreB.set(FALSE)
            self.contentPre.set("")
            self.multPages.set(FALSE)
            self.titleLoc.set(".heading")
            self.titleLocID.set("")
            self.comicname.set("Code Game Night")
            self.filenameNum.set(FALSE)
            self.filenameStartNum.set(-1)
            self.saveLoc.set("./img/Code Game Night/")
        elif choice == self.defChoices[2]: #FiD Option
            self.startURL.set("http://friendshipisdragons.thecomicseries.com/comics/1050")
            self.endURL.set("http://friendshipisdragons.thecomicseries.com/comics/")
            self.nextPage.set('a[rel="next"]')
            self.nextPageID.set("")
            self.nextPagePreB.set(TRUE)
            self.nextPagePre.set("http://friendshipisdragons.thecomicseries.com")
            self.content.set("#comicimage")
            self.contentID.set("")
            self.contentPreB.set(FALSE)
            self.contentPre.set("")
            self.multPages.set(FALSE)
            self.titleLoc.set(".heading")
            self.titleLocID.set("")
            self.comicname.set("MLP FiD")
            self.filenameNum.set(FALSE)
            self.filenameStartNum.set(-1)
            self.saveLoc.set("./img/MLP FiD/")
        elif choice == self.defChoices[3]: #Code Game Night Option
            self.startURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.endURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.nextPage.set('a[rel="next"]')
            self.nextPageID.set("")
            self.nextPagePreB.set(TRUE)
            self.nextPagePre.set("http://codegamenight.thecomicseries.com")
            self.content.set("#comicimage")
            self.contentID.set("")
            self.contentPreB.set(FALSE)
            self.contentPre.set("")
            self.multPages.set(FALSE)
            self.titleLoc.set("alt")
            self.titleLocID.set("")
            self.comicname.set("Code Game Night")
            self.filenameNum.set(FALSE)
            self.filenameStartNum.set(1)
            self.saveLoc.set("./img/Code Game Night/")
        elif choice == self.defChoices[4]: #Code Game Night Option
            self.startURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.endURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.nextPage.set('a[rel="next"]')
            self.nextPageID.set("")
            self.nextPagePreB.set(TRUE)
            self.nextPagePre.set("http://codegamenight.thecomicseries.com")
            self.content.set("#comicimage")
            self.contentID.set("")
            self.contentPreB.set(FALSE)
            self.contentPre.set("")
            self.multPages.set(FALSE)
            self.titleLoc.set("alt")
            self.titleLocID.set("")
            self.comicname.set("Code Game Night")
            self.filenameNum.set(FALSE)
            self.filenameStartNum.set(1)
            self.saveLoc.set("./img/Code Game Night/")
        elif choice == self.defChoices[5]: #Code Game Night Option
            self.startURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.endURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.nextPage.set('a[rel="next"]')
            self.nextPageID.set("")
            self.nextPagePreB.set(TRUE)
            self.nextPagePre.set("http://codegamenight.thecomicseries.com")
            self.content.set("#comicimage")
            self.contentID.set("")
            self.contentPreB.set(FALSE)
            self.contentPre.set("")
            self.multPages.set(FALSE)
            self.titleLoc.set("alt")
            self.titleLocID.set("")
            self.comicname.set("Code Game Night")
            self.filenameNum.set(FALSE)
            self.filenameStartNum.set(1)
            self.saveLoc.set("./img/Code Game Night/")
        elif choice == self.defChoices[6]: #Code Game Night Option
            self.startURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.endURL.set("http://codegamenight.thecomicseries.com/comics/")
            self.nextPage.set('a[rel="next"]')
            self.nextPageID.set("")
            self.nextPagePreB.set(TRUE)
            self.nextPagePre.set("http://codegamenight.thecomicseries.com")
            self.content.set("#comicimage")
            self.contentID.set("")
            self.contentPreB.set(FALSE)
            self.contentPre.set("")
            self.multPages.set(FALSE)
            self.titleLoc.set("alt")
            self.titleLocID.set("")
            self.comicname.set("Code Game Night")
            self.filenameNum.set(FALSE)
            self.filenameStartNum.set(1)
            self.saveLoc.set("./img/Code Game Night/")
        Tk.update(self.master)
        print(self.startURL.get())
        #TODO: HintedEntries should update text, not hint text
        # starting point: https://stackoverflow.com/questions/6548837/how-do-i-get-an-event-callback-when-a-tkinter-entry-widget-is-modified, https://www.google.com/search?q=tkinter+bind+to+when+associated+value+changes&ie=utf-8&oe=utf-8&client=firefox-b-1-ab

    def setSaveLoc(self):
        self.saveLoc.set(filedialog.askdirectory(parent=self.frame, initialdir="./img", title="Choose destination"))
        self.saveLocField.insert(END, self.saveLoc.get())

    def start_scrape(self):
        #TODO: add in scrape constraints checks
        args = ScrapeSettings()
        args.startnum = self.filenameStartNum.get()
        args.starturl = self.startURL.get()
        args.endurl = self.endURL.get()
        args.nextsel = self.nextPageID.get() + self.nextPage.get()
        args.nextpref = self.nextPagePre.get() if self.nextPagePreB.get() else ""
        args.imagesel = self.contentID.get() + self.content.get()
        args.imagepref = self.contentPre.get() if self.contentPreB.get() else ""
        args.titlesel = self.titleLocID.get() + self.titleLoc.get()
        args.comicname = self.comicname.get()
        args.addnum = True if self.filenameNum.get() else False
        args.saveloc = self.saveLoc.get()

        # Try to scrape, and provide feedback
        try:
            gen_scrape(args)
            feedback = "Scrape Successful"
            cf = self.frame
        except Exception as scrape_error:
            feedback = "Scrape Failed:\n%s" % scrape_error
            cf = None
        self.comicLoc = args.saveloc
        #Dialog(self.frame, feedback, dFrame=cf, title="Scrape Results", btnTxt="Close")
        Dialog(self.frame, feedback, dFrame=None, title="Scrape Results", btnTxt="Close")

# class to pass into a scraper function, and to be populated and used based on function
# (kinda like a c library struct)
class ScrapeSettings:
    def __init__(self, startnum=1, endnum=-1, starturl="", endurl="", imagesel="", imagepref="", pagetitlesel="",
                 comicname="", addnum=False, nextsel="", nextpref="", saveloc="./img/",
                 nest=True, foldername="", multpages=False, numInStartURL=True):
        self.startnum = startnum
        self.endnum = endnum
        self.starturl = starturl
        self.endurl = endurl
        self.imagesel = imagesel
        self.imagepref = imagepref
        self.titlesel = pagetitlesel
        self.comicname = comicname
        self.addnum = addnum
        self.nextsel = nextsel
        self.nextpref = nextpref
        self.saveloc = saveloc
        self.multpages = multpages
        self.urlHasStartNum = numInStartURL #TODO: add this and nest to GUI
        if nest:
            self.saveloc += foldername + "/" if not foldername == "" else comicname + "/"
        self.DIV = "|"

    def setRange(self, start, stop):
        self.startnum = start
        self.endnum = stop
    def setImageSettings(self, selector, prefix):
        self.imagesel = selector
        self.imagepref = prefix
    def setTitleSettings(self, selector):
        self.titlesel = selector
    def setFileSettings(self, filenameprefix, addnum, fileForm, saveloc):
        self.comicname = filenameprefix
        self.addnum = addnum
        self.fileform = fileForm
        self.saveloc = saveloc
    def setNext(self, selector, prefix):
        self.nextsel = selector
        self.nextpref = prefix
    def exportSettings(self):
        ans = ""
        for key, value in vars(self).items():
            ans += key + "=" + str(value) + self.DIV
        return ans
    def importSettings(self, instr):
        lines = instr.split(self.DIV)
        for each in lines:
            div = each.find("=")
            self.__setattr__(each[:div], each[div+1:])

def gen_scrape(settings):
    if not settings.starturl or settings.imagesel:
        raise Exception("Must have both starting URL and an image selector")
    try:
        curPage = int(settings.starturl[settings.starturl.rfind("/")+1:])
    except ValueError:
        curPage = settings.startnum if settings.startnum >= 0 else ""
    curUrl = settings.starturl
    curUrl += str(curPage) if curUrl.find(str(curPage)) == -1 else ""
    while True:
        #create soup from website
        print("Getting %s #%d" % (settings.comicname, curPage))
        res = requests.get(curUrl)
        if res.status_code == 404:
            raise Exception("URL \"%s\" invalid... ending scrape" % curUrl)
        res.raise_for_status()
        pageSoup = bs4.BeautifulSoup(res.text, "html.parser")
        try:
            pageTitle = pageSoup.select(settings.titlesel)[0].getText()
        except:
            raise Exception("Unable to extract title")

        #extract image url and name
        try:
            imgList = enumerate(pageSoup.select(settings.imagesel))
        except:
            raise Exception("Unable to use given image selector to find images")
        for indx, imgElem in imgList:
            imgUrl = settings.imagepref + imgElem.get('src')
            imgFormat = imgUrl[imgUrl.rfind("."):]
            if settings.multpages:
                pageTitle = "Chapter %d Page %d" % (curPage, indx+1)
            if not pageTitle:
                raise Exception("Page Title is empty")

            # scrape the image
            res2 = requests.get(imgUrl)
            res2.raise_for_status()

            # write img to file
            for char in "\/?:*<>\"|":
                pageTitle = pageTitle.replace(char, "_")
            name1 = "%s%s" % (settings.saveloc, settings.comicname)
            #name2 = "%s.%s" % (title, settings.fileform)
            name2 = "%s%s" % (pageTitle, imgFormat)
            name = "%s #%d - %s" % (name1, curPage, name2) if settings.addnum else "%s - %s" % (name1, name2)
            if not os.path.exists(settings.saveloc):
                try: #this attempts to fix a race condition
                    os.makedirs(settings.saveloc)
                except OSError:
                    pass
            file = open(name, 'wb')
            for chunk in res2.iter_content(100000):
                file.write(chunk)
            file.close()
            if not settings.multpages:
                break

        # get next page and set curUrl
        if not settings.nextsel:
            #must build nexturl from cururl (eg. for heine)
            nexturl = settings.starturl + str(curPage + 1)
        else:
            if not pageSoup.select(settings.nextsel):
                break
            nexturl = settings.nextpref + pageSoup.select(settings.nextsel)[0].get("href")
        if nexturl == curUrl or nexturl == settings.endurl:
            break
        curUrl = nexturl
        curPage = curPage + 1
        if curPage == settings.endnum+1:
            break

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # create the root window which will hold all objects
        root = Tk()
        app = Scraper(root, nested=False)

        # start program and open window
        root.mainloop()
        try:
            root.destroy()
        except TclError:
            pass
        except Exception as e:
            print("Error occurred: %s" % e)
    elif "-t" in sys.argv:
        lyoko = ScrapeSettings(startnum=100, endnum=120, starturl="http://codegamenight.thecomicseries.com/comics/",
                               imagesel="#comicimage", pagetitlesel="alt", comicname="Code Game Night",
                               nextsel='a[rel="next"]', nextpref="http://codegamenight.thecomicseries.com", nest=True)
        gems = ScrapeSettings(startnum=13, endnum=17, starturl="http://crystalgms.thecomicseries.com/comics/",
                              nextsel='a[rel="next"]', nextpref="http://crystalgms.thecomicseries.com", nest=True,
                              imagesel="#comicimage", pagetitlesel="alt", comicname="Crystal GMs", addnum=True)
        heine = ScrapeSettings(startnum=59, starturl="http://mangaseeonline.us/read-online/The-Royal-Tutor-chapter-",
                               nextsel="", nest=True, imagesel=".fullchapimage img", comicname="Royal Tutor Heine",
                               multpages=True)
        gen_scrape(heine)
        tmp = lyoko.exportSettings()
        tmp1 = ScrapeSettings()
        tmp1.importSettings(tmp)