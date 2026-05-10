# VBA Excel Module Sync — Custom Skill

## Purpose
Manage VBA module synchronization between source files (.bas/.frm/.cls) and a running Excel workbook without opening/closing the application repeatedly.

## Workflow

### 1. Acquire Running Excel Instance
```powershell
# Try to get existing Excel instance first
$excel = $null
try {
    $excel = [Runtime.Interopservices.Marshal]::GetActiveObject("Excel.Application")
    Write-Host "Using RUNNING Excel instance"
} catch {
    $excel = New-Object -ComObject Excel.Application
    Write-Host "Started NEW Excel instance"
}
$excel.Visible = $false
$excel.DisplayAlerts = $false
$excel.AutomationSecurity = 3  # Disable macros on open
$excel.EnableEvents = $false
```

### 2. Open Workbook Once
```powershell
$wb = $excel.Workbooks.Open($xlsmPath, $false, $false)
# Do ALL operations while workbook is open
```

### 3. Import Strategy
- **ThisWorkbook/Sheet modules** — These are "Document" types (Type 100). You CANNOT remove them. Instead, replace their code content directly via `CodeModule.ReplaceLine()` or `CodeModule.DeleteLines()` + `CodeModule.AddFromString()`.
- **Standard modules (.bas)** — Remove existing → Import new
- **Class modules (.cls)** — Remove existing → Import new
- **UserForms (.frm)** — Remove existing → Import new

### 4. Clean Dead Code
Remove: Module1, mod_StockEntry_Logic_Enhanced, mod_TestHarness, frmSystemLog, frmStockEntry_Enhanced

### 5. Verify
Count components, sum lines, check for missing references

### 6. Save & Release
```powershell
$wb.Save()
$wb.Close($false)
$excel.Quit()
[Runtime.Interopservices.Marshal]::ReleaseComObject($excel)
[System.GC]::Collect()
```

## Critical Rules
1. **NEVER open/close Excel per module** — do everything in one session
2. **ThisWorkbook is a Document type** — cannot be removed, must replace code inline
3. **Sheet code modules** — same as ThisWorkbook, they're Document types
4. **Always use Try/Catch** — COM errors are common
5. **Release COM objects** — prevent orphaned Excel.exe processes
