from pymongo import  MongoClient


db = MongoClient(  "mongodb://localhost:27017/"  ) 

test1 = db.test.test1


def getList():
    
    return list( test1.find() )

print(  getList()   )