---
description: Ingest a raw source into the LLM Wiki
agent: build
---

Ingest the source passed by the user into the LLM Wiki.

Steps:

1. Read the source path from the user message.
2. Treat the raw source as immutable.
3. Create or update a source page under `wiki/sources/`.
4. Update relevant entity and concept pages.
5. Update `wiki/index.md`.
6. Append an entry to `wiki/log.md`.
7. Report changed files and uncertainties.