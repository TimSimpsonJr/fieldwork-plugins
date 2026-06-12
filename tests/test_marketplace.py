"""Smoke test for the fieldwork pure-pointer marketplace manifest.

Stdlib only (json + pathlib). No pytest, no third-party imports.
Run directly:

    python tests/test_marketplace.py

Exits 0 and prints "OK" on success; raises AssertionError on failure.
"""

import json
from pathlib import Path

MARKETPLACE_PATH = (
    Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
)

EXPECTED_MEMBERS = {"magpie", "researcher", "librarian", "copydesk"}


def load_marketplace():
    """Parse marketplace.json; failure to parse fails the test."""
    text = MARKETPLACE_PATH.read_text(encoding="utf-8")
    return json.loads(text)


def test_marketplace():
    data = load_marketplace()

    # Top-level identity.
    assert data["name"] == "fieldwork", f"name must be 'fieldwork', got {data['name']!r}"

    # Owner shape: name present and non-empty.
    owner = data.get("owner")
    assert isinstance(owner, dict), "owner must be an object"
    owner_name = owner.get("name")
    assert isinstance(owner_name, str) and owner_name.strip(), (
        "owner.name must be a present, non-empty string"
    )

    # Plugins: exactly the four members, by name.
    plugins = data.get("plugins")
    assert isinstance(plugins, list), "plugins must be an array"
    assert len(plugins) == 4, f"expected exactly 4 plugins, got {len(plugins)}"

    names = {p.get("name") for p in plugins}
    assert names == EXPECTED_MEMBERS, (
        f"member names must be exactly {EXPECTED_MEMBERS}, got {names}"
    )

    # Every entry: non-empty description + external github source pointing at its own repo.
    for entry in plugins:
        name = entry.get("name")

        description = entry.get("description")
        assert isinstance(description, str) and description.strip(), (
            f"plugin {name!r} must have a non-empty description"
        )

        source = entry.get("source")
        expected_source = {
            "source": "github",
            "repo": f"TimSimpsonJr/{name}",
        }
        assert source == expected_source, (
            f"plugin {name!r} source must be {expected_source}, got {source}"
        )


if __name__ == "__main__":
    test_marketplace()
    print("OK")
