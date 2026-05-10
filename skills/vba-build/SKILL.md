# VBA Build Skill — ERP Académie v13.2

## Purpose
Automated VBA module synchronization, compilation verification, and workbook rebuild from source files (.bas/.frm/.cls). Solves the "stale p-code cache" problem that causes COM to report compile OK while Excel UI shows errors.

## File Locations
- **Master Workbook:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\ERP_Academie_v13_Master.xlsm`
- **Source Directory:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\VBA_Modules\`
- **Output File:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\ERP_Academie_v13_2.xlsm`
- **Build Script:** `C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\build.ps1`

## Triggers
- `build vba`, `rebuild workbook`, `compile vba`, `import modules`, `sync vba`, `refresh excel`, `vba build`

## Critical Rules

### 1. ALWAYS REBUILD FROM SCRATCH
Never import into an existing workbook. The VBA p-code cache gets corrupted and shows false compile errors.
```
Master → Strip ALL modules → Import source → Compile → Save AS NEW file
```

### 2. STRIP EVERYTHING EXCEPT SHEET MODULES
Only keep Document type modules (Type=100): ThisWorkbook, Sheet modules.
Remove: ALL standard modules (.bas), class modules (.cls), UserForms (.frm).

### 3. IMPORT ORDER MATTERS
1. Import .bas files (skip .bak files)
2. Import .frm files
3. Inject ThisWorkbook code (DON'T import .cls — inject into existing document module)

### 4. ENCODING MUST BE UTF-8 WITHOUT BOM
VBA's Import method fails to read `Attribute VB_Name` if a BOM prefix is present, causing generic Module* names.
```powershell
# Check for BOM
$bytes = [System.IO.File]::ReadAllBytes($file)
if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "BOM detected - removing"
}
```

### 5. LINE ENDINGS MUST BE CRLF
VBA import fails with LF-only files.

### 6. Sub/End MISMATCHES BREAK EVERYTHING
`Public Sub Name()` must end with `End Sub`, NOT `End Function`. A single mismatch breaks the entire module and makes procedures after it unrecognizable.

### 7. mod_Config MUST BE DEFINED BEFORE OTHER MODULES USE IT
All `mod_Config.SHEET_*`, `mod_Config.MASTER_PWD`, `mod_Config.APP_VERSION` references must have corresponding definitions in mod_Config.bas.

## Build Workflow

### Step 1: Kill Excel
```powershell
Get-Process -Name "EXCEL" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 3
```

### Step 2: Copy Master as Base
```powershell
Copy-Item $master $tempBase -Force
```

### Step 3: Open and Strip
```powershell
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$excel.AutomationSecurity = 1
$excel.ScreenUpdating = $false
$excel.EnableEvents = $false

$wb = $excel.Workbooks.Open($tempBase, 0, $false)

# Strip ALL non-sheet modules
foreach ($comp in @($wb.VBProject.VBComponents)) {
    if ($comp.Type -ne 100) {
        try { $wb.VBProject.VBComponents.Remove($comp) } catch {}
    }
}
```

### Step 4: Import Source
```powershell
# .bas files (skip .bak)
foreach ($f in (Get-ChildItem "$srcDir\*.bas" -File | Where-Object { $_.Name -notmatch "\.bak" })) {
    try { $wb.VBProject.VBComponents.Import($f.FullName) | Out-Null }
    catch { Write-Host "FAIL: $($f.Name)" }
}

# .frm files
foreach ($f in (Get-ChildItem "$srcDir\*.frm" -File)) {
    try { $wb.VBProject.VBComponents.Import($f.FullName) | Out-Null }
    catch { Write-Host "FAIL: $($f.Name)" }
}

# Inject ThisWorkbook
$twCode = [System.IO.File]::ReadAllText("$srcDir\ThisWorkbook.cls") -replace 'Attribute VB_Name = "ThisWorkbook"\r?\n', ''
$twComp = $wb.VBProject.VBComponents.Item("ThisWorkbook")
$twComp.CodeModule.DeleteLines(1, $twComp.CodeModule.CountOfLines)
$twComp.CodeModule.AddFromString($twCode)
```

### Step 5: Compile
```powershell
$excel.VBE.CommandBars("Menu Bar").Controls("Debug").Controls("Compile VBAProject").Execute()
```

### Step 6: Save as NEW File
```powershell
if (Test-Path $target) { Remove-Item $target -Force }
$wb.SaveAs($target, 52)  # xlOpenXMLWorkbookMacroEnabled
```

### Step 7: Cleanup
```powershell
$wb.Close($false)
$excel.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel)
```

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Sub or Function not defined" | Stale p-code cache | REBUILD from scratch (don't import into existing) |
| "Method or data member not found" | Sub/End mismatch or missing constant | Check Sub/End pairs, verify mod_Config constants |
| "User-defined type not defined" | UDT declared after procedures | Move `Public Type` before first Sub/Function |
| "Cannot overwrite item with itself" | Trying to save to same path | Delete target file first |
| "Unable to get the Copy property" | Sheet copy with wrong parameters | Use `$ws.Copy($null, $wb.Sheets($wb.Sheets.Count))` |
| Compile OK but errors in Excel | p-code cache corruption | New filename forces fresh cache |

## Post-Build Verification
```powershell
# Verify file exists and has content
$fi = Get-Item $target
Write-Host "Size: $($fi.Length) bytes, Modified: $($fi.LastWriteTime)"

# Open and verify key modules
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$excel.AutomationSecurity = 1
$excel.EnableEvents = $false
$excel.ScreenUpdating = $false

$wb = $excel.Workbooks.Open($target, 0, $false)
$mc = $wb.VBProject.VBComponents.Item("mod_Config")
$se = $wb.VBProject.VBComponents.Item("mod_SharedEnvironment")
Write-Host "mod_Config: $($mc.CodeModule.CountOfLines) lines"
Write-Host "mod_SharedEnvironment: $($se.CodeModule.CountOfLines) lines"

$wb.Close($false)
$excel.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel)
```

## Quick Command
The build script at `$srcDir\build.ps1` does all of this automatically:
```powershell
& "C:\Users\Administrator\Dropbox\Logistics.Public.Sector.Refactor\Software_Surgical_Edit\build.ps1"
```
