# VBA Debug Skill — ERP Académie v13.2

## Purpose
End-to-end automated VBA error resolution: test macro → capture error → diagnose → fix source → rebuild → verify → report. No human interaction needed until the final handoff.

## Triggers
`check handoff`, `handoff`, `vba error`, `compile error`, `syntax error`, `debug vba`, `fix vba`, `next error`, `test macro`

## File Locations
- **Handoff Directory:** `C:\Users\Administrator\Desktop\`
- **Handoff Pattern:** `handoff*.txt` or `HANDOFF*.txt`
- **Master Workbook:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\ERP_Academie_v13_Master.xlsm`
- **Source Directory:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\VBA_Modules/`
- **Output File:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\ERP_Academie_v13_2.xlsm`
- **Build Script:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\build.ps1`
- **Verify Script:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\verify.ps1`
- **Test Script:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\test-macro.ps1`

## Workflow (ALWAYS follow this order)

### Step 1: Run the test script (automated)
```powershell
& "C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\test-macro.ps1"
```
This kills Excel → opens workbook with `Interactive=False` (all dialogs auto-dismissed) → runs macro → captures result → saves log.

### Step 2: If test fails, check for handoff
If the automated test reports failure, the user must provide the highlighted VBA code:
```powershell
Get-ChildItem "C:\Users\Administrator\Desktop\handoff*.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```
Read the latest handoff file. It contains the highlighted VBA code.

### Step 3: Diagnose the error type
| Error Pattern | Root Cause | Fix |
|--------------|------------|-----|
| Syntax error | `End Function` on same line as comment | Add newline after `End Function/Sub/Property` |
| Syntax error | UTF-8 em dashes `—` become `"` in VBA | Replace `—`/`–` with `-` in source |
| Method/data member not found | `Public Const` after `End Sub` | Move `Const` before all procedures |
| Method/data member not found | `Public Const` not resolved across modules | Convert to `Property Get` |
| Sub/Function not defined | Stale p-code cache | REBUILD from scratch via build.ps1 |
| User-defined type not defined | UDT declared after procedures | Move `Type` before first Sub/Function |
| 0x800A9C68 | VBA runtime error — check VBE for highlighted line | Requires user handoff |

### Step 4: Fix the source file
Apply the fix to the correct `.bas` file in `VBA_Modules/`.

### Step 5: Rebuild
```powershell
& "C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\build.ps1"
```

### Step 6: Verify
```powershell
& "C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\verify.ps1"
```

### Step 7: Test the macro
```powershell
& "C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\test-macro.ps1"
```

### Step 8: Report
Output a concise summary:
```
Fix: <what was wrong> -> <what changed>
File: <source file path>
Build: COMPILE OK / FAIL
Verify: 97/97 PASS / FAIL
Macro: SUCCESS / FAILED
Status: SAFE TO OPEN / DO NOT OPEN
```

## Critical Rules

### 1. NEVER fix the .xlsm directly
Only edit source `.bas`/`.frm`/`.cls` files in `VBA_Modules/`.

### 2. `Application.Interactive = False` is the key
In test-macro.ps1, setting `Interactive = false` before running macros auto-dismisses ALL MsgBox/InputBox dialogs. MsgBox returns `vbOK` automatically. This is what makes the pipeline work without human interaction.

### 3. UTF-8 WITHOUT BOM is mandatory
After any edit, verify no BOM prefix exists.

### 4. Em dashes are poison
Always scan for `—` (U+2014) and `–` (U+2013) in `.bas` files and replace with `-`.

### 5. Const ordering in mod_Config
ALL `Public Const` must appear BEFORE any `Property Get`, `Sub`, or `Function`.

### 6. Popups during startup
Use `Optional ByVal silent As Boolean = False` pattern for any subroutine that shows MsgBox during `Workbook_Open`.

## Known Fixes Applied
- mod_Config: `MASTER_PWD` → `Property Get` (runtime-safe)
- mod_Config: All `Const` moved before `Property Get` procedures
- mod_StockEngine: `UpdateAllABCClassifications(silent:=True)`
- mod_Utilities: `RestoreMouvementsHeaders(silent:=True)`
- mod_Utilities: `End Function` on its own line (line 107)
- mod_DemoData: MsgBox suppressed for COM testing
- All `.bas` files: Em dashes `—` replaced with hyphens `-`
