import requests, bs4

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
    for char in "\/?:*<>\"|":
        title = title.replace(char, "_")

    #scrape the image
    res2 = requests.get(imgUrl)
    res2.raise_for_status()

    # write img to file
    print("Writing comic #%d" % x)
    file = open("./img/xkcd #%d - %s.jpg" % (x, title), 'wb')
    for chunk in res2.iter_content(100000):
        file.write(chunk)
    file.close()
