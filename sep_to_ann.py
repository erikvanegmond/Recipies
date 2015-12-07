# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:50:05 2015

@author: Celeste
"""

import os
#import pred as pred
#import recipe as re
from recipe import *
import pickle

rootdir = "..\AllRecipesData\chunked"
recipeList =[]
fixedPath = "..\\AllRecipesData\\chunked\\BeefMeatLoaf-chunked\\amish-meatloaf.txt"
recipeList.append(Recipe(fixedPath))
c = 0
cmax = 20
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == ".DS_Store":
            continue
        else:
            # if "amish-meatloaf" in file:
            if "\AllRecipesData\chunked" in subdir:
                path = os.path.join(subdir, file)
                print path
                recipeList.append(Recipe(path))
                c+=1
                print c
                if c > cmax:
                    break
    if c > cmax:
        break


# output = open('globals.pkl', 'wb')

# global_verb_count = {}
# global_verb_type = {}
# for item in recipeList:
#     (verb_count, verb_type) = item.verbCounter()
#     for vc in verb_count:
#         if not vc in global_verb_count:
#             global_verb_count[vc] = verb_count[vc]
#         else:
#             global_verb_count[vc] += verb_count[vc]
#     for vc in verb_type:
#         if not vc in global_verb_type:
#             global_verb_type[vc] = verb_type[vc]
#         else:
#             global_verb_type[vc] += verb_type[vc]
# pickle.dump(global_verb_count, output)
# pickle.dump(global_verb_type, output)
# output.close()

pkl_file = open('globals.pkl', 'r')
global_verb_count = pickle.load(pkl_file)
global_verb_type = pickle.load(pkl_file)

for item in recipeList:
    item.makeConnections(global_verb_count,global_verb_type)
    pprint( item.graph )
# print item, item.probability()


