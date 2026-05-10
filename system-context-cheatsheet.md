# System Context Cheatsheet — Academix v13.2

Consolidated reference for: Prompt Context | VBA Logic | Prose Quality

---

## 1. SYSTEM PROMPT CONTEXT

### Context Injection (from `context-injection` skill)
| Principle | Rule |
|-----------|------|
| **Placement** | Most critical context goes **near the query** (recency bias) or **at prompt start** |
| **Token budget** | 10-15% system instructions, 50-70% injected context, 5-10% history, 15-25% response |
| **Delimiters** | Use XML tags or markdown fences to separate context from instructions |
| **Labels** | Label each block: `<code_file path="...">`, `<user_profile>`, `<retrieved_document>` |
| **Few-shot** | 2-3 examples after system prompt, before query |
| **Don't embed instructions in context** | Keep rules in system prompt, data in context blocks |

### Skill Loading Protocol (from AGENTS.md)
```
build  agent → vba-build, vba-debug, vba-excel-sync, naming-cheatsheet
debug  agent → vba-debug, vba-build
plan   agent → plan, planning-and-task-breakdown, idea-refine
audit  agent → verify
test   agent → project, verify
```

### Commit Protocol (from `conventional-commit` skill)
```
<type>[scope]: <imperative description>

- bullet list of specific changes
- what + why, not just how
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

---

## 2. VBA LOGIC & PATTERNS

### VBA Naming Conventions (adapted from `naming-cheatsheet`)
| Pattern | VBA Example | Notes |
|---------|-------------|-------|
| Module prefix | `mod_` | Standard modules: `mod_Config`, `mod_StockEngine` |
| Form prefix | `frm_` | UserForms: `frm_StockEntry`, `frm_Login` |
| Class prefix | `cls_` | Class modules |
| Boolean prefix | `b_` / `bln` | `b_HasData`, `blnIsValid` |
| Long prefix | `l_` / `lng` | `l_RowCount` |
| String prefix | `s_` / `str` | `s_UserName` |
| Double prefix | `d_` / `dbl` | `d_TotalAmount` |
| Public Const | `UPPER_SNAKE` | `MASTER_PWD`, `APP_VERSION`, `SHEET_NAME` |
| Procedure | `PascalCase` | `Sub CalculateEOQ()`, `Function GetROP() As Double` |
| Event handler | `Object_Event` | `Worksheet_Change`, `UserForm_Initialize` |
| Sheet code name | `ws_` prefix | `ws_Articles`, `ws_Fournisseurs` |

### VBA Critical Rules (from `vba-build` skill)
1. **Always rebuild from scratch** — Master → Strip → Import → Compile → Save As
2. **Strip ALL non-sheet modules** — Keep only Type=100 (ThisWorkbook, sheets)
3. **Import order**: .bas files first, then .frm, then inject ThisWorkbook
4. **UTF-8 WITHOUT BOM** — BOM breaks `Attribute VB_Name` parsing
5. **Line endings must be CRLF** — LF-only fails VBA import
6. **Sub/End mismatch** — `End Function` where `End Sub` expected breaks module
7. **`Public Const` before procedures** — Const after `End Sub` causes "data member not found"
8. **Cross-module Const** — Use `Property Get` instead of `Public Const` across modules

### VBA Debug Patterns (from `vba-debug` skill)
| Error | Fix |
|-------|-----|
| Syntax error on same line as comment | Add newline after `End Function/Sub/Property` |
| UTF-8 em dashes `—`/`–` | Replace with `-` |
| `Public Const` after `End Sub` | Move Const before all procedures |
| Stale p-code cache | **Rebuild from scratch** (never trust .xlsm directly) |
| UDT not defined | Move `Type` before first `Sub/Function` |
| `Property Get` cross-module | Replace `Public Const` with `Property Get` for shared constants |

### VBA Build Pipeline
```powershell
build.ps1      # Kill Excel → Copy Master → Strip → Import → Compile → Save
verify.ps1     # 97-point verification (structure, security, data, call graph, compliance)
test-macro.ps1 # Automated macro test with Interactive=False
vbe.ps1        # VBE control suite
dss-audit.ps1  # 5-phase audit
```

### VBA Anti-Slop Rules (from `ai-slop-cleaner`)
1. **Dead code deletion** — Remove unused modules, procedures, variables
2. **Duplicate removal** — Consolidate repeated logic into shared helpers
3. **Naming cleanup** — Fix Hungarian notation, PascalCase procedures, UPPER_SNAKE constants
4. **Test reinforcement** — Lock behavior before refactoring
5. **No wrappers** — Avoid needless abstraction layers in VBA (no inheritance, no interfaces)

---

## 3. PROSE TECHNIQUES

### Humanizer Anti-Patterns (from `humanizer` skill)

| Category | Words/Patterns to Avoid | Fix |
|----------|------------------------|-----|
| Significance inflation | stands/serves as, testament, pivotal, underscore, vital role | Delete — state facts directly |
| -ing fake depth | highlighting, ensuring, reflecting, showcasing | Rewrite without participle |
| Promotional | boasts, vibrant, rich, nestled, groundbreaking, stunning | Replace with neutral description |
| Vague attribution | "Industry reports", "Experts argue", "Some critics" | Cite specific source or remove |
| AI vocabulary | Additionally, crucial, delve, enhance, foster, garner, intricate, landscape (abstract) | Use simpler alternatives |
| Copula avoidance | serves as, stands as, marks, represents, boasts | Use "is", "are", "has" |
| Negative parallelism | "Not only...but...", "It's not just about..." | Direct statement |
| Rule of three | 3-item lists for completeness | Single best example |
| Em dash overuse | — More than one per paragraph | Use commas or periods |
| Filler phrases | "In order to", "Due to the fact", "At this point in time" | Delete — direct speech |
| Hedging | "could potentially possibly be argued that... might have" | Be direct |
| Generic positive close | "The future looks bright", "Exciting times ahead" | Delete or state specific plan |
| Chatbot artifacts | "I hope this helps!", "Let me know if...", "Certainly!" | Delete |

### Quick Prose Checklist
1. No em dashes (use commas)
2. No "-ing" fake depth sentences
3. No "Not only X, but Y" constructions
4. No "serves as/stands as/boasts" — use "is/has"
5. No vague attributions without sources
6. No "Additionally" or "crucial" or "delve"
7. No rule-of-three lists
8. No chatbot pleasantries
9. No generic positive endings
10. Vary sentence length naturally

---

## 4. FILE REFERENCE (Key Paths)

| Path | Description |
|------|-------------|
| `C:\Users\Administrator\.config\opencode\AGENTS.md` | Agent config, model routing, bootstrap protocol |
| `C:\Users\Administrator\.config\opencode\instructions.md` | Auto-loaded full project context |
| `C:\Users\Administrator\.config\opencode\opencode.json` | API keys, provider config |
| `C:\Users\Administrator\.opencode\notepad.md` | Session memory, task tracking |
| `C:\Users\Administrator\.opencode\model-landscape-2026.md` | Model landscape & recommendations |
| `C:\Users\Administrator\.opencode\system-context-cheatsheet.md` | **This file** |
| `Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\VBA_Modules\` | VBA source (.bas/.frm/.cls) |
| `Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\build.ps1` | Build pipeline |
| `Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\verify.ps1` | 97-point verification |
| `Dropbox\Logistics.Public.Sector.Refactor\.opencode\bootstrap\MASTER_BOOTSTRAP.xml` | Uber-context |
| `Desktop\handoff*.txt` | VBA debug handoff files |
