import requests, bs4

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
        file = open("./img/xkcd #%d - %s.jpg" % (x, title), 'wb')
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
            file = open("./img/%s #%d - %s.%s" % (comicname, x, title, fileform), 'wb')
        else:
            file = open("./img/%s - %s.%s" % (comicname, title, fileform), 'wb')
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
            file = open("./img/%s #%d - %s.%s" % (comicname, x, title, fileform), 'wb')
        else:
            file = open("./img/%s - %s.%s" % (comicname, title, fileform), 'wb')
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
    scrape_xkcd()

    #Testing for gen_scrape
    xkcd = [1, 5, "http://xkcd.com/", "#comic img", "http:", "title", "xkcd", True, "jpg"]
    lyoko = [1, 5, "http://codegamenight.thecomicseries.com/comics/", "#comicimage", "", "alt", "Code Game Night", False, "png"]
    gems = [1, 5, "http://crystalgms.thecomicseries.com/comics/", "#comicimage", "", "alt", "Crystal GMs", True, "jpg"]
    scrape_range(*xkcd)
    scrape_range(*lyoko)
    scrape_range(*gems)

    #Testing for scrape_all
    scrape_all("http://codegamenight.thecomicseries.com/comics/first/", "#comicimage", "", "alt", "Code Game Night", False, "png", 'a[rel="next"]', "http://codegamenight.thecomicseries.com")
    scrape_all("http://www.misfile.com/?date=2017-08-05", ".comic img", "http://www.misfile.com/", "alt", "Misfile", True, "jpg", ".comic a", "")