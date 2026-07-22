"""Data-quality tests for the static-binding source of truth.

These run in CI with NO access to a live APIC. They catch the classes of
mistake that actually cause outages: malformed data, duplicate bindings, and
the same port/encap being claimed by two different EPGs.
"""

import collections
import json
import os
import pathlib

import jsonschema
import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
SCHEMA_PATH = pathlib.Path(__file__).with_name("schema.json")

DATA_FILES = sorted(
    str(p) for p in DATA_DIR.rglob("*.yml")
) + sorted(
    str(p) for p in DATA_DIR.rglob("*.yaml")
)


def _load(path):
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@pytest.fixture(scope="session")
def schema():
    with open(SCHEMA_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def test_data_files_exist():
    assert DATA_FILES, f"No binding definition files found under {DATA_DIR}"


@pytest.mark.parametrize("path", DATA_FILES, ids=os.path.basename)
def test_schema_valid(path, schema):
    """Each file matches the expected structure and value ranges."""
    jsonschema.validate(instance=_load(path), schema=schema)


@pytest.mark.parametrize("path", DATA_FILES, ids=os.path.basename)
def test_no_duplicate_bindings_within_file(path):
    """The same pod/leaf/interface/encap must not appear twice in one file."""
    data = _load(path)
    counts = collections.Counter(
        (b.get("pod", 1), b["leaf"], b["interface"], b["encap"])
        for b in data["bindings"]
    )
    duplicates = [key for key, n in counts.items() if n > 1]
    assert not duplicates, (
        f"Duplicate bindings in {os.path.basename(path)}: {duplicates}"
    )


def test_no_conflicting_port_encap_across_epgs():
    """A given pod/leaf/interface/encap may belong to exactly one EPG.

    Binding the same port + VLAN into two EPGs is a config error that ACI
    will reject at deploy time; catching it here fails the PR instead.
    """
    owner = {}
    conflicts = []
    for path in DATA_FILES:
        data = _load(path)
        epg = f"{data['tenant']}/{data['app_profile']}/{data['epg']}"
        for binding in data["bindings"]:
            if binding.get("state") == "absent":
                continue
            key = (
                binding.get("pod", 1),
                binding["leaf"],
                binding["interface"],
                binding["encap"],
            )
            if key in owner and owner[key] != epg:
                conflicts.append(f"{key} claimed by both {owner[key]} and {epg}")
            else:
                owner[key] = epg
    assert not conflicts, "Port/encap conflicts found:\n" + "\n".join(conflicts)
