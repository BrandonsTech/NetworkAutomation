from netmiko import ConnectHandler

device = ConnectHandler(
    host='nxos-spine1',
    username='admin',
    password='admin',
    device_type='cisco_nxos'
)

dir(device) # Allows for viewing of all possible methods

device.find_prompt() #Finds current prompt of device

device.config_mode() #Puts the device in configuration mode

show_run_output = device.send_command('show run')

print(show_run_output[:176])

output = device.send_command_expect('end') 
#This would ERROR out because the prompt does not stay the same as before.

output = device.send_command_expect('end', expect_string='nxos-spine1#') 
#This sends the command and adjusts the prompt

commands = [
    'interface Ethernet1/1',
    'description configured by netmiko',
    'shutdown'
]

output = device.send_config_set(config_commands=commands) #Send multiple commands at once

print(output)

