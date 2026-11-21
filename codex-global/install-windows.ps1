#requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$UpdateSkills
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$homeDir = [Environment]::GetFolderPath('UserProfile')
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $homeDir '.codex' }
$targetAgents = Join-Path $codexHome 'AGENTS.md'
$skillsRoot = Join-Path (Join-Path $homeDir '.agents') 'skills'
$sourceAgents = Join-Path $root 'GLOBAL_AGENTS.md'
$sourceSkills = Join-Path $root 'skills'
$begin = '<!-- AOS-CODEX-GLOBAL START -->'
$end = '<!-- AOS-CODEX-GLOBAL END -->'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$utf8 = New-Object System.Text.UTF8Encoding($false)

if (-not (Test-Path -LiteralPath $sourceAgents)) { throw "Missing source: $sourceAgents" }
$policy = [System.IO.File]::ReadAllText($sourceAgents)
$block = $begin + "`n" + $policy.TrimEnd() + "`n" + $end
$current = if (Test-Path -LiteralPath $targetAgents) { [System.IO.File]::ReadAllText($targetAgents) } else { '' }
$hasBegin = $current.Contains($begin)
$hasEnd = $current.Contains($end)
if ($hasBegin -ne $hasEnd) { throw "Malformed AOS markers in $targetAgents. Edit manually before installation." }
if ($hasBegin) {
    $pattern = [regex]::Escape($begin) + '[\s\S]*?' + [regex]::Escape($end)
    $matches = [regex]::Matches($current, $pattern)
    if ($matches.Count -ne 1) { throw 'Expected exactly one managed AOS block.' }
    $next = [regex]::Replace($current, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $block })
} elseif ([string]::IsNullOrWhiteSpace($current)) {
    $next = $block + "`n"
} else {
    $next = $current.TrimEnd() + "`n`n" + $block + "`n"
}

Write-Host "Codex home: $codexHome"
Write-Host "Global AGENTS: $targetAgents"
Write-Host "User skills: $skillsRoot"
if ($current -ne $next) {
    if ($DryRun) {
        Write-Host '[DRY RUN] Would update managed global AGENTS section.'
    } else {
        New-Item -ItemType Directory -Path $codexHome -Force | Out-Null
        if (Test-Path -LiteralPath $targetAgents) {
            Copy-Item -LiteralPath $targetAgents -Destination ($targetAgents + '.bak-' + $stamp) -ErrorAction Stop
        }
        [System.IO.File]::WriteAllText($targetAgents, $next, $utf8)
        Write-Host 'Updated global AGENTS (backup created if file existed).'
    }
} else {
    Write-Host 'Global AGENTS already up-to-date.'
}

foreach ($folder in Get-ChildItem -LiteralPath $sourceSkills -Directory) {
    $source = $folder.FullName
    $dest = Join-Path $skillsRoot $folder.Name
    if (Test-Path -LiteralPath $dest) {
        $existingManifest = Join-Path $dest 'SKILL.md'
        $sourceManifest = Join-Path $source 'SKILL.md'
        if ((Test-Path -LiteralPath $existingManifest) -and
            ([System.IO.File]::ReadAllText($existingManifest) -ceq [System.IO.File]::ReadAllText($sourceManifest))) {
            Write-Host "Skill $($folder.Name) already installed."
            continue
        }
        if (-not $UpdateSkills) {
            Write-Warning "Skipping different existing skill '$($folder.Name)'. Review it and use -UpdateSkills deliberately."
            continue
        }
        if ($DryRun) { Write-Host "[DRY RUN] Would back up and update $dest"; continue }
        $backup = $dest + '.bak-' + $stamp
        Copy-Item -LiteralPath $dest -Destination $backup -Recurse -ErrorAction Stop
        Remove-Item -LiteralPath $dest -Recurse -Force
    } else {
        if ($DryRun) { Write-Host "[DRY RUN] Would install $dest"; continue }
    }
    if (-not (Test-Path -LiteralPath $skillsRoot)) { New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null }
    Copy-Item -LiteralPath $source -Destination $dest -Recurse -ErrorAction Stop
    Write-Host "Installed skill $($folder.Name)."
}
if (-not $DryRun) { Write-Host 'Done. Start a NEW Codex session to verify discovery.' }
