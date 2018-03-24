import os
from PIL import Image
from nat_sorter import sort_natural

class entry:
    def __init__(self, ppath, name, chapter, page):
        self.path = ppath
        self.name = name
        self.chapter = chapter
        self.page = page
        self.index = str(chapter) + "." + str(page)

def loadFiles(cmcpath):
    filenames = dict()
    cnum = 0
    pnum = 1
    for path, subdirs, files in os.walk(cmcpath):
        sort_natural(subdirs)
        if not subdirs:
            cnum += 1
            sort_natural(files)
            for file in files:
                curpath = path + "/" + file
                tmp = entry(curpath, file, cnum, pnum)
                filenames[tmp.index] = tmp
                pnum += 1
            pnum = 1
        #TODO: find a way to filter out unwanted folders and files
        #TODO: account for pages with folders
    return filenames

if __name__ == "__main__":
    path = "./img"
    #path = "D:\Webcomics\The Seven Deadly Sins"
    cmcfiles = loadFiles(path)
    for key, value in cmcfiles.items():
        print(str(value.index) + ", " + value.name)

    Image.open(cmcfiles["1.1"].path).show()