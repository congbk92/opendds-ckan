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

def is_valid_idl_file(idl_path):
    if not os.path.isfile(idl_path):
        raise SystemExit(f"The idl file in {idl_path} isn't existed")

    #Add command
    try:
        subprocess.check_output(f"opendds_idl --syntax-only {idl_path}", shell=True)
    except subprocess.CalledProcessError:
        return False
    return True

def build(child_folder, idl_path):
    # 1. Prepare a temporary directory to build
    # make temp folder to build source in ${PWD}/build
    cwd = os.getcwd()
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    build_path = os.path.join(root_path, f"__{child_folder}")
    template_path = os.path.join(root_path, "template",child_folder)

    print("^^^^^^^^^^^^^^^^^^^^^^^")
    print(f"root_path: {root_path}")
    print(f"build_path: {build_path}")
    print(f"template_path: {template_path}")
    print("^^^^^^^^^^^^^^^^^^^^^^^")

    if os.path.isdir(build_path):
        os.system(f"rm -rf {build_path}")
    os.system(f"mkdir {build_path}")
    os.system(f"cp {template_path}/* {build_path}")

    if not os.path.isfile(idl_path):
        raise SystemExit(f"The idl file in {idl_path} isn't existed")
    os.system(f"cp {idl_path} {build_path}/Messenger.idl")
    # 2. build
    os.system(f"cmake -S {build_path} -B {build_path}")
    os.system(f"cmake --build {build_path}")

def run(child_folder, net_config_path, inputfile = None):
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    build_path = os.path.join(root_path, f"__{child_folder}")

    rtps_file = "relay_rtps.ini"
    if not os.path.isfile(net_config_path):
        raise SystemExit(f"The config file in {net_config_path} isn't existed")

    execution_file = "subscriber"
    if child_folder != execution_file:
        execution_file = "publisher"

    if not os.path.isfile(f"{build_path}/{execution_file}"):
        raise SystemExit(f"The execution file in {build_path}/{execution_file} isn't existed. Please try to build it before!")

    #subprocess.Popen([f"{build_path}/{node_name}", "-DCPSConfigFile" ,f"{net_config_path}"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #if action != "publisher":
    #    recvData()
    if type(inputfile) is str:
        os.system(f"{build_path}/{execution_file} -DCPSConfigFile {net_config_path} {inputfile}")
    else:
        os.system(f"{build_path}/{execution_file} -DCPSConfigFile {net_config_path}")

def recvData(dtStore, ckan):
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
            dtStore.addDataToColumn("data", json_data)
            ckan.UpdateDataStore(json_data)
    except sysv_ipc.ExistentialError:
        print("ERROR: message queue creation failed")

def publish_example():
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    example_path = os.path.join(root_path,"template", "example")
    inputfile = os.path.join(root_path,".example/LifetimeDogLicenses.csv")
    build("example", f'{example_path}/Messenger.idl')
    run("example", f'{example_path}/rtps.ini', inputfile)

    
def parse(argvs, short_opt, long_opt):
    options, arguments = getopt.getopt(
        argvs,              # Arguments
        short_opt,          # Short option definitions
        long_opt)           # Long option definitions
    result = list()
    for o, a in options:
        if o in ("-t", "--type"):
            result += [a]
        elif o in ("-n", "--netConfig"):
            result += [a]
        elif o in ("-i", "--idl"):
            result += [a]
    return result

USAGE = f'''Usage: 
                python3 {sys.argv[0]} check [-i | --idl ] 
                python3 {sys.argv[0]} run   [-t | --type] [-i | --idl ] [-n | --netConfig ]
                python3 {sys.argv[0]} publish_example'''

def main():
    #print(byteorder)
    #recvData()
    if (len(sys.argv) > 1):
        if sys.argv[1] == "check":
            idl_path = parse(sys.argv[2:], 'i:', ["idl="])[0]
            #To do: call api
            if is_valid_idl_file(idl_path):
                print("valid")
            else:
                print("invalid")
        elif sys.argv[1] == "run":
            result = parse(sys.argv[2:], 't:i:n:', ["type=","idl=", "netConfig="])
            if is_valid_idl_file(result[1]):
                dtStore = DataStore()
                dtStore.addDataToColumn("Topic", "LifetimeDogLicenses")
                dtStore.addDataToColumn("idl", open(result[1]).read())
                dtStore.addDataToColumn("netConfig", open(result[2]).read())
                build(result[0], result[1])
                #ckan = CKANConnector("http://localhost:5000", "b3c5e73a-52ef-4156-96eb-ef022746ea74", package_id="f4b61669-67d7-48c4-b114-79170f37cb5f")
                ckan = CKANConnector("http://localhost:5000", "b3c5e73a-52ef-4156-96eb-ef022746ea74", 
                    "4abbe0d0-a9ce-44ff-8ff9-d1af01078ab7")
                x = threading.Thread(target=recvData, args=[dtStore,ckan], daemon=True)
                x.start()
                run(result[0], result[2])
            else:
                raise SystemExit(f"The id file in {result[1]} is invalid. Please check")
        elif sys.argv[1] == "publish_example":
            publish_example()
        else:
            print(sys.argv)
            print(USAGE)
    else:
        print(sys.argv)
        print(USAGE)

if __name__ == '__main__':
    main()