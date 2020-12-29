import ckanapi
import time

class CKANConnector:
    def __init__(self, server, apikey, resource_id = None, package_id = None):
        self.server = server
        self.apikey = apikey
        self.resource_id = resource_id
        self.package_id = package_id
        self.ckan = ckanapi.RemoteCKAN(self.server, apikey=self.apikey)

    def UpdateResource(self, path_of_input_file):
        resourceinfo = self.ckan.action.resource_show(id=self.resource_id)
        self.ckan.action.resource_update(id=self.resource_id,upload=open(path_of_input_file,'rb'), format=resourceinfo["format"])

    def UpdateDataStore(self, records):
        if type(records) is dict:
            result = self.ckan.action.resource_show(id=self.resource_id)
            if result["datastore_active"] is True:
                self.ckan.action.datastore_upsert(resource_id=self.resource_id, records=[records], force=True)
            else:  
                self.ckan.action.datastore_create(resource_id=self.resource_id, records=[records], 
                    primary_key=[list(records.keys())[-1]], force=True)

    def CreateResource(self, path_of_input_file, name):
        if self.package_id:
            self.ckan.action.resource_create(package_id=self.package_id,upload=open(path_of_input_file,'rb'), name=name)

# if __name__ == '__main__':
#    tmp = CKANConnector("http://localhost:5000", "b3c5e73a-52ef-4156-96eb-ef022746ea74", 
#                         "c6e659e0-4450-49f3-833d-a388b966f1b4")

#     tmp.UpdateDataStore({'a' : 'b'})

#     ckan.UpdateDataStore(json_data)
