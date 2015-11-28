# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:50:05 2015

@author: Celeste
"""

import os
import pred as pred

reload(pred)

rootdir = "C:\Users\Celeste\Documents\Masters\AllRecipesData"

seg = 0
ann = 0
full = 0
size = 99999999
smallest = ""
for subdir, dirs, files in os.walk(rootdir):
    print subdir
    for file in files:
        if file == ".DS_Store":
            continue
        else:
            if "\AllRecipesData\chunked" in subdir:
                path = "\AllRecipesData\chunked"
                path2 = rootdir + "/DevSet-annotations/"
                filename = os.path.splitext(file)[0]
                new_file = open(path2 + filename + '.ann', 'w')
                path = os.path.join(subdir, file)
                f = open(path,'r')
                (all_list, input_string) = pred.parse_predicate(f.read())
                print input_string
                print all_list
                break
                #new_file.write( + '\n')

print "seg: %d, ann %d, full %d" %(seg, ann, full)
        # print os.path.join(subdir, file)
print smallest