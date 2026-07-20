from nornir_napalm.plugins.tasks import napalm_configure
from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")
results = nr.filter(platform="eos").run(
    task=napalm_configure,
    dry_run=False,
    replace=False,
    configuration="snmp-server community secret123 rw"
)

print(results["eos-spine1"].diff)