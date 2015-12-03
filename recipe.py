import pickle
import pred as pred
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.util import ngrams
from pprint import *



class Recipe(object):
    """docstring for Recipe"""

    foods = None
    cookware = None

    def __init__(self, filepath):
        self.filepath = filepath
        print self.foods
        pkl_file = open('foods.pkl', 'rb')
        self.foods = pickle.load(pkl_file)
        pkl_file = open('cookware.pkl', 'rb')
        self.cookware = pickle.load(pkl_file)
        self.stemmer = SnowballStemmer("english")
        self.maxNgrams = 5

        self.graph = self.makeGraph()
        # print pprint(self.graph)

    def probability(self):
        return 1

    def makeGraph(self):
        new_file = open(self.filepath, 'r')
        all_list = pred.parse_predicate(new_file.read())
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

    def __str__(self):
        return "a recipe based on "+self.filepath


amishMeatloaf = Recipe("..\\AllRecipesData\\chunked\\BeefMeatLoaf-chunked\\amish-meatloaf.txt")
# print amishMeatloaf