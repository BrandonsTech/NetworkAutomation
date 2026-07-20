from Nornir.napalm import get_network_driver

driver = get_network_driver('eos')
device = driver(                #Driver is the object instantiated with parameters to establish the connection properly.
    hardware='eos-spine1'
    username='ntc',
    password='ntc123'
)

device.open() #Opens connection
# At this point, "device" is a NAPALM object

device.getfacts() #These facts would be structured identically, no matter the vendor. NAPALM is doing the heavy lifting.

device.get_lldp_neighbors()

for interface, neighbors in device.get_lldp_neighbors().items(): #Print lldp neighbors in readable format.
    print(f"INTERFACE: {interface}")
    print("NEIGHBORS: ")
    for neighbor in neighbors:
        print(f" - {neighbor["hostname"]}")

