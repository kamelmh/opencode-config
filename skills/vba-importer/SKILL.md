# VBA Lifecycle Manager

## Description
A comprehensive suite of skills for managing the ERP Académie VBA project. Handles imports, exports, backups, dependency checks, smoke tests, AI-assisted optimization, documentation, and automated testing.

## Path Configuration
- **Source Modules:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\VBA_Modules\*.bas`
- **Source Workbook:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\Decision_Support_System.xlsm`
- **Temp Workspace:** `$env:TEMP\VBA_Import_Work\`
- **Deploy Target:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\ERP_Academie_v13.2_FIXED.xlsm`
- **Backup Folder:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\Backups\`

---

## 1. Import & Rebuild (`import modules`, `refresh vba`, `rebuild excel`)
**When to use:** When source `.bas` files have been updated and need to be pushed into Excel.
**Workflow:**
1. **Kill Processes:** Terminate `excel.exe`, `OneDrive.exe`, and `Dropbox.exe` to release file locks.
2. **Prepare Workspace:** Copy the source workbook to the Temp Workspace.
3. **Rebuild:**
   - Open workbook via COM.
   - Remove all existing standard modules (Type 1).
   - Import every `.bas` file from Source Modules.
   - **Auto-Open VBA Editor** using `Application.VBE.MainWindow.Visible = True`.
   - Save and close.
4. **Deploy:** Copy the rebuilt workbook to Deploy Target, unblock it, and launch it.

---

## 2. Export (`export vba`, `sync changes`, `save code to disk`)
**When to use:** When the user has made changes directly in the VBA Editor and wants to preserve them to the local `.bas` files.
**Workflow:**
1. Attach to running Excel instance.
2. Identify active workbook.
3. Loop through all `VBComponents` of Type 1.
4. Export each using `component.Export("path\filename.bas")`.
5. Clean up: Remove `Attribute VB_Name` lines if they cause duplicates (optional, usually safe to keep).
6. Confirm: Print list of updated `.bas` files.

---

## 3. Backup (`vba backup`, `snapshot`, `safe point`)
**When to use:** Before major refactors or when the user says "backup now".
**Workflow:**
1. Ensure Backup Folder exists.
2. Generate timestamp: `YYYYMMDD_HHMM`.
3. Copy source workbook to `Backups\ERP_v13.2_backup_YYYYMMDD_HHMM.xlsm`.
4. Verify file size matches original.
5. Report: "Backup created at [Path]".

---

## 4. Reference Check (`check references`, `fix missing libs`, `check deps`)
**When to use:** When "User-defined type not defined" errors occur.
**Workflow:**
1. **Scan Source:** Grep `.bas` files for common library signatures:
   - `Scripting.Dictionary` -> Needs **Microsoft Scripting Runtime** (`{420B2830-E718-11CF-893D-00A0C9054228}`)
   - `FileSystemObject` -> Needs **Microsoft Scripting Runtime**
   - `MSXML2.*` -> Needs **Microsoft XML, v6.0** (`{F5078F18-C551-11D3-89B9-0000F81FE221}`)
   - `MSForms.*` -> Needs **Microsoft Forms 2.0 Object Library**
2. **Auto-Fix:**
   - Open workbook via COM.
   - Add missing references via `wb.VBProject.References.AddFromGuid(...)`.
   - Save and report changes.

---

## 5. Smoke Test (`smoke test`, `verify import`, `quick check`)
**When to use:** Immediately after an import to ensure compilation and basic runtime logic.
**Workflow:**
1. Open workbook in Temp Workspace via COM.
2. **Run Test:** Execute a known-safe procedure (e.g., `mod_Config.SYS_TITLE` or a dummy macro `TempCompileCheck`).
3. **Report:**
   - If success: "Smoke test passed."
   - If error: Print the exact error message and the failing line/module.

---

## 🤖 AI-Assisted Commands

## 6. Compile & Fix Loop (`compile & fix loop`, `auto-fix compile`, `compile loop`)
**When to use:** When there are compilation errors and you want AI to automatically find and fix them.
**Workflow:**
1. Import modules into Temp Workspace.
2. Run a compilation check via a temporary macro that catches `Err.Number` on `Debug.Compile`.
3. If an error occurs, capture the error message and line number.
4. Locate the corresponding `.bas` file and line.
5. AI analyzes the error and applies a fix (e.g., `MSForms.ReturnInteger` -> `Integer`).
6. Re-import and repeat up to 5 times or until clean.
7. Deploy the clean version.

---

## 7. Find Dead Code (`find dead code`, `clean up`, `orphan check`)
**When to use:** To identify unused procedures and reduce bloat.
**Workflow:**
1. Grep all `.bas` files to build an index of all defined `Sub` and `Function`.
2. Search for references to each name across all other files (ignoring the definition itself).
3. Report any procedure with zero references as "Orphaned / Potentially Dead".

---

## 8. Map Dependencies (`map dependencies`, `show graph`, `impact analysis`)
**When to use:** Before changing a core module to understand what might break.
**Workflow:**
1. Scan all `.bas` files for `mod_` prefixes, `Public` calls, and `Application.Run`.
2. Build a dependency matrix (Module A calls Module B).
3. Output a text-based graph or Mermaid diagram.

---

## 9. Localization Audit (`localization audit`, `check hardcoded strings`, `localize strings`)
**When to use:** To ensure no hardcoded strings break multi-language support.
**Workflow:**
1. Grep for string literals (e.g., `"Bon de Sortie"`) in `.bas` files.
2. Flag any that are not already in `mod_Localization` or using `Chr()` for accents.
3. Offer to migrate them to `mod_Config` or `mod_Localization`.

---

## 10. Constants Sweep (`constants sweep`, `centralize constants`, `hardcode check`)
**When to use:** To find hardcoded values that should be in `mod_Config`.
**Workflow:**
1. Scan `.bas` files for repeated string literals (like `"MOUVEMENTS"`, `"ARTICLES"`) and magic numbers (like `250`, `176`).
2. Cross-reference with existing `mod_Config` constants.
3. Report any value that is hardcoded but should be a constant.

---

## 📊 Documentation & QA

## 11. Generate Docs (`generate docs`, `create docs`, `api reference`)
**When to use:** To create a Markdown reference for the entire codebase.
**Workflow:**
1. Scan all `.bas` files for `Public Sub` and `Public Function`.
2. Extract signatures, parameters, and comment blocks immediately above them.
3. Write `API_Reference.md` into the project root.

---

## 12. Check Sheet Refs (`check sheet refs`, `verify sheets`, `sheet mismatch check`)
**When to use:** When you get "Sheet not found" errors.
**Workflow:**
1. Extract all sheet names from the open workbook.
2. Scan `.bas` files for `Sheets("...")` calls.
3. Compare and report any calls referencing sheets that don't exist.

---

## 13. Performance Audit (`performance audit`, `optimize vba`, `speed check`)
**When to use:** To identify slow VBA patterns.
**Workflow:**
1. Scan for common anti-patterns:
   - Missing `Application.ScreenUpdating = False`.
   - Cell-by-cell loops instead of array reads.
   - `Select` / `Activate` usage.
2. Report specific lines and suggest optimized replacements.

---

## 🧪 Testing

## 14. Run Tests (`run tests`, `test suite`, `execute tests`)
**When to use:** To run any procedures named `Test_*` or `UnitTest_*`.
**Workflow:**
1. Open workbook via COM.
2. Discover all procedures matching `Test_*`.
3. Execute them one by one.
4. Capture `Debug.Print` output and report Pass/Fail.

---

## 15. Event Audit (`event audit`, `check events`, `wire check`)
**When to use:** To ensure UI buttons and events are properly connected.
**Workflow:**
1. Check for standard event signatures (`Workbook_Open`, `UserForm_Initialize`).
2. Verify that buttons on forms (if accessible via metadata) have matching click handlers.
