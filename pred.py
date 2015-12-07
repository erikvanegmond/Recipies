# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 16:37:31 2015

@author: Celeste
"""

def parse_predicate(input_string):
    """ Example strings:
        SENTID: 0
            SENT: Preheat oven to 350 degrees F -LRB- 175 degrees C -RRB- .
            PREDID: 0
            PRED: preheat
              DOBJ: oven
              PARG: 350 degrees f -lrb- 175 degrees c -rrb-
                PREP: to

    """
    import re

    all_list = []
    verb_list = []
    arguments_list = []
    predicate = []
    dobj = []
    parg = []
    oarg = []

    input_string = input_string.split('\n')
    for i in range (0,len(input_string)):
        if 'PRED:' in input_string[i]:
            pargs_per_verb = []
            oargs_per_verb = []
            dobjs_per_verb = ''
            predicate.append(input_string[i].split(': ')[1])
        elif 'DOBJ' in input_string[i]:
            dobjs_splitted = re.split('DOBJ: |, ', input_string[i])
            if dobjs_splitted[0] == '  ':
                dobjs_per_verb = dobjs_splitted[1:]
            else:
                dobjs_per_verb = dobjs_splitted
        elif 'PARG' in input_string[i]:
            pargs_per_verb.append(input_string[i].split(': ')[1])
        elif 'OARG' in input_string[i]:
            oargs_per_verb.append(input_string[i].split(': ')[1])
        elif i == (len(input_string)-1):
            dobj.append(dobjs_per_verb)
            parg.append(pargs_per_verb)
            oarg.append(oargs_per_verb)
        elif 'PREDID' in input_string[i]:
            if i == 2:
                continue
            else:
                dobj.append(dobjs_per_verb)
                parg.append(pargs_per_verb)
                oarg.append(oargs_per_verb)

        else:
            continue

    for j in range (0,len(predicate)):
        arguments_list = [dobj[j],parg[j],oarg[j]]
        verb_list.append(predicate[j])
        tuple_pred = (predicate[j],arguments_list)
        all_list.append(tuple_pred)
    return (all_list, list(set(verb_list)))



    #return {....}