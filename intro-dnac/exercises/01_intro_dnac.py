import os
import sys

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import helpers as dna


def main():
    response = dna.list_network_devices()
    print(
        "{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".format(
            "hostname", "mgmt IP", "serial", "platformId", "SW Version", "role", "Uptime"
        )
    )

    for device in response["response"]:
        uptime = "N/A" if device["upTime"] is None else device["upTime"]
        print(
            "{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".format(
                device["hostname"],
                device["managementIpAddress"],
                device["serialNumber"],
                device["platformId"],
                device["softwareVersion"],
                device["role"],
                uptime,
            )
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python 02_dnav3_dnac_interface_module.py IP_address_of_device")
        exit(0)

    device_id = dna.ip_to_id(sys.argv[1])
    modules = dna.get_modules(device_id)
    print(modules)
    dna.print_info(modules)
