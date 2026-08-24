from netmiko import ConnectHandler

device = ConnectHandler(
    host="172.20.20.3",
    username="admin",
    password="admin",
    device_type="cisco_ios",
)

print(type(device))