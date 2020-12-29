
import sys
import pymongo
import gridfs
import json

class DataStore:
    def __init__(self, db_name = "ThisIsTestData"):
        self.table = pymongo.MongoClient("localhost", username='root', password='example', port=27017)
        self.mydb = self.table[db_name]
        self.fs = gridfs.GridFS( self.mydb )

    def AddDataToCollection(self, collection_name, json_str = None, json_obj = None):
        self.mycol = self.mydb[collection_name]
        if json_str:
            obj = json.loads(json_str) 
            self.mycol.insert_one(obj)
        
        if json_obj:
            self.mycol.insert_one(json_obj)
     
    def AddFileToDB(self, input_file_path):
        return self.fs.put( open(input_file_path, 'rb')  )

# if __name__ == '__main__':
#     print(sys.argv[1])
#     tmp = DataStore()
#     tmp.AddDataToCollection("data", json_str = '{"data1" : "001", "data2" : "001"}')
#     tmp.AddFileToDB(sys.argv[1])