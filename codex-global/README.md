# Optional cross-project Codex defaults

This folder is an opt-in installation layer for the existing Software Development Control Plane. It does not change the control plane's runtime, schemas, sample projects, or governance. It contains **generic, public-safe engineering practices only**.

## Purpose

Install small, stable guidance **once** so every *new local Codex session on this machine/account* can discover it, while each target repository keeps its own product rules, tests, security boundaries, and working state.

- Source of truth (version-controlled): `codex-global/GLOBAL_AGENTS.md`, `codex-global/skills/*/SKILL.md`.
- Installed global instructions: `$CODEX_HOME/AGENTS.md` when CODEX_HOME is set; otherwise `~/.codex/AGENTS.md`.
- Installed user-level skills: `~/.agents/skills/<skill-name>/SKILL.md`.
- Repo-specific instructions stay in each repository's own `AGENTS.md`.
- A Codex Goal belongs to a single thread. The rules here do **not** start a Goal automatically or authorize continuous autonomous background execution.

## Windows PowerShell (native Codex Desktop)

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\codex-global\install-windows.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\codex-global\install-windows.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\codex-global\verify-windows.ps1
```

The installer refuses to overwrite different existing skills unless `-UpdateSkills` is explicitly supplied, and backs up the existing global AGENTS.md when its content changes. The global file is maintained inside explicit markers so other instructions are preserved. If the markers are malformed, it stops. Review the script before running. The installer never alters project repositories or sends data externally.

## WSL (separate Linux home)

Installing on Windows does **not** install to WSL. From the WSL checkout:

```bash
bash codex-global/install-wsl.sh --dry-run
bash codex-global/install-wsl.sh
```

Use `--update-skills` only after reviewing existing skill changes. Do not share or synchronize private credentials or machine-specific Codex state across home directories.

## Verify in a fresh Codex session

1. Confirm the real active Windows/WSL Codex environment and repository/worktree.
2. Inspect the installed global AGENTS.md and the three installed skill directories on disk.
3. Start a fresh Codex session in a small disposable repository and ask for a short summary of the applicable global/project instructions and the names of relevant available skills.
4. Give a bounded coding task and verify that Codex preserves dirty work, uses appropriate tests, and gives a truthful completion/blocked report.
5. For a UI task, check that visual/browser QA is attempted only if the environment and permissions allow it.

No install or environment validation is complete merely because these files exist in GitHub.

## Updating safely

Pull the reviewed latest commit, run the dry run, then the installer. Changes to evergreen policy/skills require evidence, security review, and a tracked Git diff. Do not auto-sync potentially unreviewed instruction changes into active sessions. Repo-local policy and user instructions take precedence where applicable. Credentials, private product contracts, media, and internal Notion context are deliberately excluded.

Official references: https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide and https://developers.openai.com/api/reference/cli and https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex.
