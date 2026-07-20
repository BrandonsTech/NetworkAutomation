from nornir import InitNornir
from nornir.core.task import Task, Result
import time

nr = InitNornir(config_file="config.yaml")

print(nr.inventory.hosts)
print(nr.inventory.groups)
print(nr.inventory.hosts["nxos-spine1"].platform)
print(nr.inventory.hosts["nxos-spine1"]["syslog_server"])
print(nr.filter(platform="ios").inventory.hosts)


def check_config(task: Task, feature: str) -> Result:
        time.sleep(5)
        data_key = f"{feature}_server"
        message = f"{task.host.name} {feature} is {task.host[data_key]}"
        return Result(
                host=task.host,
                result=message,
        )