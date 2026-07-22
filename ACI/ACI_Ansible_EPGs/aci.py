"""Custom Jinja2 filters for shaping ACI static-binding data.

The data files under data/ use human-friendly keys (leaf, encap). The
cisco.aci.aci_bulk_static_binding_to_epg module expects a slightly different
shape (leafs, encap_id) and must not receive orchestration-only keys such as
'state'. This filter bridges the two so the data files stay readable.
"""

# Friendly key in the data file -> key the ACI module expects.
_KEY_MAP = {
    "leaf": "leafs",
    "encap": "encap_id",
}

# Keys that control this pipeline's behaviour but are not module arguments.
_DROP_KEYS = {"state"}


def to_interface_configs(bindings):
    """Convert a list of friendly binding dicts into interface_configs.

    - renames leaf -> leafs and encap -> encap_id
    - defaults pod to 1 when omitted
    - drops orchestration-only keys (e.g. 'state')
    - passes through optional per-entry overrides such as interface_mode
      and deploy_immediacy untouched
    """
    if bindings is None:
        return []

    configs = []
    for binding in bindings:
        config = {}
        for key, value in binding.items():
            if key in _DROP_KEYS:
                continue
            config[_KEY_MAP.get(key, key)] = value
        config.setdefault("pod", 1)
        configs.append(config)
    return configs


class FilterModule(object):
    """Registers the filters with Ansible's Jinja2 environment."""

    def filters(self):
        return {"to_interface_configs": to_interface_configs}
