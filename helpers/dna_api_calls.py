import sys
import requests
from requests.auth import HTTPBasicAuth
from env_lab import DNA_CENTER

DNAC = DNA_CENTER["host"]
DNAC_USER = DNA_CENTER["username"]
DNAC_PASSWORD = DNA_CENTER["password"]
DNAC_PORT = DNA_CENTER.get("port", 443)


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD, port=DNAC_PORT):
    """Authenticates with controller and returns a token to be used in subsequent API invocations"""

    login_url = "https://{0}:{1}/dna/system/api/v1/auth/token".format(controller_ip, port)
    result = requests.post(
        url=login_url, auth=HTTPBasicAuth(username, password), verify=False
    )
    result.raise_for_status()

    token = result.json()["Token"]
    return {"controller_ip": controller_ip, "token": token}


def create_url(path, controller_ip=DNAC, port=443):
    """Helper function to create a DNAC API endpoint URL"""

    return "https://%s:%s/api/v1/%s" % (controller_ip, port, path)


def get_url(url):

    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {"X-auth-token": token["token"]}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()


def list_network_devices():
    return get_url("network-device")


def ip_to_id(ip):
    return get_url("network-device/ip-address/%s" % ip)["response"]["id"]


def get_modules(device_id):
    return get_url("network-device/module?deviceId=%s" % device_id)


def print_info(modules):
    print(
        "{0:30}{1:15}{2:25}{3:5}".format(
            "Module Name", "Serial Number", "Part Number", "Is Field Replaceable?"
        )
    )
    for module in modules["response"]:
        print(
            "{moduleName:30}{serialNumber:15}{partNumber:25}{moduleType:5}".format(
                moduleName=module["name"],
                serialNumber=module["serialNumber"],
                partNumber=module["partNumber"],
                moduleType=module["isFieldReplaceable"],
            )
        )
