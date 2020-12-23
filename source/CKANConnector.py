import ckanapi
import time
# class MyParser(argparse.ArgumentParser):
#     def error(self, message):
#         sys.stderr.write('error: %s\n' % message)
#         self.print_help()
#         self.exit(2)

# parser = MyParser(description='Uploads a file to update an existing resource in data.gov.au or other CKAN portal.',
#     epilog="Source code and issues: https://github.com/OpenCouncilData/Ckan-Upload")
# parser.add_argument('--apikey', required=True, help='Your API key for the portal. Find this on your data.gov.au user page.')
# parser.add_argument('--resource', required=True, help='URL of the resource to update (eg http://data.gov.au/dataset/geelong-drain-pipes/resource/970d4dfd-4313-45ee-be9a-6b69b47483f1)')
# parser.add_argument('filename', help='The file that will be uploaded in place of the existing resource.')

# try:
#     args = parser.parse_args()
# except:
#     parser.print_help()
#     raise SystemExit

# server = args.resource.split('/dataset')[0]
# resourceid = args.resource.split('/')[-1]

# server = "http://localhost:5000"
# resourceid = "9998fc72-2cd3-453a-aa53-75ef8dfcf84f"
# cur_apikey = "b3c5e73a-52ef-4156-96eb-ef022746ea74"

# ckan = ckanapi.RemoteCKAN(server, apikey=cur_apikey,user_agent='opencouncildata testing')

# resourceinfo = ckan.action.resource_show(id=resourceid)
# ckan.action.resource_update(id=resourceid,upload=open("run.py",'rb'), format=resourceinfo["format"])


class CKANConnector:
    def __init__(self, server, apikey, resource_id):
        self.server = server
        self.apikey = apikey
        self.resource_id = resource_id
        self.ckan = ckanapi.RemoteCKAN(self.server, apikey=self.apikey)

    def UpdateResource(self, path_of_input_file):
        resourceinfo = self.ckan.action.resource_show(id=self.resource_id)
        self.ckan.action.resource_update(id=self.resource_id,upload=open(path_of_input_file,'rb'), format=resourceinfo["format"])

    def UpdateDataStore(self, records):
        if type(records) is dict:
            if "epoch_time" not in records:
                records["epoch_time"] = time.time()
                print(records)
            result = self.ckan.action.resource_show(id=self.resource_id)
            if result["datastore_active"] is True:
                self.ckan.action.datastore_upsert(resource_id=self.resource_id, records=[records], force=True)
            else:  
                self.ckan.action.datastore_create(resource_id=self.resource_id, records=[records], 
                    primary_key=['epoch_time'], force=True)

if __name__ == '__main__':
    tmp = CKANConnector("http://localhost:5000", "b3c5e73a-52ef-4156-96eb-ef022746ea74", 
                        "c6e659e0-4450-49f3-833d-a388b966f1b4")

    tmp.UpdateDataStore({'a' : 'b'})