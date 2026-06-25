devices = ('switch1', 'switch2', 'switch3')
vlans = [
    {
    'ID': '10',
    'Name': 'Accounting'
},
{
    'ID': '20',
    'Name': 'IT'
},
{
    'ID': '30',
    'Name': 'HR'
},
{
    'ID': '40',
    'Name': 'Service Desk'
},
{
    'ID': '50',
    'Name': 'Finance'
},
{
    'ID': '60',
    'Name': 'Accounting'
}
]

def vlan_commands(vlan, name):
    commands = []
    commands.append(f'vlan {vlan}')
    commands.append(f'name {name}')
    return commands

def push_to_device(device, commands):
    for cmd in commands:
        print(f'Issuing the following commands: {cmd}')

for device in devices:
    print(f'Pushing Configuration to device: {device} now...')
    for vlan in vlans:
        vid = vlan.get('ID')
        vname = vlan.get('Name')
        command = vlan_commands(vid, vname)
        push_to_device(device, command)
        print()
