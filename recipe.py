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
            action = item[0]
            objectList = []
            for typeCounter, cookingObject in enumerate(item[1]):
                if typeCounter == 0:
                    syntacticType = "DOBJ"
                elif typeCounter == 1:
                    syntacticType =  "PARG"
                else:
                    syntacticType =  "OARG"

                if type(cookingObject) is list:
                    for object in cookingObject[:2]:
                        food = self.isFood(object)
                        if food and food in recipeIngredients:
                            objectList.append([object, "food", syntacticType, "explicit"])
                        elif self.isCookware(object):
                            objectList.append([object, "location", syntacticType, "explicit"])
                        else:
                            objectList.append([object, "?", syntacticType])

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
                (foodCount, locationCount) = self.argumentTypes(self.getArgumentsFromAction(action))
                if locationCount:
                    for arg in self.getArgumentsFromAction(action):
                        if self.getSemanticTypeFromArgument(arg) == "location":
                            actionID = self.findPreviousMentionOfLocation(self.getSpanFromArgument(arg), i, chosenConnections)
                            if actionID:
                                chosenConnections.add(actionID)
                                arg.append(actionID)

                verb = self.getVerbFromAction(action)
                argument = self.mostPobableArguments(verb, global_verb_count, global_verb_type)

                if argument == "-1-location":
                    if foodCount == 0 and locationCount == 1:
                        pass
                    else:
                        actionID = self.findPossibleConnection(i, "location", chosenConnections)
                        if actionID:
                            chosenConnections.add(actionID)
                            self.addArgumentToAction(action, ["?", "location", "impicit", actionID])

                elif argument == "-1-food":
                    if foodCount == 1 and locationCount == 0:
                        pass
                    else:
                        actionID = self.findPossibleConnection(i, "food", chosenConnections)
                        if actionID:
                            chosenConnections.add(actionID)
                            self.addArgumentToAction(action, ["?", "food", "impicit", actionID])
                elif argument == "-2-food":
                    if foodCount >= 2 and locationCount == 0:
                        pass
                    else:
                        for j in range(2-foodCount):
                            actionID = self.findPossibleConnection(i, "food", chosenConnections)
                            if actionID:
                                chosenConnections.add(actionID)
                                self.addArgumentToAction(action, ["?", "food", "impicit", actionID])
                elif argument == "-2-location":
                    if foodCount == 0 and locationCount >= 2:
                        pass
                    else:
                        for i in range(2-locationCount):
                            actionID = self.findPossibleConnection(i, "location", chosenConnections)
                            if actionID:
                                chosenConnections.add(actionID)
                                self.addArgumentToAction(action, ["?", "location", "impicit", actionID])
                elif argument == "-2-food-location":
                    if (foodCount >=2 and locationCount == 0) or (foodCount == 0 and locationCount >= 2) or (foodCount == 1 and locationCount == 1):
                        pass
                    else:
                        if foodCount == 0:
                            actionID = self.findPossibleConnection(i, "food", chosenConnections)
                            if actionID:
                                chosenConnections.add(actionID)
                                self.addArgumentToAction(action, ["?", "food", "impicit", actionID])
                        if locationCount == 0:
                            actionID = self.findPossibleConnection(i, "location", chosenConnections)
                            if actionID:
                                chosenConnections.add(actionID)
                                self.addArgumentToAction(action, ["?", "location", "impicit", actionID])
                else:
                    "I don't recognize this argument!"
                self.setActionResultFromAction(action, self.determineActionResult(self.getArgumentsFromAction(action)))


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
        
    def getCountVerbSignature(self):
        verb_sig_count = {}
        verb_sig_list = []
        for verb in self.verb_list:
            verb_sig_count[verb + "-DOBJPARG-true"] = 0
            verb_sig_count[verb + "-DOBJ-true"] = 0
            verb_sig_count[verb + "-PARG-true"] = 0
            verb_sig_count[verb + "-DOBJPARG-false"] = 0
            verb_sig_count[verb + "-DOBJ-false"] = 0
            verb_sig_count[verb + "-PARG-false"] = 0
        for action in self.graph:
            verb_sig = self.getVerbSignature(action)
            verb_sig_list.append(verb_sig)
            self.countVerbSignature(self.getVerbFromAction(action), verb_sig, verb_sig_count)
        return (verb_sig_list, verb_sig_count)
            
    def getVerbSignature(self, action):
        dobj = 0
        parg = 0
        origin = 0
        for argument in self.getArgumentsFromAction(action):
                if self.getSyntacticTypeFromArgument(argument) == 'DOBJ':
                    dobj = dobj+1
                    if self.getOriginFromArgument(argument) is not None:
                        origin = origin + 1
                elif self.getSyntacticTypeFromArgument(argument) == 'PARG':
                    parg = parg+1
                    if self.getOriginFromArgument(argument) is not None:
                        origin = origin + 1
        if dobj > 0 and parg > 0 and origin == 0:
            verb_sig = (['DOBJ', 'PARG'], True)
        elif dobj > 0 and parg == 0 and origin == 0:
            verb_sig = (['DOBJ'], True)
        elif dobj == 0 and parg > 0 and origin == 0:
            verb_sig = (['PARG'], True)
        elif dobj > 0 and parg > 0 and origin != 0 :
            verb_sig = (['DOBJ', 'PARG'], False)
        elif dobj > 0 and parg == 0 and origin != 0:
            verb_sig = (['DOBJ'], False)
        elif dobj == 0 and parg > 0 and origin != 0:
            verb_sig = (['PARG'], False)
        else:
            print 'no verb signature made'
        return verb_sig
        
    def countVerbSignature(self, verb, verb_sig, verb_sig_count):
        flag = "true" if verb_sig[1] else "false" 
        verb_sig_count[verb + "-"  + "".join(verb_sig[0]) + "-" + flag] += 1 
            
            

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
        for action in count_list:
            if len(self.getArgumentsFromAction(action)) == 0:
                verb_count[self.getVerbFromAction(action) + "-0"] += 1
            if len(self.getArgumentsFromAction(action)) == 1:
                verb_count[self.getVerbFromAction(action) + "-1"] += 1
                fistArguent = self.getArgumentsFromAction(action)[0]
                if self.getSemanticTypeFromArgument(fistArguent) == 'location':
                    verb_type[self.getVerbFromAction(action) + "-1-location"] += 1
                if self.getSemanticTypeFromArgument(fistArguent) == 'food':
                    verb_type[self.getVerbFromAction(action) + "-1-food"] += 1
                else:
                    continue
            if len(self.getArgumentsFromAction(action)) > 1:
                location = 0;
                food = 0;
                verb_count[self.getVerbFromAction(action) + "-2"] += 1
                for arg in self.getArgumentsFromAction(action):
                    if self.getSemanticTypeFromArgument(arg) == 'location':
                        location = location + 1
                    elif self.getSemanticTypeFromArgument(arg) == 'food':
                        food = food + 1
                    else:
                        continue
                if location >= 1 and food >= 1:
                    verb_type[self.getVerbFromAction(action) + "-2-food-location"] += 1
                if location >= 2 and food == 0:
                    verb_type[self.getVerbFromAction(action) + "-2-location"] += 1
                if location == 0 and food >= 2:
                    verb_type[self.getVerbFromAction(action) + "-2-food"] += 1
                else:
                    continue

        return (verb_count, verb_type)
            

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
            if self.getSemanticTypeFromArgument(arg) == "food":
                food +=1
            elif self.getSemanticTypeFromArgument(arg) == "location":
                location +=1
        return (food, location)

    def findPossibleConnection(self, actionIndex, type, disallowedConnections):
        for i in reversed(range(actionIndex)):
            action = self.graph[i]
            argument = self.getArgumentsFromAction(action)
            if self.getActionResultFromAction(action) == type and not self.getIDfromAction(action) in disallowedConnections:
                return self.getIDfromAction(action)

    def findPreviousMentionOfLocation(self, location, actionIndex, disallowedConnections):
        recognizedLocation = self.isCookware(location)
        for i in reversed(range(actionIndex)):
            action = self.graph[i]
            for arg in self.getArgumentsFromAction(action):
                if self.getSemanticTypeFromArgument(arg) == "location":
                    if recognizedLocation == self.isCookware(self.getSpanFromArgument(arg)) and not self.getIDfromAction(action) in disallowedConnections:
                        return self.getIDfromAction(action)
        return False

    def addArgumentToAction(self, action, list):
        arguments = self.getArgumentsFromAction(action)
        arguments.append(list)

    def getIDfromAction(self, action):
        return action[0]

    def getVerbFromAction(self, action):
        return action[1]

    def getArgumentsFromAction(self, action):
        return action[2]

    def getActionResultFromAction(self, action):
        return action[3]

    def setActionResultFromAction(self, action, value):
        action[3] = value

    def getSpanFromArgument(self, argument):
        return argument[0]

    def getSemanticTypeFromArgument(self, argument):
        return argument[1]

    def getSyntacticTypeFromArgument(self, argument):
        return argument[2]

    def getPlicitFromArgument(self, argument):
        if len(argument) >= 4:
            return argument[3]

    def getOriginFromArgument(self, argument):
        if len(argument) >= 5:
            return argument[4]

    def __str__(self):
        return "a recipe based on "+self.filepath

    def static_vars(**kwargs):
        def decorate(func):
            for k in kwargs:
                setattr(func, k, kwargs[k])
            return func
        return decorate


amishMeatloaf = Recipe("..\\AllRecipesData\\chunked\\BeefMeatLoaf-chunked\\amish-meatloaf.txt")
# pprint(amishMeatloaf.graph)
pkl_file = open('globals.pkl', 'r')
global_verb_count = pickle.load(pkl_file)
global_verb_type = pickle.load(pkl_file)
amishMeatloaf.makeConnections(global_verb_count,global_verb_type)
pprint(amishMeatloaf.graph)
print amishMeatloaf.getCountVerbSignature()


# print amishMeatloaf.verbCounter()
# amishMeatloaf.getIngredients()
# print amishMeatloaf
