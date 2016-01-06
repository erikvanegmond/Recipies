# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:50:05 2015

@author: Celeste
"""

import os
# import pred as pred
# import recipe as re
from recipe import *
import pickle

rootdir = "..\AllRecipesData\chunked"
recipeList = []
fixedPath = "..\\AllRecipesData\\chunked\\BeefMeatLoaf-chunked\\amish-meatloaf.txt"
recipeList.append(Recipe(fixedPath))
c = 0
cmax = 20
for subdir, dirs, files in os.walk(rootdir):
    for current_file in files:
        if current_file == ".DS_Store":
            continue
        else:
            # if "amish-meatloaf" in file:s
            if "\AllRecipesData\chunked" in subdir:
                path = os.path.join(subdir, current_file)
                print path
                recipeList.append(Recipe(path))
                c += 1
                print c
                if c > cmax:
                    break
    if c > cmax:
        break

'''
global_verb_count = {}
global_verb_type = {}
global_verb_sig_count = {}
global_connection_count = {}
c = 0
for item in recipeList:
    print c
    c += 1
    (verb_count, verb_type) = item.verbCounter()
    (_, verb_sig_count) = item.getCountVerbSignature()

    for vc in verb_count:
        if vc not in global_verb_count:
            global_verb_count[vc] = verb_count[vc]
        else:
            global_verb_count[vc] += verb_count[vc]
    for vc in verb_type:
        if vc not in global_verb_type:
            global_verb_type[vc] = verb_type[vc]
        else:
            global_verb_type[vc] += verb_type[vc]
    for vs in verb_sig_count:
        if vs not in global_verb_sig_count:
            global_verb_sig_count[vs] = verb_sig_count[vs]
        else:
            global_verb_sig_count[vs] += verb_sig_count[vs]


for key in global_verb_sig_count:
    global_verb_sig_count[key] += 0.1
    print global_verb_sig_count[key]

# for key in global_origin_connection_count:
#    global_origin_connection_count[key] += 0.1



# recipeList[0].makeConnections(global_verb_count, global_verb_type)
# pprint(recipeList[0].graph)
for item in recipeList:
    # print item
    # item.makeConnections(global_verb_count, global_verb_type)
    # # pprint( item.graph )
    # print
    item.makeConnections(global_verb_count, global_verb_type)
    connection_count = item.connection_counter()

    for cc in connection_count:
        if cc not in global_connection_count:
            global_connection_count[cc] = connection_count[cc]
        else:
            global_connection_count[cc] += connection_count[cc]

output = open('globals.pkl', 'wb')
pickle.dump(global_verb_count, output)
pickle.dump(global_verb_type, output)
pickle.dump(global_verb_sig_count, output)
pickle.dump(global_connection_count, output)
output.close()
'''

pkl_file = open('globals.pkl', 'r')
global_verb_count = pickle.load(pkl_file)
global_verb_type = pickle.load(pkl_file)
global_verb_sig_count = pickle.load(pkl_file)
global_connection_count = pickle.load(pkl_file)

for item in recipeList:
    item.makeConnections(global_verb_count, global_verb_type)
    item.evaluateGraph(global_verb_sig_count, global_connection_count)
    print item.graph