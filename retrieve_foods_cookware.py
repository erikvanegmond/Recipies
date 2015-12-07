from nltk.corpus import wordnet as wn
import pickle

output = open('cookware.pkl', 'wb')
cookingList = []

cookingStuff = wn.synset('cookware.n.01')
for s in cookingStuff.closure(lambda s:s.hyponyms()):
    cookingList +=  [str(lemma.name().replace("_", " ").lower())for lemma in s.lemmas()]
cookingStuff = wn.synset('kitchen_appliance.n.01')
for s in cookingStuff.closure(lambda s:s.hyponyms()):
    cookingList +=  [str(lemma.name().replace("_", " ").lower())for lemma in s.lemmas()]

cookingStuff = wn.synset('tableware.n.01')
for s in cookingStuff.closure(lambda s:s.hyponyms()):
    cookingList +=  [str(lemma.name().replace("_", " ").lower())for lemma in s.lemmas()]
print cookingList


pickle.dump(cookingList, output)
output.close()


output = open('foods.pkl', 'wb')
food = wn.synset('food.n.01')

foods = []
for s in food.closure(lambda s:s.hyponyms()):
    foods +=  [str(lemma.name().replace("_", " ").lower())for lemma in s.lemmas()]
food = wn.synset('food.n.02')
for s in food.closure(lambda s:s.hyponyms()):
    foods +=  [str(lemma.name().replace("_", " ").lower())for lemma in s.lemmas()]
food = wn.synset('flavorer.n.01')
for s in food.closure(lambda s:s.hyponyms()):
    foods +=  [str(lemma.name().replace("_", " ").lower())for lemma in s.lemmas()]

foods += ['sesame oil', 'poppy seeds', 'canola oil', 'baking powder', 'cornstarch', 'pecans']
foods.remove('cup')
print foods

pickle.dump(foods, output)
output.close()