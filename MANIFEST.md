# Fieldwork Plugins — Structural Map

A pure-pointer marketplace: it holds no plugin source, only a manifest pointing at
each member plugin's own repo. WHY/HOW for each plugin lives in that plugin's repo.

## Stack
- Claude Code plugin marketplace (`.claude-plugin/marketplace.json`); members referenced by GitHub source.
- Python 3 stdlib for the one test (`tests/test_marketplace.py`); no runtime code.

## Structure
```
.claude-plugin/marketplace.json   The marketplace: name `fieldwork`, 4 member entries
                                  (magpie, researcher, librarian, prose-craft->copydesk),
                                  each a github source + one-line description.
README.md                         Suite overview: lifecycle, per-plugin cards, callouts, quick start.
NOTES.md                          Maintainer reference: marketplace schema, dependency-resolution
                                  rules, the (unreliable) cross-repo auto-pull behavior.
tests/test_marketplace.py         Stdlib smoke test over the manifest (source shape, fields). Prints OK.
docs/plans/                       The README-overhaul + Copydesk-rename design + implementation plan.
.gitignore
```

## Key Relationships
- **Marketplace id is `fieldwork`** (not `fieldwork-plugins`); install with `<plugin>@fieldwork`.
- **Member source shape** is canonical `{ "source": "github", "repo": "TimSimpsonJr/<name>" }` — `test_marketplace.py` asserts exactly this.
- **Librarian is a required dependency** of Magpie and Researcher (declared in their `plugin.json`), but is installed explicitly: the documented auto-pull is unreliable (see NOTES.md).
- **The `prose-craft` member flips to `copydesk`** (name + repo + description) together with the GitHub repo rename; until then it points at the still-named `prose-craft` repo.
