# VBE Auto — Universal VBA Control Skill

Automated Excel VBE control for any VBA project. Provides full lifecycle management: session control, module import/export, compilation, macro execution, verification, and build automation.

## When to Use

- User asks to **build/rebuild** an Excel VBA project from source files
- User asks to **test/verify** VBA macros or compilation
- User asks to **import/export** VBA modules
- User asks to **debug** VBA compile/runtime errors
- User asks for **full VBE session control** (open workbook, run macros, inspect sheets)
- User asks to **automate** Excel VBA tasks via COM

## Project Discovery

On first load, scan for `vbe-auto-config.json` in:
1. Current working directory
2. `C:\Users\Administrator\Desktop\vbe-auto\config.json` (default toolkit)
3. Ask user to provide workbook path if not found

### Config Schema (`vbe-auto-config.json`)

```json
{
  "project_name": "Project Name",
  "version": "v1.0",
  "master_workbook": "path/to/Master.xlsm",
  "output_workbook": "path/to/Output.xlsm",
  "vba_source_dir": "path/to/VBA_Modules/",
  "thisworkbook_source": "path/to/ThisWorkbook.cls",
  "verification": {
    "expected_sheets": ["Sheet1", "Sheet2"],
    "expected_modules": ["mod_Config", "mod_Engine"],
    "expected_constants": [
      { "name": "VERSION", "value": "v1.0" }
    ]
  },
  "protection": {
    "sheet_password": "password",
    "vba_project_password": null
  },
  "macros": {
    "startup": ["InitProject", "LoadDefaults"],
    "test_all": ["TestSuite"]
  }
}
```

## Workflow

### 1. BUILD (Source → Workbook)

```
Kill Excel → Open MASTER → Strip all user modules → Import .bas/.frm/.cls → Inject ThisWorkbook → Compile → Save as output
```

Always use this protocol. **Never** manually import into existing workbook — p-code cache corrupts.

### 2. VERIFY (Workbook → Report)

```
Open via COM → Check file integrity → Compile check → Module inventory → Sheet verification → Constants validation → Cross-module safety → Report
```

### 3. TEST (Macros → Results)

```
Open via COM → Set Interactive=False → Run each macro → Capture result/timing → Report pass/fail
```

### 4. DEBUG (Error → Fix → Rebuild)

```
User provides handoff file (highlighted code) → Diagnose → Fix source .bas → Rebuild → Verify → Report
```

## Available Tools

### vbe.ps1 — VBE Control Suite
Full interactive VBE session management.

**Commands:**
- `vbe open` — Open workbook with full COM control
- `vbe close` — Close Excel session cleanly
- `vbe save` — Save current workbook
- `vbe compile` — Compile VBA project
- `vbe macro <Name>` — Run a macro
- `vbe macro-all` — Test all macros
- `vbe modules` — List all modules with line counts
- `vbe module-read <Name>` — Read module code
- `vbe export-all` — Export all modules to folder
- `vbe sheets` — List sheets with dimensions
- `vbe sheet <Name>` — Inspect sheet content
- `vbe snapshot` — Session state snapshot
- `vbe log` — Show recent operations log
- `vbe state` — Load last saved state

### build.ps1 — Automated Build
```powershell
& build.ps1                                           # Use default config
& build.ps1 -ConfigPath "path/to/config.json"         # Custom config
& build.ps1 -Master "master.xlsm" -Source "VBA_Modules/" -Output "output.xlsm"
```

### verify.ps1 — Verification Suite
```powershell
& verify.ps1                                          # Use default config
& verify.ps1 -Workbook "path/to.xlsm"
& verify.ps1 -ConfigPath "path/to/config.json"
```

## Critical Rules

1. **NEVER** manually import .bas into existing workbook — always use rebuild script
2. **ALWAYS** use `Interactive=False` for COM automation (auto-dismisses dialogs)
3. **ALWAYS** use `DisplayAlerts=False` for unattended operations
4. **ALWAYS** release COM objects: `[System.Runtime.Interopservices.Marshal]::ReleaseCOMObject($xl)`
5. **ALWAYS** set `EnableEvents=False` during module strip/import to prevent Workbook_Open triggers
6. **NEVER** modify .xlsm directly — fix source files, then rebuild
7. **ALWAYS** kill existing Excel processes before build to prevent file locks

## Error Handling

### Common VBA Import Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Syntax error" at End Sub | UTF-8 em dash (—) in comment | Replace with ASCII hyphen (-) |
| "Expected: identifier" | BOM in .bas file | Save as UTF-8 WITHOUT BOM |
| "Method or data member not found" | Const after procedure | Move all Const before Sub/Function |
| "Compile error" after import | Stale p-code cache | Full rebuild (kill → strip → import) |
| "Object required" | Sheet not found | Check sheet name matches config |

### Debug Handoff Protocol

1. User copies highlighted code from VBE → saves to `Desktop\handoffN.txt`
2. AI reads handoff, diagnoses error type
3. AI fixes source `.bas` in `VBA_Modules/`
4. AI runs `build.ps1` to rebuild
5. AI runs `verify.ps1` to validate
6. AI reports: Fix applied, Build OK, Safe to open

## Architecture Patterns

### Module Tier System
```
TIER 1: Foundation (mod_Config, mod_Utilities) — no dependencies
TIER 2: Core Engine (mod_StockEngine, mod_Database) — depends on T1
TIER 3: Business Logic (mod_*Entry, mod_*Report) — depends on T1+T2
TIER 4: UI/Presentation (mod_*Export, mod_*Dashboard) — depends on T1+T2+T3
TIER 5: Entry Points (MAIN_MACROS, ThisWorkbook, Forms) — depends on all
```

### Sheet Protection Pattern
```vba
ws.Unprotect Password:=mod_Config.MASTER_PWD
' ... operations ...
ws.Protect Password:=mod_Config.MASTER_PWD, UserInterfaceOnly:=True
```

### Session-Aware User Tracking
```vba
userName = mod_SharedEnvironment.GetCurrentUserName
If Len(userName) = 0 Then userName = Environ("USERNAME")  ' Fallback
```

## Security Guidelines

- Sheet passwords stored as Property Get, not Public Const
- Audit logging always active — LogAction for all operations
- User input validated before sheet writes
- Transaction safety: BeginTransaction → operations → CommitTransaction/RollbackTransaction

## Portability

This skill works with ANY VBA project. To deploy for a new project:

1. Copy `vbe-auto/` toolkit to project root
2. Create `vbe-auto-config.json` with project-specific values
3. Ensure source `.bas/.frm/.cls` files are in `vba_source_dir`
4. Run `build.ps1` to generate initial workbook

The skill automatically discovers config and adapts to project structure.
