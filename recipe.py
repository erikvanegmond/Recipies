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
    stemmer = None

    def __init__(self, filepath):
        self.filepath = filepath
        if not Recipe.foods:
            pkl_file = open('foods.pkl', 'r')
            Recipe.foods = set(pickle.load(pkl_file))
            print "loaded Foods"
        if not Recipe.cookware:
            pkl_file = open('cookware.pkl', 'r')
            Recipe.cookware = set(pickle.load(pkl_file))
            print "loaded cookware"
        if not Recipe.stemmer:
            Recipe.stemmer = SnowballStemmer("english")
            print "loaded stemmer"
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
        recipeIngredients = self.getIngredients()
        for item in all_list:
            actionName = "e"+str(counter)
            # print actionName,
            action = item[0]
            # print action,
            objectList = []
            for cookingObject in item[1]:
                if type(cookingObject) is list:
                    for object in cookingObject[:2]:
                        food = self.isFood(object)
                        if food and food in recipeIngredients:
                            objectList.append([object, "food", "explicit"])
                        elif self.isCookware(object):
                            objectList.append([object, "location", "explicit"])
                        else:
                            objectList.append([object, "?"])

            actionResult = self.determineActionResult(objectList)
            actionList = [actionName, action, objectList, actionResult]
            graphObject.append(actionList)
            counter += 1

        return graphObject

    def determineActionResult(self, arguments):
        (foodCount, locationCount) =  self.argumentTypes(arguments)
        if foodCount:
            actionResult = "food"
        elif locationCount:
            actionResult = "location"
        else:
            actionResult = "?"
        return actionResult

    def getIngredients(self):
        path = self.filepath.replace('chunked','fulltext')
        with open(path, 'r'  ) as f:
            recipe = f.read().replace("\n\n","\n").split("\n")
        ingredients = []
        ingBool = False
        for line in recipe:
            if line.startswith("Data Parsed"):
                ingBool = False
            food = self.isFood(line)
            if ingBool and line and food:
                ingredients.append(food)

            if line == "Ingredients":
                ingBool = True
        return ingredients

    def makeConnections(self, global_verb_count, global_verb_type):
        chosenConnections = set()
        for i, action in enumerate(self.graph):
            if i:
                (foodCount, locationCount) = self.argumentTypes(action[2])
                if locationCount:
                    for arg in action[2]:
                        if arg[1] == "location":
                            actionID = self.findPreviousMentionOfLocation(arg[0], i, chosenConnections)
                            if actionID:
                                chosenConnections.add(actionID)
                                arg.append(actionID)

                verb = action[1]
                argument = self.mostPobableArguments(verb, global_verb_count, global_verb_type)

                if argument == "-1-location":
                    if foodCount == 0 and locationCount == 1:
                        pass
                    else:
                        actionID = self.findPossibleConnection(i, "location", chosenConnections)
                        chosenConnections.add(actionID)
                        action[2].append(["?", "location", "impicit", actionID])

                elif argument == "-1-food":
                    if foodCount == 1 and locationCount == 0:
                        pass
                    else:
                        actionID = self.findPossibleConnection(i, "food", chosenConnections)
                        chosenConnections.add(actionID)
                        action[2].append(["?", "food", "impicit", actionID])
                elif argument == "-2-food":
                    if foodCount >= 2 and locationCount == 0:
                        pass
                    else:
                        for j in range(2-foodCount):
                            actionID = self.findPossibleConnection(i, "food", chosenConnections)
                            chosenConnections.add(actionID)
                            action[2].append(["?", "food", "impicit", actionID])
                elif argument == "-2-location":
                    if foodCount == 0 and locationCount >= 2:
                        pass
                    else:
                        for i in range(2-locationCount):
                            actionID = self.findPossibleConnection(i, "location", chosenConnections)
                            chosenConnections.add(actionID)
                            action[2].append(["?", "location", "impicit", actionID])
                elif argument == "-2-food-location":
                    if (foodCount >=2 and locationCount == 0) or (foodCount == 0 and locationCount >= 2) or (foodCount == 1 and locationCount == 1):
                        pass
                    else:
                        if foodCount == 0:
                            actionID = self.findPossibleConnection(i, "food", chosenConnections)
                            chosenConnections.add(actionID)
                            action[2].append(["?", "food", "impicit", actionID])
                        if locationCount == 0:
                            actionID = self.findPossibleConnection(i, "location", chosenConnections)
                            chosenConnections.add(actionID)
                            action[2].append(["?", "location", "impicit", actionID])

                else:
                    "I don't recognize this argument!"
                action[3] = self.determineActionResult(action[2])


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
                        found = True
                        break
                    if n == 1:
                        potentialFood = self.stemmer.stem(potentialFood)
                        if potentialFood in itemList:
                            found = True
                            break
            if found:
                return potentialFood
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
                    elif count_list[k][2][l][1] == 'food':
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

    def mostPobableArguments(self, verb, global_verb_count, global_verb_type):
        count_list = []
        argumentsTypesList = ["-1-location", "-1-food", "-2-food", "-2-location", "-2-food-location"]
        count_list.append( global_verb_type[verb + "-1-location"] )
        count_list.append( global_verb_type[verb + "-1-food"])
        count_list.append( global_verb_type[verb + "-2-food"])
        count_list.append( global_verb_type[verb + "-2-location"])
        count_list.append( global_verb_type[verb + "-2-food-location"])
        # print count_list.index(max(count_list))
        return argumentsTypesList[count_list.index(max(count_list))]

    def argumentTypes(self, action):
        food = 0
        location = 0
        for arg in action:
            if arg[1] == "food":
                food +=1
            elif arg[1] == "location":
                location +=1
        return (food, location)

    def findPossibleConnection(self, actionIndex, type, disallowedConnections):
        for i in reversed(range(actionIndex)):
            if self.graph[i][3] == type and not self.graph[i][0] in disallowedConnections:
                return self.graph[i][0]

    def findPreviousMentionOfLocation(self, location, actionIndex, disallowedConnections):
        recognizedLocation = self.isCookware(location)
        for i in reversed(range(actionIndex)):
            # print "   ",self.graph[i]
            for arg in self.graph[i][2]:
                if arg[1] == "location":
                    if recognizedLocation == self.isCookware(arg[0]) and not self.graph[i][0] in disallowedConnections:
                        return self.graph[i][0]
        return False



    def __str__(self):
        return "a recipe based on "+self.filepath

    def static_vars(**kwargs):
        def decorate(func):
            for k in kwargs:
                setattr(func, k, kwargs[k])
            return func
        return decorate


#P(C) =prod{i} P(gi,vi) prod{i} prod{cp in di} P(o(cp)|d1...di1,c1...cp1,gi)
# verbsignature: DOBJ,PP,both and Origin = 0 or not
#P(R|C) = prod{i} P(vi|gi) prod{skij in Sij} funcsem(o,(part)ij) P(skij|syn,sem,C,hi)
#When the argument is a food, and o != 0 : prod{k} P(skij|food(skij,C)) P(implicit|d(i,o))
#When the argument is a food, and o = 0 : prod{l} (wl|rsw)
#When the argument is a location : explicit :(loc(i),loc(o))   implicit :P(loc(o)|vi)

# amishMeatloaf = Recipe("..\\AllRecipesData\\chunked\\BeefMeatLoaf-chunked\\amish-meatloaf.txt")
# pkl_file = open('globals.pkl', 'r')
# global_verb_count = pickle.load(pkl_file)
# global_verb_type = pickle.load(pkl_file)
# amishMeatloaf.makeConnections(global_verb_count,global_verb_type)
# pprint(amishMeatloaf.graph)

# amishMeatloaf.getIngredients()
# print amishMeatloaf