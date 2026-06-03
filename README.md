# Fieldwork

Fieldwork is an investigative toolkit suite for Claude Code: a family of plugins
that carry a topic from raw web research through analysis, follow-up notes, and
finally outward-facing writing.

This repository is a **pure-pointer marketplace**. It contains no plugin source.
Each member is referenced by its own upstream GitHub repo, so every plugin stays
a single source of truth in its own repository.

## Members

The four members map onto the investigative lifecycle —
**Research → Magpie → Librarian → Prose Craft**:

| Member | Repo | Role |
|--------|------|------|
| `research-workflow` | `TimSimpsonJr/research-workflow` | Deep web-research pipeline — gathers and structures source material. |
| `magpie` | `TimSimpsonJr/magpie` | Investigations analysis toolkit — works the gathered material into findings. |
| `librarian` | `TimSimpsonJr/librarian` | Structured notes for follow-up and browsing — keeps threads organized for later. |
| `prose-craft` | `TimSimpsonJr/prose-craft` | Outward-facing prose plus a review gate — turns findings into publishable writing. |

`magpie` and `research-workflow` depend on `librarian`, which is itself a member
of this marketplace, so the dependency resolves within Fieldwork on install.

## Usage

Add the marketplace, then install any member:

```
/plugin marketplace add TimSimpsonJr/fieldwork-plugins
/plugin install magpie@fieldwork
```

Swap `magpie` for `research-workflow`, `librarian`, or `prose-craft` to install
a different member. Installing a member auto-installs its declared dependencies
(for example, installing `magpie` pulls `librarian`). If a dependency does not
pull automatically, install it directly:

```
/plugin install librarian@fieldwork
```

## Notes for contributors

- **No vendoring.** Members are referenced by their own repos via GitHub
  sources in `.claude-plugin/marketplace.json`. Do not add plugin source to this
  repo. To change a plugin, change its upstream repo.
- **`obsidian-publisher` was dropped** in favor of `prose-craft`, which now
  covers Fieldwork's outward-writing role.
- See [`NOTES.md`](./NOTES.md) for the `marketplace.json` schema, the
  plugin-dependency resolution rules (tag-based versioning, bare-string vs.
  pinned deps), and the cross-repo auto-pull behavior.
- `tests/test_marketplace.py` is a stdlib-only smoke test over the manifest.
  Run it with your Python interpreter, e.g. `python tests/test_marketplace.py`
  (prints `OK` on success).

## License

MIT
