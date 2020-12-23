import pymongo

class DataStore:
    def __init__(self):
        self.table = pymongo.MongoClient("localhost", username='root', password='example', port=27017)
        self.mydb = self.table["ckan_data"]
        self.mycol = self.mydb["dds_data"]

    def addDataToColumn(self, column_names, data):
        #json_data = json.loads(json_str)
        mydict = { column_names : data}
        self.mycol.insert_one(mydict)