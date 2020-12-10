import os
import pathlib
import getopt
import sys
import subprocess


def is_valid_idl_file(idl_path):
    if not os.path.isfile(idl_path):
        raise SystemExit(f"The idl file in {idl_path} isn't existed")

    #Add command
    try:
        subprocess.check_output(f"opendds_idl --syntax-only {idl_path}", shell=True)
    except subprocess.CalledProcessError:
        return False
    return True

def build(action, idl_path):
    # 1. Prepare a temporary directory to build
    # make temp folder to build source in ${PWD}/build
    if action == "publisher":
        child_folder = "publisher"
    else:
        child_folder = "subscriber"

    cwd = os.getcwd()
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    build_path = os.path.join(root_path, f".{child_folder}")
    template_path = os.path.join(root_path, "template",child_folder)

    if os.path.isdir(build_path):
        os.system(f"rm -rf {build_path}")
    os.system(f"mkdir {build_path}")
    os.system(f"cp {template_path}/* {build_path}")

    if not os.path.isfile(idl_path):
        raise SystemExit(f"The idl file in {idl_path} isn't existed")
    os.system(f"cp {idl_path} {build_path}/Messenger.idl")
    # 2. build
    os.chdir(build_path)
    os.system("cmake .")
    os.system("cmake --build .")
    os.chdir(cwd)

def run(action, net_config_path):
    if action == "publisher":
        node_name = "publisher"
    else:
        node_name = "subscriber"

    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    build_path = os.path.join(root_path, f".{node_name}")

    rtps_file = "relay_rtps.ini"
    if not os.path.isfile(net_config_path):
        raise SystemExit(f"The config file in {net_config_path} isn't existed")

    if not os.path.isfile(f"{build_path}/{node_name}"):
        raise SystemExit(f"The execution file in {build_path}/{node_name} isn't existed. Please try to build it before!")

    os.system(f"{build_path}/{node_name} -DCPSConfigFile {net_config_path}")

def publish_example():
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    template_path = os.path.join(root_path, "template")
    idl_path = f"{template_path}/Messenger.idl"
    net_config_path = f"{template_path}/relay_rtps.ini"
    build("publisher", idl_path)
    run("publisher", net_config_path)
    
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
            build(result[0], result[1])
            run(result[0], result[2])
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