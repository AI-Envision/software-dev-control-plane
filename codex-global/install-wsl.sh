#!/usr/bin/env bash
set -euo pipefail
dry_run=0
update_skills=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=1 ;;
    --update-skills) update_skills=1 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done
source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
target="$codex_home/AGENTS.md"
skill_home="$HOME/.agents/skills"
start='<!-- AOS-CODEX-GLOBAL START -->'
end='<!-- AOS-CODEX-GLOBAL END -->'
stamp="$(date +%Y%m%d-%H%M%S)"
python3 - "$target" "$source_dir/GLOBAL_AGENTS.md" "$dry_run" "$stamp" <<'PY'
import pathlib, sys
target, source, dry, stamp = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), bool(int(sys.argv[3])), sys.argv[4]
begin = "<!-- AOS-CODEX-GLOBAL START -->"
end = "<!-- AOS-CODEX-GLOBAL END -->"
old = target.read_text(encoding="utf-8") if target.exists() else ""
new_block = begin + "\n" + source.read_text(encoding="utf-8").rstrip() + "\n" + end
if old.count(begin) != old.count(end) or old.count(begin) > 1:
    raise SystemExit(f"Malformed managed section in {target}")
if old.count(begin):
    start_index = old.index(begin)
    end_index = old.index(end, start_index) + len(end)
    new = old[:start_index] + new_block + old[end_index:]
elif old.strip():
    new = old.rstrip() + "\n\n" + new_block + "\n"
else:
    new = new_block + "\n"
print(f"Global AGENTS: {target}")
if old == new:
    print("Already current")
elif dry:
    print("[DRY RUN] Would update managed section")
else:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        (target.parent / (target.name + ".bak-" + stamp)).write_bytes(target.read_bytes())
    target.write_text(new, encoding="utf-8")
    print("Updated (backup created when applicable)")
PY
for skill in "$source_dir"/skills/*; do
  [[ -d "$skill" ]] || continue
  name="$(basename "$skill")"
  target_skill="$skill_home/$name"
  if [[ -d "$target_skill" ]]; then
    if [[ -f "$target_skill/SKILL.md" ]] && cmp -s "$skill/SKILL.md" "$target_skill/SKILL.md"; then
      echo "Already installed: $name"; continue
    fi
    if [[ "$update_skills" -ne 1 ]]; then
      echo "SKIP different existing skill: $name (review; use --update-skills deliberately)" >&2; continue
    fi
    if [[ "$dry_run" -eq 1 ]]; then echo "[DRY RUN] Would back up/update $name"; continue; fi
    cp -a "$target_skill" "$target_skill.bak-$stamp"
    rm -rf -- "$target_skill"
  fi
  if [[ "$dry_run" -eq 1 ]]; then echo "[DRY RUN] Would install $name"; continue; fi
  mkdir -p "$skill_home"
  cp -a "$skill" "$target_skill"
  echo "Installed $name"
done
echo "Open a NEW WSL Codex session to verify discovery; Windows installation is separate."
