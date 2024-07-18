#concept : database -> collections -> documents(json) -> fields 

from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000")
#client = MongoClient("localhost",27017) # ou tout simpleemnt accéder au localhost avec cette ligne de code d
db = client.LOG
error = db.error
#id = error.insert_one({"origine":"tak"},{"host":"Sagemcom"}).inserted_id #recuperation de l'id attrinué lors de l'insretion 
for log in error.find() :
    print(log)
#print(id)
print("Operations :")
print([p for p in error.find({"_id":ObjectId("6693e64316cde267d1c4e49c")})])
print("done")
print([p for p in error.find({"origine":{"$in": ["Takwa", "tak"]}})])
print("done")