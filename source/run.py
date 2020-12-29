import os
import pathlib
import getopt
import sys
import subprocess
import time
import sysv_ipc
import struct
import threading
import json
from CKANConnector import CKANConnector
from DataStore import DataStore
from DDSConnector import DDSConnector
import configparser


def ReceiveStreamData(dtStore, ckan):
    try:
        mq = sysv_ipc.MessageQueue(1234, sysv_ipc.IPC_CREAT, max_message_size = 2048)
        while True:
            try:
                message = mq.receive()
            except OSError:
                print("ERROR")
                continue
            #print(message)
            length = int(message[1])
            #print(struct.unpack("<%ds" % length, message[0][0:length])[0].decode())
            msg = message[0][0:length].decode()
            json_data = json.loads(msg)
            dtStore.AddDataToCollection("data", json_obj = json_data.copy())
            ckan.UpdateDataStore(json_data)
    except sysv_ipc.ExistentialError:
        print("ERROR: message queue creation failed")


def parse(argvs, short_opt, long_opt):
    options, arguments = getopt.getopt(
        argvs,              # Arguments
        short_opt,          # Short option definitions
        long_opt)           # Long option definitions
    result = list()
    for o, a in options:
        if o in ("-c", "--config"):
            result += [a]
        elif o in ("-i", "--idl"):
            result += [a]
    return result

USAGE = f'''Usage: 
                python3 {sys.argv[0]} check [-i | --idl ] 
                python3 {sys.argv[0]} run   [-c | --config]
                python3 {sys.argv[0]} publish_dds_example'''



def main():
    if (len(sys.argv) > 1):
        if sys.argv[1] == "check":
            idl_path = parse(sys.argv[2:], 'i:', ["idl="])[0]
            #To do: call api
            dds = DDSConnector(idl_path)
            if dds.IsIDLValid():
                print("valid")
            else:
                print("invalid")
        elif sys.argv[1] == "run":
            config = configparser.ConfigParser()
            config.read_file(open(parse(sys.argv[2:], 'c:', ["config="])[0]))
            if config['common']['converter'] == 'dds':
                if config['dds']['mode'] == 'subscriber':
                    dtStore = DataStore(db_name = config['common']['package_id'])

                    dtStore.AddDataToCollection("file_idl", 
                        json_obj = {"id" : dtStore.AddFileToDB(config['dds']['file_idl'])})
                    dtStore.AddDataToCollection("network_config", 
                        json_obj = {"id" : dtStore.AddFileToDB(config['dds']['network_config'])})

                    ckan = CKANConnector(config['common']['ckan_sever'], config['common']['api_token'], 
                        config['common']['resource_id'], config['common']['package_id'])
                    ckan.CreateResource(config['dds']['file_idl'], "The idl file")
                    ckan.CreateResource(config['dds']['network_config'], "The network config file")
                    x = threading.Thread(target=ReceiveStreamData, args=[dtStore,ckan], daemon=True)
                    x.start()
                dds = DDSConnector(config['dds']['file_idl'], config['dds']['topic_name'], 
                    config['dds']['network_config'], config['dds']['mode'])
                dds.Build()
                dds.Run()
        elif sys.argv[1] == "publish_example":
            DDSConnector().PublishExample()
        else:
            print(sys.argv)
            print(USAGE)
    else:
        print(sys.argv)
        print(USAGE)

if __name__ == '__main__':
    main()