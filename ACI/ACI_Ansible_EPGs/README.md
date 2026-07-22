# ACI Static Port Bindings — GitOps Pipeline

Manage Cisco ACI EPG static port bindings as version-controlled YAML. A change
is proposed as a pull request, validated automatically with no access to a live
device, and applied to the fabric only after it merges to `main`.

```
YAML change  ──►  PR opened  ──►  validate (lint · schema · syntax)  ──►  merge
                                                                            │
                                                              approve (environment)
                                                                            │
                                                          check mode ──► apply to APIC
```

The YAML files under `data/` are the source of truth: what they describe is what
the fabric is made to look like. Bindings are applied through the
`cisco.aci.aci_bulk_static_binding_to_epg` module, so each EPG needs at most two
API calls (one to add/update, one to remove) no matter how many ports it has.

## Repository layout

```
aci-static-port-bindings/
├── ansible.cfg                     # points at the local inventory + filter plugin
├── requirements.txt                # python tooling (ansible, pytest, linters)
├── requirements.yml                # galaxy collection (cisco.aci)
├── inventory/
│   └── hosts.yml                   # localhost only; APIC reached over HTTPS
├── data/                           # ── SOURCE OF TRUTH ──
│   └── prod_tn/
│       ├── web_epg.yml             # one file per EPG
│       └── db_epg.yml
├── playbooks/
│   ├── deploy_static_bindings.yml  # discovers every data file and reconciles it
│   └── tasks/
│       └── reconcile_epg.yml       # add/update + remove logic for one EPG
├── filter_plugins/
│   └── aci.py                      # shapes friendly YAML into module arguments
├── tests/
│   ├── schema.json                 # structure + value ranges for a data file
│   ├── test_data_validation.py     # schema + duplicate + cross-EPG conflict checks
│   └── test_filters.py             # unit tests for the filter
└── .yamllint / .ansible-lint       # lint configuration

.github/workflows/
└── aci-static-bindings.yml         # CI/CD — lives at the REPO ROOT, not here
```

> The workflow file must sit at `.github/workflows/` in the repository root.
> If you place this project folder somewhere other than the repo root, update
> the `paths:` filters and `working-directory` in the workflow to match.

## Prerequisites

- Python 3.10+
- Network reachability from wherever you run `apply` to the APIC (see
  [CI/CD](#cicd) for why this matters for the deploy job)

## Setup

```bash
cd aci-static-port-bindings
python -m pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

## APIC access (no secrets in the repo)

Connection details are read from the environment, never stored in files.

Locally:

```bash
export ACI_HOST=apic.example.com
export ACI_USERNAME=automation
export ACI_PASSWORD='...'          # consider `read -s ACI_PASSWORD` to avoid shell history
export ACI_VALIDATE_CERTS=true     # set false only for lab/self-signed certs
```

In CI: add `ACI_HOST`, `ACI_USERNAME`, and `ACI_PASSWORD` as repository or
environment secrets (Settings → Secrets and variables → Actions). The `deploy`
job reads them from `secrets.*`. Use a dedicated automation account scoped to
the tenants it manages, not `admin`.

## Everyday workflow

### Add a binding

Edit the relevant EPG file and add a line, then open a PR:

```yaml
bindings:
  - {pod: 1, leaf: 106, interface: "1/12", encap: 100}
```

### Remove a binding

Set `state: absent` on the entry and open a PR. After it merges and the apply
runs, delete the line in a follow-up commit so the file keeps describing only
what should exist:

```yaml
bindings:
  - {pod: 1, leaf: 105, interface: "1/30", encap: 100, state: absent}
```

### Run it locally

```bash
# validate without touching anything
pytest -v
ansible-playbook playbooks/deploy_static_bindings.yml --syntax-check

# preview the exact changes against the fabric
ansible-playbook playbooks/deploy_static_bindings.yml --check --diff

# apply
ansible-playbook playbooks/deploy_static_bindings.yml --diff
```

## Data model

| Field                     | Where            | Required | Notes                                                     |
|---------------------------|------------------|----------|-----------------------------------------------------------|
| `tenant`                  | top level        | yes      | Existing tenant name                                      |
| `app_profile`             | top level        | yes      | Existing application profile                              |
| `epg`                     | top level        | yes      | Existing EPG                                              |
| `defaults.interface_type` | top level        | no       | `switch_port` (default), `port_channel`, `vpc`            |
| `defaults.interface_mode` | top level        | no       | `trunk` (default), `untagged`, `native`                   |
| `defaults.deploy_immediacy` | top level      | no       | `lazy` (default) or `immediate`                           |
| `pod`                     | per binding      | no       | Defaults to `1`                                           |
| `leaf`                    | per binding      | yes      | Leaf node ID                                              |
| `interface`               | per binding      | yes      | e.g. `"1/10"` (quote it)                                  |
| `encap`                   | per binding      | yes      | VLAN ID, 1–4094                                           |
| `interface_mode`          | per binding      | no       | Overrides the file default for this port                 |
| `state`                   | per binding      | no       | `present` (default) or `absent`                           |

The tenant, application profile, and EPG must already exist. This pipeline
manages port bindings only; provisioning the objects above is out of scope
(the `cisco.aci.aci_tenant`, `aci_ap`, and `aci_epg` modules cover that).

> `interface_mode` accepts the friendly values above. The exact set the module
> accepts can vary slightly by ACI/collection version — if a value is rejected
> at apply time, check the module documentation for your version and adjust the
> `enum` in `tests/schema.json` to match.

## CI/CD

**`validate`** runs on every PR and push. It lints the YAML, runs the data
tests (schema, duplicate detection, cross-EPG conflict detection), syntax-checks
the playbook, and runs `ansible-lint`. It never contacts a device, so it is safe
on untrusted pull requests and needs no secrets.

**`deploy`** runs only after a merge to `main`, only if `validate` passed, and
is gated by a GitHub Environment named `production`. Create that environment
(Settings → Environments) and add a required reviewer to force a manual approval
before any change reaches the fabric. It runs check mode first, then applies.

> **GitHub-hosted runners cannot reach a private APIC.** Register a
> [self-hosted runner](https://docs.github.com/actions/hosting-your-own-runners)
> with network access to the APIC and change `runs-on:` in the `deploy` job to
> `[self-hosted]`, or trigger the playbook from your own CD system. The
> workflow ships with `runs-on: ubuntu-latest` purely so the file is complete.

## A note on pruning (important)

This pipeline is authoritative for the bindings it *knows about*: it adds and
updates everything listed as present, and removes anything marked `absent`. It
does **not** automatically delete a binding that exists on the fabric but was
never in these files (for example, one added by hand in the GUI). Removal is
always explicit, via `state: absent`, which keeps a clear record in Git history
of what was removed and when.

If you want strict declarative pruning — where deleting a line makes the binding
disappear from the fabric automatically — that is exactly what Terraform's
`aci_bulk_epg_to_static_path` resource does natively, because Terraform tracks
state and reconciles to it. The trade-off is that Terraform will also revert any
out-of-band change, and you take on state-file management. Pick the model that
matches how your team actually operates.

## Extending

- **More tenants/EPGs:** add `data/<tenant>/<epg>.yml`; the playbook discovers
  it automatically.
- **Port-channel / vPC:** set `defaults.interface_type` to `port_channel` or
  `vpc`. For those, `interface` becomes the interface policy group name and the
  path uses `protpaths` for vPC — extend `tests/schema.json` and the example
  data accordingly.
- **Pre-merge preview against a lab APIC:** if you have a lab fabric reachable
  from CI, add a check-mode job to the PR trigger using lab secrets, so
  reviewers see the diff before approving.
