import os, copy

netIDs = []
index = 0
for path, subdirs, files in os.walk("./collected/"):
    if subdirs and not netIDs:
        print(subdirs)
        netIDs = copy.deepcopy(subdirs)
    elif index > 6:
        # generate output file
        outline = "NetID: " + netIDs[index] + "\n==========\n"
        outline += "C program: 1/1\nC screenshot: 1/1\n"
        outline += "Javascript program: 1/1\nJavascript screenshot: 1/1\n"
        outline += "Python program: 1/1\nPython screenshot: 1/1\n"
        outline += "Prolog program: 1/1\nProlog screenshot: 1/1\n"
        outline += "SML program: 1/1\nSML screenshot: 1/1\n"
        outline += "==========\nTotal Points: 10/10\n"

        # bookkeeping and create file
        index += 1
        f = open(path + "/output.txt", "w")
        f.write(outline)
        f.close()
    else:
        index += 1
