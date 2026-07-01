import time
import concurrent.futures
import this

with concurrent.futures.ThreadPoolExecutor() as executor:




def get_commands(vlan, name):
    time.sleep(5)
    commands = []
    commands.append(f'vlan {vlan}')
    commands.append(f'name {name}')

    return commands


vlans = [{'id': '10', 'name': 'Accounting'},{'id': '20', 'name': 'HR'},{'id': '30', 'name': 'IT'}]

def run_task(vlans):
    start_time = time.time()
    for vlan in vlans:
        results = get_commands(vlan=vlan['id'], name=vlan['name'])
        print(results)
    print(f'Time Spent: {time.time() - start_time} seconds')

run_task(vlans)