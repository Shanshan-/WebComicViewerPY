"""
Functions used to put a series of strings in natural order
"""
import re

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [
        c if c in "~!@#$%^&*()`-_=+[]\{}|;':\"<>?,./\\+"
        else int(c) if c.isdigit()
        else c.lower() for c in re.split('([0-9]+)', s)
    ]


def sort_natural(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

filenames = list()

""" Taking in strings from user input
filenames.append(input("Enter filename 1: "))
filenames.append(input("Enter filename 2: "))
filenames.append(input("Enter filename 3: "))
filenames.append(input("Enter filename 4: "))
filenames.append(input("Enter filename 5: "))"""

""" Taking in strings from a file """
f = open("./test-filenames.txt")
for line in f:
    filenames.append(line.strip())

print("Original:", filenames)
sort_natural(filenames)
print("---------------")
print("Natural: ", filenames)
filenames.sort()
print("---------------")
print("Default: ", filenames)
