import requests, bs4
from tkinter import *
from tkinter import ttk
from widgets import *

DEFAULTLOC = "./img/"

class Scraper:
    def __init__(self, master):
        # create the window, and set base properties
        self.frame = Toplevel(master)
        self.frame.grab_set()
        self.frame.wm_title("Scraper Input")
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
        self.filename = StringVar(value="")
        self.filenameNum = BooleanVar(value=FALSE)
        self.fileFormat = StringVar(value="jpg")

        # populate the window
        self.create_form()

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
        Checkbutton(self.frame, text="Multiple Pages", variable=self.multPages, state="disable")\
            .grid(row=9, column=1, columnspan=3)

        # saving-related fields
        Label(self.frame, text="Page Title\nSelector").grid(row=1, column=5)
        Radiobutton(self.frame, text="class(.)", variable=self.titleLocID, value=".", tristatevalue="x").grid(row=1, column=6)
        Radiobutton(self.frame, text="id(#)", variable=self.titleLocID, value="#", tristatevalue="x").grid(row=1, column=7)
        Radiobutton(self.frame, text="other", variable=self.titleLocID, value="", tristatevalue="x").grid(row=1, column=8)
        Entry(self.frame, textvariable=self.titleLoc).grid(row=2, column=6, columnspan=3)

        Label(self.frame, text="Filename").grid(row=3, column=5)
        Checkbutton(self.frame, text="#", variable=self.filenameNum).grid(row=3, column=6)
        Entry(self.frame, textvariable=self.filename).grid(row=3, column=7, columnspan=2)

        Label(self.frame, text="File Format").grid(row=4, column=5)
        Radiobutton(self.frame, text=".jpg", variable=self.fileFormat, value="jpg").grid(row=4, column=6)
        Radiobutton(self.frame, text=".png", variable=self.fileFormat, value="png").grid(row=4, column=7)

        #TODO: save destination

        # set global padding for above items
        for child in self.frame.winfo_children():
            child.grid_configure(padx=8, pady=2, sticky="we")

        # other fields and elements
        title = Label(self.frame, text="Scraper Input", font=('Cooper Black', 24))
        title.grid(row=0, columnspan=9, padx=10, pady=10, sticky="we")
        ttk.Separator(self.frame, orient=VERTICAL).grid(row=1, column=4, rowspan=9, sticky="ns")
        cancel = Button(self.frame, text="Cancel", command=self.frame.destroy)
        cancel.grid(row=10,column=5, padx=10, pady=10, sticky="we")
        scrape = Button(self.frame, text="Scrape", command=self.start_scrape)
        scrape.grid(row=10, column=3, padx=10, pady=10, sticky="we")

    def start_scrape(self):
        args = []  #starturl, imgsel, imgpref, titlesel, comicname, addnum, fileform, nextsel, nextpref
        args.append(self.startURL.get())
        #args.append(self.endURL.get())
        args.append(self.contentID.get() + self.content.get())
        args.append("") if not self.contentPreB else args.append(self.contentPre.get())
        args.append(self.titleLocID.get() + self.titleLoc.get())
        args.append(self.filename.get())
        args.append(True) if self.filenameNum.get() else args.append(False)
        args.append(self.fileFormat.get())
        args.append(self.nextPageID.get() + self.nextPage.get())
        args.append("") if not self.nextPagePreB else args.append(self.nextPagePre.get())

        # Try to scrape, and provide feedback
        try:
            scrape_all(*args)
            feedback = "Scrape Successful"
            cf = self.frame
        except Exception as e:
            feedback = "Scrape Failed:\n%s" % e
            cf = None
        Dialog(self.frame, feedback, dFrame=cf, title="Scrape Results", btnTxt="Close")

class ScrapeSettings:
    def __init__(self):
        self.startnum = 0
        self.endnum = 0
        self.starturl = ""
        self.imagesel = ""
        self.imagepref = ""
        self.titlesel = ""
        self.comicname = ""
        self.addnum = False
        self.fileform = ""
        self.nextsel = ""
        self.nextpref = ""

    def setRange(self, start, stop):
        self.startnum = start
        self.endnum = stop
    def setImage(self, selector, prefix):
        self.imagesel = selector
        self.imagepref = prefix
    def setTitle(self, selector):
        self.titleSel = selector
    def setFile(self, filenameprefix, addnum, format):
        self.comicname = filenameprefix
        self.addnum = addnum
        self.fileform = format
    def setNext(self, selector, prefix):
        self.nextsel = selector
        self.nextpref = prefix

""" Test function that can be used to specifically scrape xkcd.com """
def scrape_xkcd(start, stop):
    for x in range(start,stop):
        # get the website
        url = "http://xkcd.com"
        res = requests.get(url + "/" + str(x) + "/")
        res.raise_for_status()

        # create beautiful soup object and extract image url and name
        pageSoup = bs4.BeautifulSoup(res.text, "html.parser")
        imgElem = pageSoup.select('#comic img')[0]
        imgUrl = "http:" + imgElem.get('src')
        title = imgElem.get('title')

        #scrape the image
        res2 = requests.get(imgUrl)
        res2.raise_for_status()

        # write img to file
        print("Writing comic #%d" % x)
        for char in "\/?:*<>\"|":
            title = title.replace(char, "_")
        file = open("%sxkcd #%d - %s.jpg" % (DEFAULTLOC, x, title), 'wb')
        for chunk in res2.iter_content(100000):
            file.write(chunk)
        file.close()

""" Function capable of scraping a range of pages from any website of url format http://<website url>/<comic number>
    Accepts:
        start page number
        stop page number
        url of the website
        CSS selector for the comic image
        any prefixes that need to be added to the img url
        CSS selector for comic title
        desired name of comic for the file
        whether or not to add the comic page number # TODO: this should be an optional field, and set to true by default
        desired file format
"""
def scrape_range(start, stop, starturl, imgsel, imgpref, titlesel, comicname, addnum, fileform):
    for x in range(start, stop+1):
        # get the website and create soup
        print("Getting %s #%d" % (comicname, x))
        res = requests.get(starturl + str(x))
        res.raise_for_status()
        pageSoup = bs4.BeautifulSoup(res.text, "html.parser")

        # extract image url and name
        imgElem = pageSoup.select(imgsel)[0]
        imgUrl = imgpref + imgElem.get('src')
        title = imgElem.get(titlesel)

        # scrape the image
        res2 = requests.get(imgUrl)
        res2.raise_for_status()

        # write img to file
        for char in "\/?:*<>\"|":
            title = title.replace(char, "_")
        if addnum:
            file = open("%s%s #%d - %s.%s" % (DEFAULTLOC, comicname, x, title, fileform), 'wb')
        else:
            file = open("%s%s - %s.%s" % (DEFAULTLOC, comicname, title, fileform), 'wb')
        for chunk in res2.iter_content(100000):
            file.write(chunk)
        file.close()

""" Function that takes first page of comic, and scrapes until next page url == current url, and saves all
    Accepts:
        url of the first page (or starting page)
        CSS selector for the comic image
        any prefixes that need to be added to the img url
        CSS selector for comic title
        desired name of comic for the file
        whether or not to add the comic page number # TODO: this should be an optional field, and set to true by default
        desired file format
        CSS selector for the next page url
        any prefixes that need to be added to the next page url
"""
def scrape_all(starturl, imgsel, imgpref, titlesel, comicname, addnum, fileform, nextsel, nextpref):
    x = 1
    cururl = starturl
    while True:
        # get the website and create soup
        print("Getting %s #%d" % (comicname, x))
        res = requests.get(cururl)
        res.raise_for_status()
        pageSoup = bs4.BeautifulSoup(res.text, "html.parser")

        # extract image url and name
        imgElem = pageSoup.select(imgsel)[0]
        imgUrl = imgpref + imgElem.get('src')
        title = imgElem.get(titlesel)

        # scrape the image
        res2 = requests.get(imgUrl)
        res2.raise_for_status()

        # write img to file
        for char in "\/?:*<>\"|":
            title = title.replace(char, "_")
        if addnum:
            file = open("%s%s #%d - %s.%s" % (DEFAULTLOC, comicname, x, title, fileform), 'wb')
        else:
            file = open("%s%s - %s.%s" % (DEFAULTLOC, comicname, title, fileform), 'wb')
        for chunk in res2.iter_content(100000):
            file.write(chunk)
        file.close()

        # get next page and set cururl
        if not pageSoup.select(nextsel):
            break
        nexturl = nextpref + pageSoup.select(nextsel)[0].get("href")
        if nexturl == cururl:
            break
        cururl = nexturl
        x = x + 1

"""Tests for above functions"""
if __name__ == "__main__":
    #scrape_xkcd()

    #Testing for gen_scrape
    #xkcd = [1, 5, "http://xkcd.com/", "#comic img", "http:", "title", "xkcd", True, "jpg"]
    #lyoko = [1, 5, "http://codegamenight.thecomicseries.com/comics/", "#comicimage", "", "alt", "Code Game Night", False, "png"]
    #gems = [1, 5, "http://crystalgms.thecomicseries.com/comics/", "#comicimage", "", "alt", "Crystal GMs", True, "jpg"]
    #scrape_range(*xkcd)
    #scrape_range(*lyoko)
    #scrape_range(*gems)

    #Testing for scrape_all
    #scrape_all("http://codegamenight.thecomicseries.com/comics/first/", "#comicimage", "", "alt", "Code Game Night", False, "png", 'a[rel="next"]', "http://codegamenight.thecomicseries.com")
    #scrape_all("http://www.misfile.com/?date=2017-08-05", ".comic img", "http://www.misfile.com/", "alt", "Misfile", True, "jpg", ".comic a", "")

    #update currently managed ones
    scrape_all("http://codegamenight.thecomicseries.com/comics/278/", "#comicimage", "", "alt", "Code Game Night", False, "png", 'a[rel="next"]', "http://codegamenight.thecomicseries.com")