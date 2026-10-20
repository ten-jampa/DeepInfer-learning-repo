#!/bin/sh
# lesson-done.sh — the canonical finish ritual for the teaching workspace.
# Stage everything, commit, sync with origin/main, push.
# Usage: ./scripts/lesson-done.sh [message] [-t]
#   message  optional commit message (default: lesson: <latest lesson file>)
#   -t       trust the working tree: skip rebase and force-push (use sparingly)
set -eu

cd "$(dirname "$0")/.."

case "${1:-}" in
  -t) FORCE=1; shift ;;
esac
BRANCH="$(git branch --show-current)"
[ "$BRANCH" = "main" ] || { echo "aborted: you are on branch '$BRANCH', expected main" >&2; exit 1; }

# Nothing to do when the tree is clean.
if [ -z "$(git status --porcelain)" ]; then
  echo "nothing to commit — workspace clean"
  exit 0
fi

git add -A

MSG="$1"
[ -n "$MSG" ] || MSG="lesson: $(ls lessons | sort | tail -1 2>/dev/null || echo workspace-update)"
git commit -m "$MSG"

# Sync with origin/main (skip if the remote branch doesn't exist yet).
if git fetch origin main 2>/dev/null && git rev-parse --verify --quiet origin/main >/dev/null; then
  git pull --rebase origin main
else
  echo "no origin/main yet — creating it"
  git push -u origin main
  exit 0
fi

if [ "${FORCE:-}" = 1 ]; then
  git push --force-with-lease origin main
else
  git push origin main
fi
echo "✓ pushed: $MSG"
