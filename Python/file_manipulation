read_file = open(r'C:\Cool\GitHub\NetworkAutomation\Python\hosts', 'r')
contents = read_file.read().splitlines()
print(contents)

vlans = []
"""
this is a comment
"""
for item in contents:
    if 'vlan' in item:
        ID = {}
        vlan_id = item.strip().strip('vlan').strip()
        ID['id'] = vlan_id
    elif 'name' in item:
        stripped = item.strip().strip('name').strip()
        ID['name'] = stripped
        vlans.append(ID)

for vlan in vlans:
    id = vlan.get('id')
    name = vlan.get('name')
    with open('hostss', 'a') as f: #FILE MANIPULATION
        f.write(f'vlan {id}\n')
        f.write(f'   name {name}\n')


