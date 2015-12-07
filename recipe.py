import pickle
import pred as pred
import pprint
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.util import ngrams
from pprint import *



class Recipe(object):
    """docstring for Recipe"""

    foods = None
    cookware = None

    def __init__(self, filepath):
        print "starting the recipe"
        self.filepath = filepath
        print self.foods
        pkl_file = open('foods.pkl', 'r')
        self.foods = pickle.load(pkl_file)
        pkl_file = open('cookware.pkl', 'r')
        self.cookware = pickle.load(pkl_file)
        self.stemmer = SnowballStemmer("english")
        self.maxNgrams = 5

        self.graph = self.makeGraph()
        # print pprint(self.graph)

    def probability(self):
        return 1

    def makeGraph(self):
        new_file = open(self.filepath, 'r')
        (all_list, self.verb_list) = pred.parse_predicate(new_file.read())
        counter = 1
        graphObject = []
        for item in all_list:
            actionName = "e"+str(counter)
            # print actionName,
            action = item[0]
            # print action,
            objectList = []
            for cookingObject in item[1]:
                if type(cookingObject) is list:
                    for object in cookingObject[:2]:
                        if self.isFood(object):
                            # print object
                            objectList.append([object, "food", "explicit"])
                        elif self.isCookware(object):
                            objectList.append([object, "location", "explicit"])
                        else:
                            objectList.append([object, "?"])
            actionResult = "?"
            actionList = [actionName, action, objectList, actionResult]
            graphObject.append(actionList)
            counter += 1

        return graphObject
        
    def makeConnections(self):
        

    def isFood(self, string):
        return self.isType(string, "food")

    def isCookware(self, string):
        return self.isType(string, "cookware")

    def isType(self, string, type):
        found = False
        string = string.decode('ascii', 'ignore')
        if type == "food":
            itemList = self.foods
        elif type == "cookware":
            itemList = self.cookware

        text = word_tokenize(string)
        for n in reversed(range(1, self.maxNgrams+1)):
            for gram in ngrams(text, n):
                potentialFood = " ".join(gram)
                if len(potentialFood) > 1:
                    if potentialFood in itemList:
                        # print potentialFood,
                        found = True
                        continue
                    if n == 1:
                        potentialFood = self.stemmer.stem(potentialFood)
                        if potentialFood in itemList:
                            found = True
                            # print "stemmed",
                            continue
            if found:
                # print potentialFood, type
                return True
        return False
        
    def verbCounter(self):
        verb_count = {}
        verb_type = {}
        count_list = self.graph
        for verb in self.verb_list:
            verb_count[verb + "-0"] = 0
            verb_count[verb + "-1"] = 0
            verb_count[verb + "-2"] = 0
            verb_type[verb + "-1-location"] = 0
            verb_type[verb + "-1-food"] = 0
            verb_type[verb + "-2-food"] = 0
            verb_type[verb + "-2-location"] = 0
            verb_type[verb + "-2-food-location"] = 0    
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
                if location >= 1 and food >= 1:
                    verb_type[count_list[k][1] + "-2-food-location"] = verb_type[count_list[k][1] + "-2-food-location"] + 1
                if location >= 2 and food == 0:
                    verb_type[count_list[k][1] + "-2-location"] = verb_type[count_list[k][1] + "-2-location"] + 1
                if location == 0 and food >= 2:
                    verb_type[count_list[k][1] + "-2-food"] = verb_type[count_list[k][1] + "-2-food"] + 1
                else:
                    continue
        
        return  (verb_count, verb_type)

    def __str__(self):
        return "a recipe based on "+self.filepath


amishMeatloaf = Recipe("..\\AllRecipesData\\chunked\\BeefMeatLoaf-chunked\\amish-meatloaf.txt")
pprint(amishMeatloaf.graph)
amishMeatloaf.verbCounter()
# print amishMeatloaf