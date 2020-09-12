import requests, bs4, os, json
from tkinter import ttk, filedialog
from widgets import *
from tkinter import *

DEFAULTLOC = "./img/"

class Scraper:
    def __init__(self, master, defaultJson, nested=True):
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
        self.baseURL = StringVar(value="")
        self.pageStartNum = IntVar(value=1)
        self.pageEndNum = IntVar(value=-1)
        self.nextPage = StringVar(value="")
        self.nextPagePreB = BooleanVar(value=FALSE)
        self.nextPagePre = StringVar(value="")
        self.content = StringVar(value="")
        self.contentPreB = BooleanVar(value=FALSE)
        self.contentPre = StringVar(value="")
        self.multPages = BooleanVar(value=FALSE)
        self.titleLoc = StringVar(value="")
        self.titleLocB = BooleanVar(value=TRUE)
        self.titleLocAttr = StringVar(value="")
        self.comicname = StringVar(value="")
        self.filenameNum = BooleanVar(value=FALSE)
        self.saveLoc = StringVar(value="")
        self.saveLocField = None #used to dynamically update directory entry
        self.comicLoc = "" #used to store location of scraped comic, potentially for use in reader
        self.baseURLEntry = (None,)
        self.defaultData = defaultJson.get("comicSettings")
        self.template = ""

        #add pre-built profile support
        self.defOption = StringVar(value="None")
        self.defChoices = [x["name"] for x in self.defaultData]
        self.defMenu = OptionMenu(self.frame, self.defOption, *self.defChoices)
        #self.defMenu['menu'].entryconfig("XKCD", state="disabled")
        self.defOption.trace('w', self.chooseDefault)

        # populate the window
        useHinted = True
        self.create_form_hinted() if useHinted else None

    def create_form_hinted(self):
        #URL starting and stopping points
        Label(self.frame, text="Start URL").grid(row=1, column=0)
        self.baseURLEntry = HintedEntry(self.frame, hintTxt="Base URL", textvariable=self.baseURL)
        self.baseURLEntry.grid(row=1, column=1, columnspan=6)
        HintedEntry(self.frame, hintTxt="Start #, eg.", textvariable=self.pageStartNum).grid(row=1, column=7)
        HintedEntry(self.frame, hintTxt="End #, eg.", textvariable=self.pageEndNum).grid(row=1, column=8)

        # Content Selectors
        Label(self.frame, text="Content\nSelector").grid(row=2, column=0)
        HintedEntry(self.frame, hintTxt="CSS selector for image", textvariable=self.content).grid(row=2, column=1, columnspan=3)
        Checkbutton(self.frame, text="URL Prefix:", variable=self.contentPreB).grid(row=3, column=1)
        HintedEntry(self.frame, hintTxt="URL Prefix", textvariable=self.contentPre).grid(row=3, column=2, columnspan=2)
        Checkbutton(self.frame, text="Multiple Pages", variable=self.multPages).grid(row=4, column=1, columnspan=3)

        # Next Page Selectors
        Label(self.frame, text="Next Page\nSelector").grid(row=5, column=0)
        HintedEntry(self.frame, hintTxt="CSS selector for next page", textvariable=self.nextPage).grid(row=5, column=1, columnspan=3)
        Checkbutton(self.frame, text="URL Prefix:", variable=self.nextPagePreB).grid(row=6, column=1)
        HintedEntry(self.frame, hintTxt="URL Prefix", textvariable=self.nextPagePre).grid(row=6, column=2, columnspan=2)

        # Filename Prefix
        Label(self.frame, text="Filename\nPrefix").grid(row=2, column=5)
        HintedEntry(self.frame, hintTxt="Comic Name", textvariable=self.comicname).grid(row=2, column=6, columnspan=2)
        Checkbutton(self.frame, text="Add #", variable=self.filenameNum).grid(row=2, column=8)

        # Page Title Selectors
        Label(self.frame, text="Page Title\nSelector").grid(row=3, column=5)
        HintedEntry(self.frame, hintTxt="CSS selector for page title", textvariable=self.titleLoc).grid(row=3, column=6, columnspan=3)
        Radiobutton(self.frame, text="In Text", variable=self.titleLocB, value=TRUE, tristatevalue="x").grid(row=4, column=6)
        Radiobutton(self.frame, text="In Attr", variable=self.titleLocB, value=FALSE, tristatevalue="x").grid(row=4, column=7)
        HintedEntry(self.frame, hintTxt="CSS Atribute", textvariable=self.titleLocAttr).grid(row=4, column=8)
        #TODO: above entry should be disabled when self.titleLocB is TRUE

        # Save Location Details
        Label(self.frame, text="Save Location").grid(row=5, column=5)
        self.saveLocField = HintedEntry(self.frame, hintTxt="\"./img/\" by default", textvariable=self.saveLoc)
        self.saveLocField.grid(row=5, column=6, columnspan=3)
        Button(self.frame, text="Choose Directory", command=self.setSaveLoc).grid(row=6, column=6, columnspan=2)

        # set global padding for above items
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=2, sticky="we")

        # other fields and elements
        title = Label(self.frame, text="Scraper Input", font=('Cooper Black', 24)) #large title
        title.grid(row=0, columnspan=9, padx=10, pady=10, sticky="we")
        ttk.Separator(self.frame, orient=VERTICAL).grid(row=2, column=4, rowspan=5, sticky="ns", padx=10, pady=5) #middle line
        cancel = Button(self.frame, text="Cancel", command=self.frame.destroy)
        cancel.grid(row=7,column=5, padx=10, pady=10, sticky="we")
        scrape = Button(self.frame, text="Scrape", command=self.start_scrape)
        scrape.grid(row=7, column=3, padx=10, pady=10, sticky="we", ipadx=10)
        self.defMenu.grid(row=7, column=7, columnspan=2, sticky="e")
        Label(self.frame, text='NOTE: "#" for id, "." for class').grid(row=7, column=0, columnspan=2)

    def chooseDefault(self, *args):
        choice = self.defOption.get()
        choice = [x for x in self.defaultData if x["name"] == choice][0]
        print(self.baseURL.get())
        self.baseURL.set(value=choice["baseURL"])
        self.pageStartNum.set(value=choice["startNum"])
        self.pageEndNum.set(value=choice["endNum"])
        self.nextPage.set(value=choice["nextSelector"])
        self.nextPagePreB.set(value=TRUE) if choice["nextPrefix"] else self.nextPagePreB.set(value=FALSE)
        self.nextPagePre.set(value=choice["nextPrefix"])
        self.content.set(value=choice["contentSelector"])
        self.contentPreB.set(value=TRUE) if choice["contentPrefix"] else self.contentPreB.set(value=FALSE)
        self.contentPre.set(value=choice["contentPrefix"])
        self.multPages.set(value=choice["multPages"])
        self.titleLoc.set(value=choice["titleSelector"])
        self.titleLocB.set(value=choice["titleLocationB"])
        self.titleLocAttr.set(value=choice["titleAttributeVal"])
        self.comicname.set(value=choice["comicName"])
        self.filenameNum.set(value=choice["filenameNum"])
        self.saveLoc.set(value=choice["saveLoc"])
        self.template = choice["template"]
        #TODO: look into selecting BS elements based on innerHTML contents, and  not just attribute values
        Tk.update(self.master)
        print(self.baseURL.get())
        #TODO: HintedEntries should update text, not hint text
        # starting point: https://stackoverflow.com/questions/6548837/how-do-i-get-an-event-callback-when-a-tkinter-entry-widget-is-modified, https://www.google.com/search?q=tkinter+bind+to+when+associated+value+changes&ie=utf-8&oe=utf-8&client=firefox-b-1-ab

    def setSaveLoc(self):
        self.saveLoc.set(filedialog.askdirectory(parent=self.frame, initialdir="./img", title="Choose destination"))
        self.saveLocField.insert(END, self.saveLoc.get())

    def start_scrape(self):
        args = ScrapeSettings()
        args.baseurl = self.baseURL.get()
        args.startnum = self.pageStartNum.get()
        args.endnum = self.pageEndNum.get()
        args.nextsel = self.nextPage.get()
        args.nextpref = self.nextPagePre.get() if self.nextPagePreB.get() else ""
        args.imagesel = self.content.get()
        args.imagepref = self.contentPre.get() if self.contentPreB.get() else ""
        args.multpages = self.multPages.get()
        args.titlesel = self.titleLoc.get()
        args.isTextTitle = self.titleLocB.get()
        args.titleAttr = self.titleLocAttr.get()
        args.comicname = self.comicname.get()
        args.addnum = True if self.filenameNum.get() else False
        args.saveloc = self.saveLoc.get()

        # Try to scrape, and provide feedback
        #TODO: scrape first image, then prompt user for confirmation
        try:
            if self.template == "MangaSee" or self.baseURL.get().find("mangasee123.com") >= 0:
                raise Exception("MangaSee websites are currently not supported")
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
    def __init__(self, startnum=1, endnum=-1, baseurl="", imagesel="", imagepref="", pagetitlesel="",
                 titleInText=True, titleAttr="", comicname="", addnum=False, nextsel="", nextpref="",
                 saveloc="./img/", multpages=False):
        self.startnum = startnum
        self.endnum = endnum
        self.baseurl = baseurl
        self.imagesel = imagesel
        self.imagepref = imagepref
        self.titlesel = pagetitlesel
        self.isTextTitle = titleInText
        self.titleAttr = titleAttr
        self.comicname = comicname
        self.addnum = addnum
        self.nextsel = nextsel
        self.nextpref = nextpref
        self.saveloc = saveloc
        self.multpages = multpages
        self.DIV = "|"

    def setRange(self, start, stop):
        self.startnum = start
        self.endnum = stop
    def setImageSettings(self, selector, prefix):
        self.imagesel = selector
        self.imagepref = prefix
    def setTitleSettings(self, selector, inText, titleAttr=""):
        self.titlesel = selector
        self.isTextTitle = inText
        self.titleAttr = titleAttr
    def setFileSettings(self, filenameprefix, addnum, saveloc):
        self.comicname = filenameprefix
        self.addnum = addnum
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
    #check conditions, and setup for scraping
    if not settings.baseurl or not settings.imagesel:
        raise Exception("Must have both starting URL and an image selector")
    if not os.path.exists(settings.saveloc):
        try:
            os.makedirs(settings.saveloc)
        except OSError:
            raise Exception("The indicated save directory does not exist, and could not be created")
    curPage = settings.startnum
    curUrl = settings.baseurl + str(curPage)

    #begin scraping
    while True:
        #create soup from website
        print("Getting %s #%d" % (settings.comicname, curPage))
        res = requests.get(curUrl)
        if res.status_code == 404:
            raise Exception("URL \"%s\" invalid" % curUrl)
        res.raise_for_status()
        pageSoup = bs4.BeautifulSoup(res.text, "html.parser")

        #get page title
        try:
            if not settings.titlesel:
                pageTitle = ""
            elif settings.isTextTitle:
                pageTitle = pageSoup.select(settings.titlesel)[0].getText()
            else:
                titleElem = pageSoup.select(settings.titlesel)
                pageTitle = titleElem[0].get(settings.titleAttr)
        except Exception as error:
            raise Exception("Unable to extract title: %s" % error)

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
            name2 = "%s%s" % (pageTitle, imgFormat)
            name = "%s - Page %d - %s" % (name1, curPage, name2) if settings.addnum else "%s - %s" % (name1, name2)
            file = open(name, 'wb')
            for chunk in res2.iter_content(100000):
                file.write(chunk)
            file.close()
            if not settings.multpages:
                break

        # get next page and set curUrl
        if not settings.nextsel: #must build nexturl from cururl (eg. for heine)
            nexturl = settings.baseurl + str(curPage + 1)
        else:
            try:
                nextElem = pageSoup.select(settings.nextsel)
            except:
                raise Exception("Cannot get next page with given selector")
            if not nextElem:
                break
            nexturl = settings.nextpref + nextElem[0].get("href")
        if nexturl == curUrl:
            break
        curUrl = nexturl
        curPage = curPage + 1
        if curPage == settings.endnum+1:
            break

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # create the root window which will hold all objects
        root = Tk()
        defaultFile = open("./defaults.json")
        defaults = json.load(defaultFile)
        app = Scraper(root, defaults, nested=False)

        # start program and open window
        root.mainloop()
        try:
            root.destroy()
        except TclError:
            pass
        except Exception as e:
            print("Error occurred: %s" % e)
        defaultFile.close()
    elif "-t" in sys.argv:
        lyoko = ScrapeSettings(startnum=100, endnum=120, baseurl="http://codegamenight.thecomicseries.com/comics/",
                               imagesel="#comicimage", pagetitlesel="alt", comicname="Code Game Night",
                               nextsel='a[rel="next"]', nextpref="http://codegamenight.thecomicseries.com")
        gems = ScrapeSettings(startnum=13, endnum=17, baseurl="http://crystalgms.thecomicseries.com/comics/",
                              nextsel='a[rel="next"]', nextpref="http://crystalgms.thecomicseries.com",
                              imagesel="#comicimage", pagetitlesel="alt", comicname="Crystal GMs", addnum=True)
        heine = ScrapeSettings(startnum=59, baseurl="http://mangaseeonline.us/read-online/The-Royal-Tutor-chapter-",
                               nextsel="", imagesel=".fullchapimage img", comicname="Royal Tutor Heine",
                               multpages=True)
        gen_scrape(heine)
        tmp = lyoko.exportSettings()
        tmp1 = ScrapeSettings()
        tmp1.importSettings(tmp)