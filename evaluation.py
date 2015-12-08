# -*- coding: utf-8 -*-
"""
Created on Tue Dec 08 16:06:12 2015

@author: Celeste
"""

import numpy as np

#P(C) =prod{i} P(gi,vi) prod{i} prod{cp in di} P(o(cp)|d1...di1,c1...cp1,gi)
# verbsignature: DOBJ,PP,both and Origin = 0 or not
#P(R|C) = prod{i} P(vi|gi) prod{skij in Sij} funcsem(o,(part)ij) P(skij|syn,sem,C,hi)
#When the argument is a food, and o != 0 : prod{k} P(skij|food(skij,C)) P(implicit|d(i,o))
#When the argument is a food, and o = 0 : prod{l} (wl|rsw)
#When the argument is a location : explicit :(loc(i),loc(o))   implicit :P(loc(o)|vi)

prior_c = np.prod([2,3,4])