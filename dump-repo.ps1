<#
    Dump repo source files ( *.py, *.yml, *.yaml, Dockerfile, Makefile )
    into one UTF‑8 text file with “### path” headers.
#>

param(
    [string]$RepoRoot = "$PSScriptRoot",                     # default: script’s dir
    [string]$OutFile  = "$PSScriptRoot\repo_dump.txt"
)

# ── 0.  fresh output ────────────────────────────────────────────────────────────
if (Test-Path $OutFile) { Remove-Item $OutFile -Force }

# ── 1.  collect wanted files ───────────────────────────────────────────────────
$wantExt  = @('.py', '.yml', '.yaml')
$wantName = @('Dockerfile', 'Makefile')

$files =
    Get-ChildItem -Path $RepoRoot -Recurse -File |
    Where-Object {
        $wantExt -contains $_.Extension.ToLower() -or
        $wantName -contains $_.Name
    } |
    Sort-Object FullName

# ── 2.  write them into a single dump ──────────────────────────────────────────
foreach ($f in $files) {
    # relative path by string slicing (works everywhere)
    $relPath = $f.FullName.Substring($RepoRoot.Length).TrimStart('\','/')
    
    Add-Content -Path $OutFile -Value "### $relPath"
    Add-Content -Path $OutFile -Value (Get-Content -Path $f.FullName -Raw)
    Add-Content -Path $OutFile -Value "`r`n"  # blank line separator
}

Write-Host "Dumped $($files.Count) files → $OutFile"
