---
description: Health-check the LLM Wiki
agent: build
---

Lint the LLM Wiki.

Check for:

- broken links;
- orphan pages;
- missing frontmatter;
- missing source references;
- contradictions;
- stale claims;
- index/log inconsistency.

Run `python3 core/scripts/check_wiki.py .` if available, then add semantic findings.