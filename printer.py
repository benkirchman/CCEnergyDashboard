import localDB as db
def printBuildings():
    for building in db.buildingsDict :
        print(building['value'] + ' = ' + building['label'])

printBuildings()
