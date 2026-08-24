from netmiko import ConnectHandler
from netmiko.exceptions import ConfigInvalidException


R1 = {
    "host": "172.20.20.3",
    "username": "admin",
    "password": "admin",
    "device_type":"cisco_xe"
}

configuration = ["interface lo1", "ip address 126.0.0.1 255.255.255.255", "shut", "no shut"]
conn = ConnectHandler(**R1)

def intf_config():
    with conn as c:
        output = c.send_config_set(configuration, error_pattern=r"% (Invalid|Incomplete|Ambiguous)", exit_config_mode=False)
        print(output)


def show_intf():
    with conn as c:
        prompt = c.find_prompt()
        output = c.send_command("show ip int br")
        print(output)

def external_config():
    with conn as c:
        output = c.send_config_from_file(config_file="commands.txt")
        print (output)

show_intf()

#intf_config()

#show_intf()

#external_config()

#show_intf()