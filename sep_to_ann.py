# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:50:05 2015

@author: Celeste
"""

import os
import pred as pred
from recipe import *

reload(pred)

rootdir = "..\AllRecipesData\chunked"
recipeList =[]

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

for item in recipeList:
    print item, item.probability()


