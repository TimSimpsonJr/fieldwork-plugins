# Fieldwork overhaul + Copydesk rename — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.
> **README prose** (anything in a `README.md` body) MUST be authored through the `prose-craft` (→ `copydesk`) skill — it is outward-facing prose. Plan/design/MANIFEST text is exempt (coding artifacts).

**Goal:** Make the Fieldwork suite shareable with semi-technical journalists/OSINT researchers: accessible READMEs + descriptions with Mermaid visuals, a unified naming convention, the `prose-craft` → `copydesk` rename (without breaking the local env), a reworked suite README, Dossier removal, and a GitHub-render review gate before any merge.

**Architecture:** Five independent repos. Parallelizable *content* work (READMEs/descriptions/diagrams/MANIFESTs) fans out; the *Copydesk migration* runs sequentially with backups + a verify gate. One branch + PR per repo, merge commits. Every outward-facing action (GitHub repo rename, repo description/topics, Dossier delete, issue filing, PR merges) is gated behind explicit user approval and the render-review checkpoint.

**Tech Stack:** Markdown, Mermaid (GitHub-native), shields.io, JSON (`plugin.json` / `marketplace.json`), `gh` CLI, Python (existing pytest suites), `git`.

**Source design:** `fieldwork-plugins/docs/plans/2026-06-11-fieldwork-overhaul-and-copydesk-rename-design.md`

**Paths (absolute):**
- `magpie` → `C:\Users\tim\OneDrive\Documents\Projects\magpie`
- `researcher` (dir) → `C:\Users\tim\OneDrive\Documents\Projects\research-workflow`
- `librarian` → `C:\Users\tim\OneDrive\Documents\Projects\librarian`
- `copydesk` (currently) → `C:\Users\tim\OneDrive\Documents\Projects\prose-craft`
- `fieldwork-plugins` → `C:\Users\tim\OneDrive\Documents\Projects\fieldwork-plugins`
- dossier → `C:\Users\tim\OneDrive\Documents\Projects\dossier`
- live config → `C:\Users\tim\.claude\` · dotfiles source → `…\Projects\dotfiles-claude\claude\`

---

## Shared reference: README template (apply to every plugin)

Author via the prose-craft/copydesk skill. Section order:

1. `# <Display name>` + shields.io badge row
2. 1–2 plain-language paragraphs ("what this does for a journalist")
3. `## How it works` — a **Mermaid** `flowchart` of the pipeline
4. `## What you can do with it` — capabilities + example commands
5. `## Why it's useful`
6. `## Quick start` — marketplace add + `/plugin install <name>@fieldwork` + setup + first command
7. `## Under the hood` — mechanics/tiers/tables
8. `> [!NOTE] What you need` — Python 3.12; Claude installs optional tiers
9. `> [!IMPORTANT] Your data & privacy` — where data goes; Magpie's pii-sweep/redaction
10. `## For developers` — tests/requirements (mise/Node/Docker = contributor/full-tier only)
11. `## Part of the Fieldwork suite` — sibling links + one-line roles
12. `## License`

Badge row (sentence-case labels, flat style):
```markdown
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-<v>-informational)
![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-8A3FFC)
![Python](https://img.shields.io/badge/python-3.12-3776AB)
![Status](https://img.shields.io/badge/status-beta-orange)
```

Suite footer (identical everywhere, link the four repos + roles):
```markdown
## Part of the Fieldwork suite
- [Researcher](https://github.com/TimSimpsonJr/researcher) — gather sources into cited notes
- [Magpie](https://github.com/TimSimpsonJr/magpie) — analyze FOIA/data into findings
- [Librarian](https://github.com/TimSimpsonJr/librarian) — file findings as linked notes (shared layer)
- [Copydesk](https://github.com/TimSimpsonJr/copydesk) — write findings up in your voice
```

Description convention: `plugin.json.description` = benefit-first sentence(s) + ` Part of the Fieldwork investigative suite.` · `marketplace.json` entry = `Fieldwork — <Display>: <plain benefit>.`

---

## Phase 0 — Safety net (non-destructive; do first)

### Task 0.1: Back up local registries + config
**Step 1:** Copy each file with a `.bak.copydesk-rename` suffix:
```bash
ts=$(date +%Y%m%d-%H%M%S)
cd "/c/Users/tim/.claude/plugins"
cp installed_plugins.json "installed_plugins.json.bak.copydesk-$ts"
cp known_marketplaces.json "known_marketplaces.json.bak.copydesk-$ts"
cp "/c/Users/tim/.claude/settings.json" "/c/Users/tim/.claude/settings.json.bak.copydesk-$ts"
cp "/c/Users/tim/.claude/CLAUDE.md" "/c/Users/tim/.claude/CLAUDE.md.bak.copydesk-$ts"
```
**Verify:** `ls /c/Users/tim/.claude/plugins/*.bak.copydesk-* /c/Users/tim/.claude/*.bak.copydesk-*` → 4 files listed.

### Task 0.2: Archive Dossier history (bundle now, delete later)
**Step 1:**
```bash
cd "/c/Users/tim/OneDrive/Documents/Projects/dossier"
git bundle create "../dossier-archive-$(date +%Y%m%d).bundle" --all
```
**Verify:** `git bundle verify ../dossier-archive-*.bundle` → "is okay". (Folder deletion happens only in Phase 6, on approval.)

### Task 0.3: Trace the Copydesk learning-data path (discovery)
**Step 1:** Read how the skill locates learning data + registers:
```bash
grep -rnE "data/prose-craft|\.claude/data|CLAUDE_PLUGIN_ROOT|learning/|registers/" \
  "/c/Users/tim/OneDrive/Documents/Projects/prose-craft/skills" \
  "/c/Users/tim/OneDrive/Documents/Projects/prose-craft/scripts"
```
**Step 2:** Record the resolved path(s) in a scratch note. Decide: does the data path key on the plugin name (→ must migrate the folder) or live inside `${CLAUDE_PLUGIN_ROOT}/learning` (→ travels with the reinstall)?
**Verify:** the data path is documented before any rename step runs. **Blocks Phase 3.**

---

## Phase 1 — Per-plugin content (parallelizable; Workflow fan-out)

> Each plugin: own branch `docs/readme-overhaul`, own PR. Author README via prose-craft/copydesk skill, then commit. Do NOT merge — Phase 5 gate first.

### Task 1.1: Magpie README + description + MANIFEST
**Files:** Modify `magpie/README.md`, `magpie/.claude-plugin/plugin.json`, `magpie/MANIFEST.md`
**Steps:**
1. `git -C magpie checkout -b docs/readme-overhaul`
2. Rewrite `README.md` to the template. Mermaid `flowchart`: `archive-evidence → ingest → pii-sweep → dataset-analyze / entity-extract → redaction-check → findings (via Librarian)`. Emphasize the "What you need" callout (heavy optional ML tiers; Claude installs them). Privacy callout highlights `pii-sweep` + `redaction-check`.
3. `plugin.json.description` → convention (benefit-first + suite tag); bump `version` 0.2.1 → 0.2.2.
4. Rewrite `MANIFEST.md` to the owned-repo budget (50–80 lines).
5. **Verify render locally:** `grep -c '```mermaid' magpie/README.md` → ≥1; `grep -n 'fieldwork-plugins' magpie/README.md` shows `@fieldwork` install (not `@fieldwork-plugins`).
6. Commit: `git -C magpie commit -am "docs: accessible README + Mermaid + unified description"`

### Task 1.2: Researcher README retrofit + description
**Files:** Modify `research-workflow/README.md`, `research-workflow/.claude-plugin/plugin.json` (+ `marketplace.json`)
**Steps:**
1. Branch `docs/readme-overhaul`.
2. **Light touch** (already gold standard): add badge row, a Mermaid `flowchart` (`triage → resolve → hop loop (search→fetch→summarize→plan) → quality gate → classify → write (Librarian) → discover threads`), the "What you need" + privacy callouts, the suite footer.
3. **Fix the bug:** `@fieldwork-plugins` → `@fieldwork` in the install snippet.
4. Confirm `plugin.json.description` ends with the suite tag; bump 3.2.0 → 3.2.1.
5. **Verify:** `grep -n '@fieldwork-plugins' research-workflow/README.md` → no matches; `grep -c '```mermaid' research-workflow/README.md` → ≥1.
6. Commit.

### Task 1.3: Librarian README + description + MANIFEST
**Files:** Modify `librarian/README.md`, `librarian/.claude-plugin/plugin.json`, `librarian/MANIFEST.md`
**Steps:**
1. Branch `docs/readme-overhaul`.
2. Rewrite README to template. Mermaid `flowchart`: `findings → classify (content-type/tags) → write notes (Markdown/CSV) → wikilink scan → MOC update`. Note it's the shared output layer for Magpie + Researcher.
3. `plugin.json.description` → convention (de-jargon the current text; "Research" → "Researcher"; "Prose Craft" → "Copydesk"); bump 0.1.0 → 0.1.1.
4. Rewrite `MANIFEST.md`.
5. **Verify:** `grep -niE 'prose.?craft|"Research"' librarian/README.md librarian/.claude-plugin/plugin.json` → only "Researcher"/"Copydesk", zero "prose-craft"/"Prose Craft".
6. Commit.

### Task 1.4: Copydesk README content (still in `prose-craft` dir; rename in Phase 3)
**Files:** Modify `prose-craft/README.md`, `prose-craft/.claude-plugin/plugin.json`
**Steps:**
1. Branch `docs/readme-overhaul`.
2. Rewrite README to template under the **Copydesk** name. Mermaid `flowchart`: `register select → draft in voice → dual review gate (AI-pattern + craft) → learning loop (sharpen from edits)`. Privacy callout: prose stays local.
3. `plugin.json`: set `description` to convention; **fill missing fields** (`author`, `repository: https://github.com/TimSimpsonJr/copydesk`, `license: MIT`, `keywords`); leave `name` as `prose-craft` for now (Phase 3 flips it atomically with the registries).
4. **Verify:** `grep -c '```mermaid' prose-craft/README.md` → ≥1; README contains "Copydesk", not "Prose Craft".
5. Commit.

---

## Phase 2 — Suite README + marketplace manifest

### Task 2.1: Rework `fieldwork-plugins/README.md`
**Files:** Modify `fieldwork-plugins/README.md`; ensure `NOTES.md` retains schema/dependency facts
**Steps:**
1. On branch `docs/fieldwork-overhaul-copydesk-rename` (already created).
2. Rewrite README per the approved mockup: H1 "Fieldwork Plugins", badge row, journalist-facing intro, Mermaid lifecycle diagram (`Researcher → Magpie → Librarian → Copydesk`, Librarian = shared layer), plugin cards, "What you need" + "Your data & privacy" callouts, quick start, suite footer.
3. **Delete the "Notes for contributors" section.** Confirm its schema/dependency facts already exist in `NOTES.md` (they do); if any unique fact is only in the README, move it to `NOTES.md` first.
4. **Verify:** `grep -n 'Notes for contributors' fieldwork-plugins/README.md` → no matches; `grep -c '```mermaid' fieldwork-plugins/README.md` → ≥1.

### Task 2.2: Update `marketplace.json` descriptions + naming
**Files:** Modify `fieldwork-plugins/.claude-plugin/marketplace.json`
**Steps:**
1. Set each member `description` to the convention; "Research" → "Researcher". Leave the `prose-craft` member entry's **name/URL** for Phase 3 (it flips with the rename); update its description text to the Copydesk wording now is OK only if name stays `prose-craft` until Phase 3 — **defer the whole prose-craft entry to Phase 3** to keep name+url+desc atomic.
2. **Verify:** `python tests/test_marketplace.py` (from `fieldwork-plugins/`) → prints `OK`.

### Task 2.3: Generate `fieldwork-plugins/MANIFEST.md`
**Files:** Create `fieldwork-plugins/MANIFEST.md`
**Steps:** Author to the owned-repo format (Stack / Structure / Key Relationships, 50–80 lines). Add the cheap per-entry word-budget guard test if practical.
**Verify:** line count `wc -l < fieldwork-plugins/MANIFEST.md` ≤ 120.

---

## Phase 3 — Copydesk migration (SEQUENTIAL; do not parallelize)

> Pre-req: Phase 0 backups + Task 0.3 data-path trace complete. Work on a branch `chore/rename-to-copydesk` inside the prose-craft repo. The GitHub repo rename itself is **staged to Phase 6**; everything here is local + content.

### Task 3.1: Rename repo content (in place, dir still `prose-craft`)
**Files:** `prose-craft/.claude-plugin/plugin.json`, `prose-craft/.claude-plugin/marketplace.json`, `skills/prose-craft/` → `skills/copydesk-write/` (skill `name: copydesk` / command surface `copydesk:write`), `skills/prose-craft-learn/` → `skills/copydesk-learn/`, `agents/*.md` (namespace refs), `scripts/discipline_check.py`, `MANIFEST.md`, internal SKILL.md self-references.
**Steps:**
1. Set `plugin.json.name` → `copydesk`; `version` → `3.0.0`.
2. Rename skill dirs + update each `SKILL.md` `name:`/frontmatter to `copydesk-write` / `copydesk-learn` (verb skill names; the user rejected `copydesk:copydesk`).
3. Update the local `marketplace.json` (name → `copydesk`, plugin entry, source).
4. Find/replace remaining in-repo `prose-craft` → `copydesk` (skip historical `docs/plans`, `docs/handoffs` content if desired; update active SKILL/script/agent/MANIFEST).
5. **Verify:** `grep -rIl "prose-craft" prose-craft/skills prose-craft/agents prose-craft/scripts prose-craft/.claude-plugin` → empty.
6. Run the repo's own tests: `pytest -q` (from prose-craft repo) → pass; update any test asserting the old name.
7. Commit on `chore/rename-to-copydesk`.

### Task 3.2: Preserve learning data + registers (COPY the live install — never reinstall from repo)
**Finding (Task 0.3, confirmed):** the live data lives INSIDE the install dir `~/.claude/plugins/cache/local/prose-craft/2.0.0/` — `learning/` (accumulator.md = 23-obs file, `snapshots/` incl. `manifest.json`, `splits.md`, `ablation-log.md`, `bootstrap-run.md`) and `registers/` (advocacy.md, personal.md, dystopian-fiction.md). The **repo's** `learning/`+`registers/` are EMPTY templates. The skill reads `${CLAUDE_PLUGIN_ROOT}/learning` + `/registers` (install-dir-relative, NOT keyed on the name string). `dotfiles-claude/claude/data/prose-craft/` is a version-controlled BACKUP of this live data. A prior handoff explicitly warns: NEVER do a naive full reinstall — it overwrites live registers/accumulator with the repo's empty templates.
**Steps:**
1. Create `~/.claude/plugins/cache/local/copydesk/3.0.0/` by **copying the entire old install dir** `…/local/prose-craft/2.0.0/` into it (carries `learning/` + `registers/` intact).
2. Apply the Task 3.1 rename edits **on top of the copy** (rename skill dirs, set `plugin.json` name/version, internal refs). Do NOT overwrite `learning/`/`registers/` from the repo.
3. Rename the dotfiles backup dir `dotfiles-claude/claude/data/prose-craft/` → `…/data/copydesk/` (keeps the backup convention consistent).
4. Keep the old `…/local/prose-craft/2.0.0/` dir untouched until the verify gate passes (it is the rollback source).
**Verify:** `~/.claude/plugins/cache/local/copydesk/3.0.0/registers/dystopian-fiction.md`, `…/learning/accumulator.md` (the 23-obs file, not the empty template), and `…/learning/snapshots/manifest.json` all exist.

### Task 3.3: Update local registries (live + dotfiles)
**Files:** `~/.claude/plugins/installed_plugins.json`, `~/.claude/settings.json`, `dotfiles-claude/claude/settings.json`, the local plugin cache dir.
**Steps:**
1. The new `copydesk@local` install dir was created by **copying** the old install (Task 3.2) — do NOT reinstall from the repo. Point the registry at it.
2. `installed_plugins.json`: rename key `prose-craft@local` → `copydesk@local`.
3. Both `settings.json` copies: `enabledPlugins["prose-craft@prose-craft"]` → `copydesk@copydesk`; `extraKnownMarketplaces.prose-craft` → `copydesk` (+ `.git` URL → `…/copydesk.git`).
4. **Verify:** `grep -rn "prose-craft" ~/.claude/settings.json ~/.claude/plugins/installed_plugins.json` → empty.

### Task 3.4: Update cross-references + global config
**Files:** `librarian/**` , `magpie/**`, `fieldwork-plugins/**`, `~/.claude/CLAUDE.md` + `dotfiles-claude/claude/CLAUDE.md`, `MEMORY.md`
**Steps:**
1. "Distinct from Prose Craft" → "Distinct from Copydesk" (librarian description + docs).
2. Global CLAUDE.md MANDATORY rule: "invoke the `prose-craft` skill" → "invoke the `copydesk` skill" (both live + dotfiles copies).
3. Update `MEMORY.md` + the relevant memory file(s).
4. `fieldwork-plugins/.claude-plugin/marketplace.json`: flip the deferred prose-craft member entry → `copydesk` (name + URL `…/copydesk.git` + description).
5. **Verify:** scoped grep returns zero in-scope `prose-craft`:
```bash
grep -rIl "prose-craft" \
  "/c/Users/tim/OneDrive/Documents/Projects/librarian" \
  "/c/Users/tim/OneDrive/Documents/Projects/magpie" \
  "/c/Users/tim/OneDrive/Documents/Projects/fieldwork-plugins" \
  "/c/Users/tim/.claude/CLAUDE.md" \
  --include=*.md --include=*.json --include=*.py | grep -vE "docs/(plans|handoffs)" || echo CLEAN
```
Expected: `CLEAN`.

### Task 3.5: Verify gate (after `/reload-plugins`)
**Steps:**
1. `/reload-plugins` (or note restart needed — this session keeps the old skill in context).
2. Confirm `/copydesk:write` + `/copydesk:learn` resolve.
3. Confirm Magpie + Researcher still load (no broken dep — nothing depended on prose-craft).
4. Re-run Task 3.4 grep → `CLEAN`; learning history + registers present.
5. `python fieldwork-plugins/tests/test_marketplace.py` → `OK`.
**Verify:** all five checks pass. **Blocks Phase 6 for the copydesk repo.**

---

## Phase 4 — Dependency-doc consistency (fold into Phase 1 where touched)

### Task 4.1: Unify documented Python floor to 3.12
**Files:** `research-workflow/README.md` (the "Requirements: Python 3.10+" line), any operator guide stating 3.10+.
**Steps:** State **Python 3.12** as the suite floor; clarify mise/Node/Docker as contributor/full-tier only; note Claude installs optional tiers.
**Verify:** `grep -rn "3.10+" research-workflow/README.md` → no matches (or reframed as "standalone 3.10+, suite 3.12").

---

## Phase 5 — GitHub-render review gate (MANDATORY before any merge)

### Task 5.1: Produce a rendered preview of all READMEs + repo metadata
**Steps:**
1. Render each README **as GitHub will display it** — Mermaid diagrams rendered, badges resolved, callout admonitions, cards. Options: an `html-anything` page bundling all five, or per-README preview. Include each repo's proposed GitHub **`description` + `topics`** as an "About" card.
2. Present to the user via the preview/visual tools.
**Verify:** user explicitly signs off. **No PR merges and no Phase 6 actions before this sign-off.**

---

## Phase 6 — Staged outward-facing checklist (run ONLY on explicit approval)

Present as a single checklist; execute item-by-item on the user's go.

### Task 6.1: GitHub repo rename + remote
```bash
gh repo rename copydesk --repo TimSimpsonJr/prose-craft
git -C prose-craft remote set-url origin https://github.com/TimSimpsonJr/copydesk.git
```
Then rename the **local dir** `prose-craft` → `copydesk`.

### Task 6.2: Per-repo GitHub description + topics
```bash
gh repo edit TimSimpsonJr/magpie     --description "<convention>" --add-topic foia --add-topic osint --add-topic journalism --add-topic claude-code
gh repo edit TimSimpsonJr/researcher --description "<convention>" --add-topic osint --add-topic obsidian --add-topic claude-code --add-topic web-research
gh repo edit TimSimpsonJr/librarian  --description "<convention>" --add-topic obsidian --add-topic notes --add-topic claude-code --add-topic knowledge-management
gh repo edit TimSimpsonJr/copydesk   --description "<convention>" --add-topic writing --add-topic editing --add-topic claude-code --add-topic ai-detection
gh repo edit TimSimpsonJr/fieldwork-plugins --description "Fieldwork — an investigative plugin suite for Claude Code." --add-topic claude-code --add-topic osint --add-topic journalism --add-topic foia
```
(Optionally upload social-preview images — future.)

### Task 6.3: Delete Dossier (bundle already made in Task 0.2)
```bash
rm -rf "/c/Users/tim/OneDrive/Documents/Projects/dossier"
```

### Task 6.4: File the worked-example future issue
```bash
gh issue create --repo TimSimpsonJr/fieldwork-plugins \
  --title "Add an end-to-end worked example (FOIA PDF → sourced memo)" \
  --body "Thread Researcher → Magpie → Librarian → Copydesk over a real example. Needs a real dataset/run." \
  --label design-input-needed
```

### Task 6.5: Open + merge PRs (merge commits)
For each repo: `gh pr create` then, after the Phase 5 sign-off, `gh pr merge --merge`. Rewrite each `MANIFEST.md` to budget as part of its PR (already done in Phase 1/2).

---

## Acceptance criteria (final)
- All 5 READMEs follow the template; descriptions follow the convention; "Research"/"Prose Craft"/"Scribe" appear nowhere in-scope.
- Each README renders correctly on GitHub in the Phase 5 preview; user signed off.
- Copydesk verify gate (Task 3.5) green; zero in-scope `prose-craft`; learning data + registers preserved.
- Python 3.12 documented uniformly.
- Dossier archived + removed; worked-example issue filed.
- No outward-facing action ran without explicit approval.
