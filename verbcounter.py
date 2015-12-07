# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 12:53:50 2015

@author: Celeste
"""
import os

count_list = [['e1',  'preheat',  [['the oven', 'location', 'explicit'],   ['350 degrees f -lrb- 175 degrees c -rrb-', '?']],  '?'], ['e2',  'mix',  [['ground beef ', 'food', 'explicit'],   ['crushed crackers ', 'food', 'explicit'],   ['a medium bowl', 'food', 'explicit'],   ['well blended', '?'],   ['together', '?']],  '?'], ['e3', 'press', [['a 9x5 inch loaf pan', 'food', 'explicit']], '?'], ['e4',  'lay',  [['the two slices of bacon', 'food', 'explicit'], ['the top', '?']],  '?'], ['e5',  'bake',  [['1 hour', '?'], ['the preheated oven', 'location', 'explicit']],  '?'], ['e6',  'mix',  [['the remaining 1 cup ketchup ', 'food', 'explicit'],   ['vinegar ', 'food', 'explicit'],   ['the loaf bakes', 'food', 'explicit'],   ['together', '?']],  '?'], ['e7',  'spread',  [['the top of the meat loaf', 'food', 'explicit'],   ['the last 15 minutes of baking', '?']],  '?']]
verb_list = []
for i in range(0,len(count_list)):
    #this if statement ensures that there will not be duplicate verbs in verb_list
    if count_list[i][1] not in verb_list:
        verb_list.append(count_list[i][1])
    #otherwise it will continue the for-loop
    else:
        continue
print count_list[0][2][0][1]
#verb_type_counter(count_list, verb_list)

   
#def verb_type_counter(all_recipes_in_lists, verb_list):
verb_count = {}
verb_type = {}
for j in range(0,len(verb_list)):
    verb_count[verb_list[j] + "-0"] = 0
    verb_count[verb_list[j] + "-1"] = 0
    verb_count[verb_list[j] + "-2"] = 0
    verb_type[verb_list[j] + "-1-location"] = 0
    verb_type[verb_list[j] + "-1-food"] = 0
    verb_type[verb_list[j] + "-2-food"] = 0
    verb_type[verb_list[j] + "-2-location"] = 0
    verb_type[verb_list[j] + "-2-food-location"] = 0
for k in range(0,len(count_list)):
    if len(count_list[k][2]) == 0:
        verb_count[count_list[k][1] + "-0"] = verb_count[count_list[k][1] + "-0"] + 1
    if len(count_list[k][2]) == 1:
        verb_count[count_list[k][1] + "-1"] = verb_count[count_list[k][1] + "-1"] + 1
        if count_list[k][2][0][1] == 'location':
            verb_type[count_list[k][1] + "-1-location"] = verb_type[count_list[k][1] + "-1-location"] + 1
        if count_list[k][2][0][1] == 'food':
            verb_type[count_list[k][1] + "-1-food"] = verb_type[count_list[k][1] + "-1-food"] + 1
        else:
            continue
    if len(count_list[k][2]) > 1:
        print count_list[k][1]
        location = 0;
        food = 0;
        verb_count[count_list[k][1] + "-2"] = verb_count[count_list[k][1] + "-2"] + 1
        for l in range(0,len(count_list[k][2])):
            if count_list[k][2][l][1] == 'location':
                location = location + 1
            if count_list[k][2][l][1] == 'food':
                food = food + 1
            else:
                continue
        print "location:"
        print location
        print "food:"
        print food
        if location >= 1 and food >= 1:
            verb_type[count_list[k][1] + "-2-food-location"] = verb_type[count_list[k][1] + "-2-food-location"] + 1
            print(count_list[k][1] + "-2-food-location")
        if location >= 2 and food == 0:
            verb_type[count_list[k][1] + "-2-location"] = verb_type[count_list[k][1] + "-2-location"] + 1
            print(count_list[k][1] + "-2-location")
        if location == 0 and food >= 2:
            verb_type[count_list[k][1] + "-2-food"] = verb_type[count_list[k][1] + "-2-food"] + 1
            print(count_list[k][1] + "-2-food")
        else:
            continue
        
            
        
print verb_count
print verb_type
# make 2 dictionaries of verbs. 3 dict items per verb
# count number of arguments per verb
# for each number of arguments, put in types



#verb-argument-count
#{mix-0: 1, mix-1: 2, mix-2: 50, press-0, ...}
#for each verb, 3 entries: 
#verb-0, no arguments
#verb-1, 1 argument
#verb-2, more than 1 argument

#verb-argument-kind-count
#{mix-1-location: 1, mix-1-food: 2, mix-2-food: 20, mix-2-location: 0, mix-2-food-location:10,...}
