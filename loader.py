import os
from nat_sorter import sort_natural

class entry:
    def __init__(self, ppath, name, chapter, page):
        self.path = ppath
        self.name = name
        self.chapter = chapter
        self.page = page
        self.index = str(chapter) + "." + str(page)

cmcpath = "./img"
filenames = dict()
nested = False
cnum = 0
pnum = 1
for path, subdirs, files in os.walk(cmcpath):
    #case 1: files are all in single folder (aka no subdirs)
    if not subdirs:
        cnum += 1
        sort_natural(files)
        for file in files:
            curpath = path + "/" + file
            tmp = entry(curpath, file, cnum, pnum)
            filenames[tmp.index] = tmp
            pnum += 1
        pnum = 1

    #case 2: files are all divided by chapters (only subdirs)
    elif not files:
        nested = True

    #case 3: hybrid of two

for key in filenames:
    print(str(filenames[key].index) + ", " + filenames[key].name)