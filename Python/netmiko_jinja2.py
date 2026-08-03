from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

device = ConnectHandler(
    host='nxos-spine1',
    username='admin',
    password='admin',
    device_type='cisco_nxos'
)

interface_dict = {
    'name': 'Ethernet1/2',
    'description': 'Server Port',
    'vlan': 10,
    'uplink': False
}

ENV = Environment(loader=FileSystemLoader('.'))
template = ENV.get_template("config.j2")
commands = template.render(interface=interface_dict)

filename = 'nxos.config'

#Store cli commands in new file
with open(filename, 'w') as config_file:
    config_file.writelines(commands)

#Send CLI commands to device from newly written file
output = device.send_config_from_file(filename)

verify = device.send_command(f'show run interface {interface_dict['name']}')
print(verify)

device.disconnect()

############################################### NETWORK TO CODE TEMPLATES
from ntc_templates.parse import parse_output
show_interfaces_parsed = parse_output(
    platform="cisco_nxos",
    command="show int brief",
    data=show_interfaces_raw,
)

print(show_interfaces_parsed[0]) #This will show structured data 