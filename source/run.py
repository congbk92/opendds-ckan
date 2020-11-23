import os
import pathlib
import getopt
import sys


def is_valid_idl_file(idl_file_content):
    if idl_file_content != "":
        f = open("check_Messenger.idl", 'w')
        #Convert
        f.write(idl_file_content)
        f.close()

    #Add command


    return True

def build(idl_file_content=None):
    # 1. Prepare a temporary directory to build
    # make temp folder to build source in ${PWD}/build
    cwd = os.getcwd()
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    build_path = os.path.join(root_path, "build")
    template_path = os.path.join(root_path, "template")

    if os.path.isdir(build_path):
        command = "rm -rf {}"
        command = command.format(build_path)
        os.system(command)
    command = "mkdir {}"
    command = command.format(build_path)
    os.system(command)


    command = "cp {}/* {}"
    command = command.format(template_path, build_path)
    os.system(command)

    # 2. build
    os.chdir(build_path)
    if type(idl_file_content) is str:
        f = open("Messenger.idl", 'w')
        #Convert
        f.write(idl_file_content)
        f.close()

    command = "cmake {}"
    command = command.format(build_path)
    os.system(command)

    command = "cmake --build ."
    command = command.format(build_path)
    os.system(command)

    os.chdir(cwd)

def run(net_config_file_content = None, isPublic = None):
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    build_path = os.path.join(root_path, "build")

    rtps_file = "relay_rtps.ini"
    if type(net_config_file_content) is str:
        f = open("{}/rtps.ini".format(build_path), 'w')
        #Convert
        f.write(net_config_file_content)
        f.close()
        rtps_file = "rtps.ini"

    node_name = "subscriber"

    if isPublic:
        node_name = "publisher"

    command = "{}/{} -DCPSConfigFile {}/{}"
    command = command.format(build_path,node_name,build_path,rtps_file)   
    os.system(command)

def public_example():
    root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
    build_path = os.path.join(root_path, "build")
    if not os.path.isfile("{}/publisher".format(build_path)):
        build()
    run(isPublic=True)

    

def parse(argvs, short_opt, long_opt):
    options, arguments = getopt.getopt(
        argvs,                      # Arguments
        short_opt,                            # Short option definitions
        long_opt) # Long option definitions
    separator = "\n"
    result = list()
    for o, a in options:
        if o in ("-n", "--netConfig"):
            result += [a]
        if o in ("-i", "--idl"):
            result += [a]
    # if not arguments or len(arguments) > 3:
    #     raise SystemExit(USAGE)
    # try:
    #     operands = [int(arg) for arg in arguments]
    # except ValueError:
    #     raise SystemExit(USAGE)
    return result

def main():

    USAGE = f'''Usage: 
                    python3 {sys.argv[0]} check [-i | --idl ] 
                    python3 {sys.argv[0]} build [-i | --idl ]
                    python3 {sys.argv[0]} run   [-n | --netConfig ] [--] [-i | --idl]
                    python3 {sys.argv[0]} public
                    python3 {sys.argv[0]}'''

    if (len(sys.argv) > 1):
        if sys.argv[1] == "check":
            idl = parse(sys.argv[2:], 'i', ["idl"])[0]
            is_valid_idl_file(idl)
        elif sys.argv[1] == "build":
            idl_path = parse(sys.argv[2:], 'i', ["idl"])[0]
            build(idl)
        elif sys.argv[1] == "run":
            result = parse(sys.argv[2:], 'ni:', ["netConfig", "idl="])
            if len(result) == 2:
                build(result[1])
            run(result[0])
        elif sys.argv[1] == "public":
            public_example()
        else:
            print(sys.argv)
            print(USAGE)
    else:
        build()
        run()

if __name__ == '__main__':
    main()