#requires -Version 5.1
[CmdletBinding()]
param()
$homeDir = [Environment]::GetFolderPath('UserProfile')
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $homeDir '.codex' }
$global = Join-Path $codexHome 'AGENTS.md'
$skills = Join-Path (Join-Path $homeDir '.agents') 'skills'
Write-Host "Global AGENTS path: $global"
if (Test-Path $global) {
    $data = [System.IO.File]::ReadAllText($global)
    Write-Host ("Managed AOS section present: " + ($data.Contains('<!-- AOS-CODEX-GLOBAL START -->') -and $data.Contains('<!-- AOS-CODEX-GLOBAL END -->')))
} else { Write-Warning 'Missing global AGENTS.md' }
foreach ($name in @('outcome-delivery','browser-qa','evidence-learning')) {
    $file = Join-Path (Join-Path $skills $name) 'SKILL.md'
    Write-Host ("{0}: {1}" -f $name, (Test-Path $file))
}
$command = Get-Command codex -ErrorAction SilentlyContinue
if ($command) { & codex --version } else { Write-Host 'Codex CLI not in PATH; check installed app directly.' }
Write-Host 'Filesystem presence is NOT proof of runtime discovery. Open a fresh Codex session and validate.'
