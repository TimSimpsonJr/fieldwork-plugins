# Fieldwork Plugins

![License](https://img.shields.io/badge/license-MIT-blue) ![Plugins](https://img.shields.io/badge/plugins-4-informational) ![Python](https://img.shields.io/badge/python-3.12-3776AB) ![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-8A3FFC) ![Status](https://img.shields.io/badge/status-beta-orange)

Fieldwork is a suite of Claude Code plugins for investigative work: four tools that carry a story from a raw question to a finished, sourced piece. Research the web, work through the documents, file what you find as linked notes, then write it up in your own voice. Each plugin does one job and hands off cleanly to the next, and any of them works on its own.

It is built for people who end up with more documents than time: journalists, OSINT researchers, and anyone who files public-records requests in service of a bigger story.

## The workflow

**Researcher** → **Magpie** → **Librarian** (the shared notes layer) → **Copydesk**

Researcher and Magpie both file through **Librarian**, the shared notes layer, so a web pass and a document pass land in one consistent, linked set of notes instead of three filing styles. **Copydesk** turns those findings into publishable writing.

## The plugins

### [Researcher](https://github.com/TimSimpsonJr/researcher)
Turns any topic, or a batch of fifty, into cited, cross-linked notes in your Obsidian vault. Confidence-gated web search with source-credibility tiering, and no separate API key to wire up.

### [Magpie](https://github.com/TimSimpsonJr/magpie)
The documents-and-data half. Turn a FOIA release or a messy spreadsheet into findings you can stand behind: counted, cited to the exact page, swept for PII, and checked for bad redactions, all on your own machine.

### [Librarian](https://github.com/TimSimpsonJr/librarian)
The shared output layer. Keeps your Obsidian vault organized: it files findings as classified, tagged, cited notes, placed by your folder conventions and cross-linked with `[[wikilinks]]`, with a full-text index so a second pass updates a note instead of duplicating it. No vault? It writes portable Markdown and CSV instead. Researcher and Magpie both require it, so install it from the same marketplace.

### [Copydesk](https://github.com/TimSimpsonJr/copydesk)
Turns findings into publishable writing in your own voice, with a review gate that catches AI tells and a learning loop that sharpens from your edits.

## Quick start

You need [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and Python 3.12. Add the marketplace, then install whichever plugin you want:

```
/plugin marketplace add TimSimpsonJr/fieldwork-plugins
/plugin install magpie@fieldwork
```

Swap `magpie` for `researcher`, `librarian`, or `copydesk`. Researcher and Magpie both require Librarian (their shared output layer), so install it from the same marketplace too. Each plugin has its own setup step and its own README with the details.

> [!NOTE]
> **What you need:** Claude Code and Python 3.12. The heavier extras (local search, OCR, transcription, entity graphs) are optional and specific to a plugin, and Claude installs them for you when a task needs them. Nothing here needs a separate API key or a paid service.

> [!IMPORTANT]
> **Your data & privacy:** Fieldwork runs locally, inside your own Claude Code session, and your documents and notes stay on your machine. Magpie adds a PII sweep and redaction checks for sensitive material; Librarian and Copydesk run no external service of their own. Each plugin's README spells out exactly what touches the network and what stays local.

## How they fit together

| Plugin | Role | Depends on |
|--------|------|------------|
| [Researcher](https://github.com/TimSimpsonJr/researcher) | gather sources into cited notes | Librarian |
| [Magpie](https://github.com/TimSimpsonJr/magpie) | analyze FOIA/data into findings | Librarian |
| [Librarian](https://github.com/TimSimpsonJr/librarian) | organize findings into your Obsidian vault (shared layer) | none |
| [Copydesk](https://github.com/TimSimpsonJr/copydesk) | write findings up in your voice | none |

This repository is a pure-pointer marketplace: it holds no plugin source, just a manifest pointing at each plugin's own repo. The schema and dependency-resolution details live in [NOTES.md](./NOTES.md).

## License

MIT. Each plugin is MIT-licensed in its own repository.
