devices = []
if devices:
    print("Devices found")
if not devices:
    print("No devices found")

interfaces = ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2"]
ip_addr = "1.1.1.1"
vrf = "management"
command = f"ping {ip_addr} vrf {vrf}"
print(command)

new_command = ' : '.join(interfaces)
print(new_command)

print(interfaces[2])

hostname = "DEVICE_1234567890987654321"
hostname_length = len(hostname)
hostname_pos = hostname[:8]
print(hostname_length)
print(hostname_pos)
hostname_dir = dir(interfaces)
interfaces.append("Ethernet0/3")
print (interfaces)
interfaces.insert(1, "Ethernet0/0.1")
print(interfaces)
device_1 = {'hostname': 'R1', 'vendor': 'cisco', 'os': '15.1'}
print(device_1['hostname'])
print(device_1['vendor'])
print(device_1['os'])
device_1['hostname'] = 'R2'
print(device_1['hostname'])
oper = {'cpu': '50%','temp': '36C'}
device_1.update(oper)
print(device_1)
print(device_1.items())
for key, value in device_1.items():
    print(f"{key}, {value}")
vendors = ['cisco', 'arista', 'HP', 'Dell']
approved_vendors = ['cisco']
print(len(vendors))
description = ("Router1", "PORTLAND")
print(type(description))
hostname = "NYC"
if hostname == 'DEVICE_1234567890987654321':
    print("This Device exists!")
elif hostname == "OTHER_DEVICE":
    print("This is a new device")
elif hostname == "NYC":
    print("this is in NYC")
else:
    print ("UNKNOWN DEVICE")
if 'arista' in vendors:
    print("Arista is deployed")

### Combining for loop with "in" and "not in"
for vendor in vendors:
	if vendor not in approved_vendors:
		print(f'Vendor not approved: {vendor}')
          
### BGP Command Dictionary
BGP_COMMANDS = {
     'neighbors': 'neighborssssss',
     'description': 'Description: {}',
     'network': 'network {}',
     'neighbor': 'neighbor {}',
}

BGP_PARAMS = {
     'description': 'Configured using Python',
     'network': '10.0.0.0 mask 255.255.255.0',
     'neighbor': '1.2.3.4'
}

commands_list = []

### Our first for loop

for feature, value in BGP_PARAMS.items():
     commandss = BGP_COMMANDS.get(feature).format(value)
     commands_list.append(commandss)
commands_list.insert(0, 'interface ethernet1/10')
print(commands_list)

print(BGP_COMMANDS.get('neighbors'))

for index, each in enumerate(vendors):
    print(f'{index} {each}')