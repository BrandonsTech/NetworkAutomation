import yaml
from netmiko import ConnectHandler

# 1. Python reads YOUR inventory.yaml file (Containerlab never touches this!)
with open("inventory/inventory.yaml", "r") as file:
    inventory = yaml.safe_load(file)

# 2. Loop through every switch defined in inventory.yaml
for hostname, data in inventory["devices"].items():
    # Strip the '/24' subnet mask to get the raw SSH IP (e.g., '172.20.20.11')
    ssh_ip = data["mgmt_ip"].split("/")[0]

    # 3. Connect to the switch that Containerlab booted on that Management IP
    conn = ConnectHandler(
        device_type="arista_eos",
        host=ssh_ip,
        username="admin",
        password="admin",
    )

    # 4. Build CLI commands dynamically from your YAML data model
    commands = [
        f"interface Loopback0",
        f"ip address {data['loopback0']}",
    ]
    for intf_name, intf_data in data["interfaces"].items():
        commands.extend([
            f"interface {intf_name}",
            f"description {intf_data['description']}",
            f"no switchport",
            f"ip address {intf_data['ipv4']}",
            f"mtu {intf_data['mtu']}",
            f"no shutdown",
        ])

    # 5. Push the configuration over SSH
    print(f"Configuring {hostname} ({ssh_ip})...")
    conn.enable()
    conn.config_mode()
    conn.send_config_set(commands, read_timeout=60)
    conn.disconnect()