#!/usr/bin/env bash
# Verify the Paxus skills library is healthy and ready to sync into Cowork.
#
#   bash scripts/verify.sh
#
# Exit 0 = all checks pass (READY). Exit 1 = at least one FAIL (NOT READY).
# WARN lines are for human attention but do not fail the run.
set -uo pipefail
cd "$(dirname "$0")/.." || { echo "FATAL: cannot find repo root"; exit 2; }

MANIFEST=".claude-plugin/marketplace.json"
fail=0; warn=0
pass() { printf "  \033[32mPASS\033[0m  %s\n" "$1"; }
fyl()  { printf "  \033[31mFAIL\033[0m  %s\n" "$1"; fail=$((fail+1)); }
wrn()  { printf "  \033[33mWARN\033[0m  %s\n" "$1"; warn=$((warn+1)); }

echo "Verifying the Paxus skills library…"
echo

# 1. The marketplace manifest must be valid JSON (Cowork can't sync if it isn't).
if [ ! -f "$MANIFEST" ]; then
  fyl "$MANIFEST is missing — Cowork has nothing to sync from"
  echo; echo "RESULT: NOT READY — 1 problem"; exit 1
fi
if python3 -c "import json; json.load(open('$MANIFEST'))" 2>/dev/null; then
  pass "marketplace.json is valid"
else
  fyl "marketplace.json is not valid — fix this before anything else"
  echo; echo "RESULT: NOT READY — 1 problem"; exit 1
fi

# Collect skills the manifest lists, and skills actually on disk.
listed=$(python3 -c "
import json
d=json.load(open('$MANIFEST'))
for p in d.get('plugins',[]):
    for s in p.get('skills',[]):
        print(s)
")
ondisk=""
for d in skills/*/; do [ -d "$d" ] && ondisk+="./${d%/}"$'\n'; done

# 2. Every skill the manifest lists must exist and have a SKILL.md.
while IFS= read -r s; do
  [ -z "$s" ] && continue
  if [ -f "$s/SKILL.md" ]; then pass "listed skill is present: $s"
  else fyl "listed skill is missing its SKILL.md: $s (Cowork sync will break)"; fi
done <<< "$listed"

# 3. Every skill folder on disk should be listed, or it silently won't sync.
while IFS= read -r d; do
  [ -z "$d" ] && continue
  if grep -qF "\"$d\"" "$MANIFEST"; then :
  else wrn "skill folder exists but is NOT listed in marketplace.json — it won't reach the team: $d"; fi
done <<< "$ondisk"

# 4. Every SKILL.md needs a name + description, and the name should match its folder.
for f in skills/*/SKILL.md; do
  [ -e "$f" ] || continue
  dir=$(basename "$(dirname "$f")")
  name=$(awk -F': *' '/^name:/{print $2; exit}' "$f" | tr -d '"'\''[:space:]')
  desc=$(awk -F': *' '/^description:/{print $2; exit}' "$f")
  if [ -n "$name" ]; then pass "$dir: has a name"; else fyl "$dir: SKILL.md is missing 'name:'"; fi
  if [ -n "$desc" ]; then pass "$dir: has a description"; else fyl "$dir: SKILL.md is missing 'description:'"; fi
  if [ -n "$name" ] && [ "$name" != "$dir" ]; then
    wrn "$dir: the name '$name' doesn't match the folder '$dir' — they should match"; fi
done

# 5. Client data must never live in a skill (skills = engine, client data = fuel).
#    Heuristic scan — flags for human review, never the final word.
leaks=$(grep -rInE 'if[[:space:]]+client[[:space:]]*==|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\b[0-9]{7,}\b' skills/ 2>/dev/null \
  | grep -viE 'example|placeholder|your-?email|kebab-case' | head -20)
if [ -n "$leaks" ]; then
  wrn "possible client data inside a skill — skills must not contain client names, emails, or account numbers."
  wrn "Move it to the client's Google Drive folder (see docs/context-model.md). Lines to check:"
  echo "$leaks" | sed 's/^/        /'
else
  pass "no obvious client data found in skills"
fi

echo
if [ "$fail" -gt 0 ]; then
  echo "RESULT: NOT READY — $fail problem(s), $warn warning(s) to review."
  exit 1
else
  echo "RESULT: READY — 0 problems, $warn warning(s) to review."
  exit 0
fi
