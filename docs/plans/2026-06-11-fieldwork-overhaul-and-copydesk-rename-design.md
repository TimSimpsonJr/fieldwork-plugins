# Fieldwork suite — README/description overhaul + Copydesk rename

**Date:** 2026-06-11
**Status:** Design approved; implementation plan pending
**Scope:** Cross-repo (5 repos): `fieldwork-plugins`, `magpie`, `researcher` (dir `research-workflow`), `librarian`, `prose-craft` → `copydesk`. Plus local `~/.claude` config + `dotfiles-claude` source, and deletion of the local `dossier` repo.

## 1. Goal

Make the Fieldwork plugin suite ready to share publicly with **semi-technical journalists and OSINT researchers**. Concretely:

1. Rework every plugin's `README.md` + `plugin.json`/marketplace `description` to be accessible and feature-forward, modeled on Researcher's already-approved style, with **Mermaid** visual aids.
2. Unify the naming convention across the suite.
3. Rename the writing plugin `prose-craft` → **`copydesk`** (full migration, including the live local install) without breaking the user's local environment.
4. Rework the `fieldwork-plugins` suite README into a broad overview; drop the contributor notes.
5. Land a polished, professional, approachable presentation (badges, callouts, repo metadata).

Non-goal: changing plugin *behavior*. This is documentation, naming, and metadata only — plus the mechanical rename.

## 2. Decisions (resolved with the user)

| Question | Decision |
|---|---|
| Writing plugin's new name | **Copydesk** (`prose-craft` → `copydesk`). "Scribe" was rejected: it collides head-on with an existing `scribe` anti-AI-slop plugin in `athola/claude-night-market`. `copydesk` verified clear in the official + community marketplaces. |
| Rename depth | Full: repo + dir + `plugin.json` name + `@local` registry + agents, **with a verb skill name** (not the redundant `copydesk:copydesk`). |
| Copydesk skill names | `copydesk:write` (primary), `copydesk:learn` (learning loop). Agents become `copydesk:*` automatically. Agent base filenames (`craft-review`, `prose-review`, etc.) stay — descriptive, low-churn. |
| Suite repo "rename" | **Display only.** GitHub slug stays `fieldwork-plugins` (no URL churn, no `known_marketplaces.json` edit). README H1/title becomes "Fieldwork Plugins". |
| Visual aids | **Mermaid** (GitHub-native render, diff-friendly, no binary assets). One workflow diagram per plugin README + a lifecycle diagram in the suite README. **Retrofit Researcher** for consistency. |
| Outward-facing GitHub actions | **Staged.** All content + local files prepared first; the one `gh repo rename`, repo description/topic updates, and the Dossier delete go in a final approval checklist. |
| Repo visibility | No action — all repos (`magpie`, `researcher`, `librarian`, `prose-craft`, `fieldwork-plugins`) are already **public**. "Ready to share" is a content problem, not a visibility one. |
| Python floor | Document a single suite floor of **Python 3.12** (Magpie's `mcp-sqlite` hard-requires ≥3.12; ML stack validated on 3.12.10). Researcher still runs standalone on 3.10+, but the suite "What you need" says 3.12. |
| Worked end-to-end example | **Deferred** to a future GitHub issue (`design-input-needed`) — needs real data the user doesn't have yet. |
| Per-repo integration | **PRs + merge commits** (matches repo convention; `git log --merges` shows merge-commit style). |
| Final review | **Mandatory gate:** a rendered GitHub-style preview of every README + repo description for user review **before any merge**. |

## 3. Naming convention (the unified spec)

- **Plugin `name`** (kebab, lowercase, one word): `magpie`, `researcher`, `librarian`, `copydesk`.
- **Display name** (Title Case): Magpie, Researcher, Librarian, Copydesk. Suite display: "Fieldwork Plugins".
- **`plugin.json` `description`**: benefit-first plain-language sentence(s) in Researcher's voice, ending with a consistent suite tag: `… Part of the Fieldwork investigative suite.`
- **`marketplace.json` entry `description`**: short one-liner — `Fieldwork — <Display>: <plain benefit>.`
- **Cross-references**: always "Researcher" (never "Research"), "Copydesk" (never "Prose Craft"/"Scribe").
- **Install snippet** (identical everywhere): `/plugin marketplace add TimSimpsonJr/fieldwork-plugins` then `/plugin install <name>@fieldwork`. (Marketplace id is `fieldwork`, NOT `fieldwork-plugins` — fixes Researcher's current bug.)

## 4. Per-plugin README template

Modeled on Researcher's approved structure. Written **through the copydesk/prose-craft skill** (outward-facing prose for an audience → the user's MANDATORY voice rule applies during the writing step; the design doc itself is exempt as a coding artifact).

1. H1 (display name) + shields.io **badge row** (MIT · version · Built for Claude Code · Python 3.12 · beta)
2. 1–2 plain-language paragraphs: "what this does for a journalist"
3. **Mermaid workflow diagram** of the plugin's pipeline
4. "What you can do with it" — capabilities + example commands
5. "Why it's useful / different"
6. "Quick start" — install from Fieldwork + setup + first command
7. "Under the hood" — mechanics, tiers, tables
8. **"What you need"** callout — Python 3.12; Claude installs the optional tiers (emphasized for Magpie + Researcher, which have heavy optional deps)
9. **"Your data & privacy"** callout — where data goes; Magpie's `pii-sweep`/`redaction-check`
10. "For developers" — tests/requirements (mise/Node/Docker flagged here as contributor/full-tier only)
11. **"Part of the Fieldwork suite"** footer — sibling links + one-line roles
12. License

Each repo also gets: a rewritten `MANIFEST.md` (per the user's owned-repo rule; `fieldwork-plugins` gets one generated for the first time), a version bump, and unified GitHub `description` + `topics` (`foia`, `osint`, `journalism`, `claude-code`, plus per-plugin terms).

## 5. Suite README (`fieldwork-plugins`)

Per the approved mockup: H1 "Fieldwork Plugins"; badges; intro for journalists/OSINT; **Mermaid lifecycle diagram** (`Researcher → Magpie → Librarian → Copydesk`, Librarian noted as the shared notes layer); per-plugin cards; "What you need" + "Your data & privacy" callouts; quick start; suite footer. **Drop "Notes for contributors"** — the still-useful schema/dependency facts already live in `NOTES.md`. Generate a `MANIFEST.md`.

## 6. Copydesk migration (the careful part)

`prose-craft` is wired through **multiple** registries across **both** `~/.claude` (live) and `dotfiles-claude` (source-of-truth backup). A thorough rename audits every surface, with backups and a verify gate.

**Surfaces to update:**
- The repo: GitHub rename `prose-craft` → `copydesk` (staged), local dir rename, `plugin.json` (name + fill missing author/repo/license/keywords), major version bump → **3.0.0** (rename is breaking).
- Skills: `skills/prose-craft` → `copydesk:write`, `skills/prose-craft-learn` → `copydesk:learn`. Internal SKILL.md / script / MANIFEST self-references.
- Agents: namespace becomes `copydesk:*` automatically from the plugin name.
- `installed_plugins.json` → `prose-craft@local` key + install path.
- `settings.json` → `enabledPlugins["prose-craft@prose-craft"]` and `extraKnownMarketplaces.prose-craft` (name + `.git` URL).
- `fieldwork-plugins/.claude-plugin/marketplace.json` → member entry (name + URL + description).
- Cross-references in `librarian`, `magpie`, `fieldwork-plugins` ("Distinct from Prose Craft" → "Distinct from Copydesk").
- Global `~/.claude/CLAUDE.md` + its `dotfiles-claude` source (MANDATORY "invoke prose-craft" rule → "invoke copydesk"); `MEMORY.md`.

**Data preservation (must-not-lose):**
- Trace the exact learning-data path the skill reads/writes **before** renaming.
- Preserve the learning history and the user's **custom voice registers** (e.g. `dystopian-fiction`) found in `dotfiles-claude\claude\data\prose-craft\`.

**Operational note:** the running session keeps the old `prose-craft` skill + CLAUDE.md in context until `/reload-plugins` or restart. Expected, not a breakage.

**Verify gate (after migration):**
- `/copydesk:write` and `/copydesk:learn` resolve.
- Learning history + registers intact.
- Magpie + Researcher still load (their `librarian` dep is unaffected — nothing depended on `prose-craft`).
- Re-grep returns **zero** in-scope `prose-craft` references.
- `fieldwork-plugins/tests/test_marketplace.py` passes; the renamed repo's own pytest suite passes (update any test that hardcodes the old name).

**Backups + rollback:** snapshot `installed_plugins.json`, `known_marketplaces.json`, both `settings.json` copies (`.bak` precedent already exists). Each repo change is one revertable commit. Rollback = `gh repo rename` back + restore `.bak` files + `git revert`.

**Explicitly NOT touched:** `prose-craft-pro` (proprietary, out of scope), `claude-skills/prose-craft` (older R&D / ML-detection incubation copy), `dotfiles-claude/claude/skills/prose-craft-old` (already deprecated), the `data/prose-craft` archive (preserve; folder-rename is a low-stakes follow-up call, not part of this migration).

## 7. Dossier deletion

- No GitHub remote (`TimSimpsonJr/dossier` does not exist) — deletion is local-only.
- Capability verified folded into Researcher (`.claude/workflows/research-batch.js`, `lib/confidence.js`, `lib/schemas.js`); lessons captured in user memory.
- History is local-only (8 commits, no remote) → **`git bundle create dossier-archive.bundle --all`** to a safe location first, then delete the folder. The bundle is disposable.

## 8. Dependency findings (sweep result)

No conflicting package versions across the suite. Only shared runtime package is PyYAML — Librarian pins `==6.0.2`, Researcher leaves it unpinned → compatible. Each plugin isolates its environment (Magpie via mise `.venv`; others are light). Copydesk adds **no** Python deps (stdlib only — no requirements file). The only fix is documentation consistency: standardize the stated floor to **Python 3.12** and mark mise/Node/Docker as contributor/full-tier-only.

| Plugin | Documented Python | Runtime deps | Node/other |
|---|---|---|---|
| Magpie | 3.12 (mise-pinned 3.12.10) | heavy ML stack — tiered/opt-in | — |
| Librarian | 3.12 | `PyYAML==6.0.2` | — |
| Researcher | 3.10+ → **document 3.12** | requests, pymupdf, python-docx, rich, PyYAML | Node = dev tests; yt-dlp/Whisper/Docker = full tier |
| Copydesk | none (stdlib) | none | — |

## 9. Execution & sequencing

1. **Content fan-out (parallelizable):** the 5 READMEs + descriptions + Mermaid diagrams + MANIFESTs are independent → orchestrate via the Workflow tool. README prose authored via the copydesk/prose-craft skill.
2. **Copydesk migration (sequential):** run as one careful, backup-guarded step with the verify gate above. Not parallelized.
3. **Integration:** one branch + PR per repo; **merge commits**.
4. **Review gate (§10) before any merge.**
5. **Staged outward-facing checklist** (run only on explicit approval): `gh repo rename prose-craft copydesk`; per-repo `gh repo edit` description + topics; `git bundle` + delete Dossier; file the worked-example issue (`design-input-needed`).

## 10. Final review gate (user requirement)

Before merging anything, produce a **rendered GitHub-style preview** of:
- every plugin README + the suite README (with Mermaid diagrams rendered, badges, callouts, cards), and
- every repo's GitHub `description` + `topics` (the "About" card).

User reviews and signs off. Only then does the staged checklist run and PRs merge.

## 11. Acceptance criteria

- All 5 READMEs follow the template; all descriptions follow the convention; "Research" and "Prose Craft"/"Scribe" appear nowhere.
- Each README renders correctly on GitHub (Mermaid included) in the review preview.
- Copydesk migration passes its verify gate; zero in-scope `prose-craft` references remain; learning data + registers preserved.
- No dependency conflicts; Python 3.12 documented uniformly.
- Dossier archived + removed; worked-example issue filed.
- Nothing outward-facing executed without explicit approval.

## 12. Risks

- **Local-env breakage from the rename** → mitigated by full registry audit + backups + verify gate + documented rollback.
- **Data loss** (learning history / custom registers / Dossier history) → mitigated by tracing the data path first, preserving registers, and bundling Dossier.
- **Name re-collision** → `copydesk` verified clear; re-confirm at execution time.
- **Mermaid render differences** → caught by the §10 GitHub-render review gate before merge.
