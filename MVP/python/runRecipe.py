import couchdb

# Initialize the CouchDB with databases and populate the variables
#Author: Howard Webb
#Date: 7/6/2017

recipe_db = 'recipe'

class MVP_Recipe:
    """Class representation of recipe stored in CouchDB"""

    def __init__(self, name):
        '''Initialize the object'''
        self.name = name
        self.getInstructions(name)
        self.running = False

    def getInstructions(self, name):
        '''Retreive the recipe from CouchDB by name'''
        couch = couchdb.Server()
        db = couch[recipe_db]
        doc = db[name]
        self.instructions = doc

    def run(self):
        self.running = True

# Test code, uncomment to run
recipe = MVP_Recipe('My Lettuce')
print(recipe.name)
print(recipe.instructions)
print(recipe.running)
recipe.run()
print(recipe.running)
