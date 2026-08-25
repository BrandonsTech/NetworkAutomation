from netmiko import ConnectHandler

R1 = {
    "host": "172.20.20.3",
    "username": "admin",
    "password": "admin",
    "device_type": "autodetect",
    "port": 22,
    "session_log": "sesh_log.txt"
}

conn = ConnectHandler(**R1)

def show_command():
    with conn as c:
        output = c.send_command("show ip int br", use_genie=True)
        output_2 = c.send_command("show run | sec syslog", use_textfsm=True)
        print("Commands have been converted into python dictionaries!")
        return output

def intf_config():
    with conn as c:
        c.establish_connection()
        config = c.send_config_from_file(config_file="intf_configs_nm.txt")
        print("Interfaces configured from file!")


def reload():
    with conn as c:
        action = c.send_command_expect("reload")
        if "confirm" in action:
            action += conn.send_command_timing("y")
        print(out)

def standard_config():
    with conn as c:
        action = c.send_config_from_file("standard_nm.txt")
        print("Standard configuration Applied!")

data = show_command()
print(type(data))

#intf_config()
#standard_config()