# Fieldwork marketplace — research-gate notes

Reference notes for maintaining this pure-pointer marketplace. Captures the
`marketplace.json` schema, the plugin-dependency resolution rules, and the
cross-repo install behavior that the Task 1.6 acceptance test will exercise.

Verified against `code.claude.com/docs` (`plugin-marketplaces.md` and
`plugin-dependencies.md`), 2026-06.

## marketplace.json schema

Top-level fields:

- `name` (string) — marketplace identifier. Used as the `@<marketplace>` suffix
  when installing (`/plugin install magpie@fieldwork`).
- `owner` (object) — `name` is required; `email` is optional.
- `metadata` (object) — free-form; here it carries `description` and `version`.
- `plugins` (array) — one entry per member plugin.

Each plugin entry:

- `name` (string, required) — the plugin name used at install time.
- `source` (required) — where the plugin source lives (see below).
- `description` (string, optional) — short human-readable summary.

### External GitHub source shape (what this marketplace uses)

Each member is referenced by its own upstream GitHub repo — no vendored copies:

```json
"source": { "source": "github", "repo": "TimSimpsonJr/<member>" }
```

This is the only source shape used here. (A local/vendored member would instead
use a path string like `"source": "./<member>"`, which is what this repo used
*before* the pure-pointer conversion.)

## Plugin `dependencies` field

A plugin declares its dependencies in its own `plugin.json` `dependencies`
array. Each entry is either:

- a bare plugin-name string — e.g. `"librarian"`, or
- an object `{ name, version, marketplace }`.

### Version constraints resolve against git tags

A `version` constraint resolves against git tags named:

```
{plugin-name}--v{version}
```

If no matching tag exists, the dependent plugin is **disabled** with a
`no-matching-tag` error.

**Consequence for Fieldwork today:** Magpie and Research declare `librarian` as
a **bare string** so it resolves regardless of tags:

```json
"dependencies": ["librarian"]
```

Upgrade these to a version constraint (`{ "name": "librarian", "version": "..." }`)
only **after** librarian publishes tagged releases (see tagging convention
below). Pinning a version before the tag exists would disable the dependent
plugin with `no-matching-tag`.

## `allowCrossMarketplaceDependenciesOn`

- Top-level array of marketplace names, declared in the **root**
  `marketplace.json`.
- **Not needed in Fieldwork.** `librarian` is itself a member of *this*
  marketplace, so `magpie → librarian` and `research-workflow → librarian`
  resolve within the same marketplace when the members are installed via
  `fieldwork`.
- It **would** be needed if a member depended on a plugin that lives in a
  **different** marketplace. In that case the dependent's marketplace must list
  the other marketplace's name in `allowCrossMarketplaceDependenciesOn` for the
  cross-marketplace dependency to resolve.

## Cross-repo auto-pull behavior (Task 1.6 acceptance test)

When a plugin is installed, its declared dependencies are **auto-installed** and
listed at the end of the install output.

Missing dependencies get (re)resolved by any of:

- `/reload-plugins`,
- background auto-update,
- re-running the install, or
- re-adding the marketplace.

**Important caveat:** a dependency is only auto-resolved if **its marketplace is
already added**. Dependencies whose marketplace the user has *not* added are
left **unresolved**. Because `librarian` is a member of `fieldwork`, adding the
`fieldwork` marketplace and installing `magpie` (or `research-workflow`) pulls
`librarian` automatically.

Documented co-install fallback if a dependency does not pull automatically:

```
claude plugin install librarian@fieldwork
```

## Release tagging convention (for later)

When a member publishes a release, tag it as:

```
{plugin-name}--v{version}
```

Create and push the tag with:

```
claude plugin tag --push
```

Once tagged, dependents can pin that member with a `version` constraint in their
`dependencies` (instead of the current bare-string form).
