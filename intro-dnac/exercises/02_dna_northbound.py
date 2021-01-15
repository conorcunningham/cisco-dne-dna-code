import os
import sys

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import helpers as dna


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python 02_dnav3_dnac_interface_module.py IP_address_of_device")
        exit(0)

    device_id = dna.ip_to_id(sys.argv[1])
    modules = dna.get_modules(device_id)
    dna.print_info(modules)
