"""
Sandbox functions used to put a series of strings in natural order
"""
import re
from natsort import natsorted, humansorted, ns

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [
        int(c) if c.isdigit()
        else c.lower() for c in re.split('([0-9]+)', s)
    ]


def sort_natural(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

def test():
    filenames = list()
    f = open("./test-filenames.txt")
    for line in f:
        filenames.append(line.strip())

    print("Original:", filenames)
    print("---------------")
    filenames.sort()
    print("Default: ", filenames)
    print("---------------")
    sort_natural(filenames)
    print("Natural: ", filenames)
    print("---------------")
    natsorted(filenames, alg=ns.IGNORECASE)
    print("NatSort: ", filenames)
