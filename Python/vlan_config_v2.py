devices = ('switch1', 'switch2', 'switch3')
vlans = [
    {'id': 10, 'name': 'Accounting'},
    {'id': 20, 'name': 'IT'},
    {'id': 30, 'name': 'HR'},
    {'id': 40, 'name': 'Service Desk'},
    {'id': 50, 'name': 'Finance'},
    {'id': 60, 'name': 'Marketing'},
]

def vlan_commands(vlan):
    return [f"vlan {vlan['id']}", f"name {vlan['name']}"]

def push_to_device(device, commands):
    print(f'Pushing configuration to {device}...')
    for cmd in commands:
        print(f'- {cmd}')

commands = [cmd for vlan in vlans for cmd in vlan_commands(vlan)]

for device in devices:
    push_to_device(device, commands)
    print()
    

##############

commands = []
for vlan in vlans:              # first for  → outer loop
    for cmd in vlan_commands(vlan):   # second for → inner loop
        commands.append(cmd)    # the expression at the front → what gets collected