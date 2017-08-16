import requests, bs4

def scrape_xkcd():
    for x in range(32,35):
        # get the website
        url = "http://xkcd.com"
        res = requests.get(url + "/" + str(x) + "/")
        res.raise_for_status()

        # create beautiful soup object and extract image url and name
        pageSoup = bs4.BeautifulSoup(res.text, "html.parser")
        imgElem = pageSoup.select('#comic img')[0]
        #print(imgElem.attrs)
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

def gen_scrape(start, stop, starturl, imgsel, titlesel, comicname, addnum, fileform):
    for x in range(start, stop+1):
        # get the website
        res = requests.get(starturl + str(x))
        res.raise_for_status()

        # create beautiful soup object and extract image url and name
        pageSoup = bs4.BeautifulSoup(res.text, "html.parser")
        imgElem = pageSoup.select(imgsel)[0]
        imgUrl = imgElem.get('src')
        if imgUrl.find("http:") == -1:
            imgUrl = "http:" + imgUrl
        title = imgElem.get(titlesel)

        # scrape the image
        res2 = requests.get(imgUrl)
        res2.raise_for_status()

        # write img to file
        print("Writing %s #%d" % (comicname, x))
        for char in "\/?:*<>\"|":
            title = title.replace(char, "_")
        if addnum:
            file = open("./img/%s #%d - %s.%s" % (comicname, x, title, fileform), 'wb')
        else:
            file = open("./img/%s - %s.%s" % (comicname, title, fileform), 'wb')
        for chunk in res2.iter_content(100000):
            file.write(chunk)
        file.close()

gen_scrape(1, 5, "http://xkcd.com/", "#comic img", "title", "xkcd", True, "jpg")
gen_scrape(1, 5, "http://codegamenight.thecomicseries.com/comics/", "#comicimage", "alt", "Code Game Night", False, "png")
gen_scrape(1, 5, "http://crystalgms.thecomicseries.com/comics/", "#comicimage", "alt", "Crystal GMs", True, "jpg")

