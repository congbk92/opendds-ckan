import os
import pathlib


def check_idl_file(idl_file_path):
	pass

def build(idl_file_path):
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
	command = "cmake {}"
	command = command.format(build_path)
	os.system(command)

	command = "cmake --build ."
	command = command.format(build_path)
	os.system(command)

	os.chdir(cwd)

def run():
	cwd = os.getcwd()
	root_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent
	build_path = os.path.join(root_path, "build")

	command = "{}/subscriber -DCPSConfigFile {}/relay_rtps.ini"
	command = command.format(build_path,build_path)
	os.system(command)


def main():
	build("")
	run()

if __name__ == '__main__':
    main()