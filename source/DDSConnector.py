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
import uuid

class DDSConnector:
    def __init__(self, idl_path = None, topic_name = None, net_config_path = None, mode = None):
        self.topic_name = topic_name
        self.idl_path = idl_path
        self.net_config_path = net_config_path
        self.mode = mode

        if idl_path and net_config_path and topic_name:
            root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
            self.workspace = os.path.join(root_path, f'__{uuid.uuid4().hex}')
            
            if os.path.isdir(self.workspace):
                os.system(f"rm -rf {self.workspace}")
            os.system(f"mkdir {self.workspace}")

            if not os.path.isfile(self.idl_path):
                raise SystemExit(f"The idl file in {self.idl_path} isn't existed")
            idl_new_path = os.path.join(self.workspace, "Messenger.idl")
            os.system(f"cp {self.idl_path} {idl_new_path}")
            self.idl_path = idl_new_path

            if not os.path.isfile(self.net_config_path):
                raise SystemExit(f"The config file in {self.net_config_path} isn't existed")
            net_config_new_path = os.path.join(self.workspace, "rtps.ini")
            os.system(f"cp {self.net_config_path} {net_config_new_path}")
            self.net_config_path = net_config_new_path

    def isIDLValid(self):
        if not os.path.isfile(self.idl_path):
            raise SystemExit(f"The idl file in {idl_path} isn't existed")
        #Add command
        try:
            subprocess.check_output(f"opendds_idl --syntax-only {idl_path}", shell=True)
        except subprocess.CalledProcessError:
            return False
        return True

    # def __del__(self): 
    #     if os.path.isdir(self.workspace):
    #         os.system(f"rm -rf {self.workspace}")


    def Build(self):
        # 1. Prepare a temporary directory to build
        cwd = os.getcwd()

        if self.mode == "subscriber" or self.mode == "publisher":
            child_folder = self.mode
        else:
            child_folder = "example"

        root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
        template_path = os.path.join(root_path, "template",child_folder)

        os.system(f"cp {template_path}/* {self.workspace}")

        # 2. build
        os.system(f"cmake -S {self.workspace} -B {self.workspace}")
        os.system(f"cmake --build {self.workspace}")


    def Run(self, inputfile = None):
        if self.mode == "subscriber" or self.mode == "publisher":
            child_folder = self.mode
        else:
            child_folder = "example"

        execution_file = "subscriber"
        if child_folder != execution_file:
            execution_file = "publisher"

        if not os.path.isfile(f"{self.workspace}/{execution_file}"):
            raise SystemExit(f"The execution file in {self.workspace}/{execution_file} isn't existed. Please try to build it before!")

        if type(inputfile) is str:
            os.system(f"{self.workspace}/{execution_file} -DCPSConfigFile {self.net_config_path} {inputfile}")
        else:
            print(f"{self.workspace}/{execution_file} -DCPSConfigFile {self.net_config_path} {self.topic_name}")
            os.system(f"{self.workspace}/{execution_file} -DCPSConfigFile {self.net_config_path} {self.topic_name}")

    # def ReceiveStreamData(self, dtStore, ckan):
    #     try:
    #         mq = sysv_ipc.MessageQueue(1234, sysv_ipc.IPC_CREAT, max_message_size = 2048)
    #         while True:
    #             try:
    #                 message = mq.receive()
    #             except OSError:
    #                 print("ERROR")
    #                 continue
    #             #print(message)
    #             length = int(message[1])
    #             #print(struct.unpack("<%ds" % length, message[0][0:length])[0].decode())
    #             msg = message[0][0:length].decode()
    #             json_data = json.loads(msg)
    #             dtStore.addDataToColumn("data", json_data)
    #             ckan.UpdateDataStore(json_data)
    #     except sysv_ipc.ExistentialError:
    #         print("ERROR: message queue creation failed")

    def PublishExample(self):
        root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
        example_path = os.path.join(root_path,"template", "example")
        inputfile = os.path.join(root_path,".example/LifetimeDogLicenses.csv")
        self.mode ="example" 
        self.Build()
        self.Run(inputfile)

if __name__ == '__main__':
    tmp1 = DDSConnector("template/Messenger.idl", "ThisIsTopic", "template/rtps.ini", "publisher")
    tmp1.Build()
    tmp1.Run()