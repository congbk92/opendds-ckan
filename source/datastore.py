import pymongo

myclient = pymongo.MongoClient("localhost", username='root', password='example', port=27017)
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

mydict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)