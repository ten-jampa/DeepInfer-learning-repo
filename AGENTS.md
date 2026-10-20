# Course workspace rules — DeepInfer learning repo

This is a **teaching workspace** (agent curriculum, lessons, assignments), not an application repo.
The agent (OpenCode) is the teacher here; `../DeepInfer` is the read-only subject repository.

## Lesson lifecycle — MANDATORY

**When a lesson is done, you must commit it and push to `origin main`. "Done" means one of:**

- A lesson you created or substantially updated this session is delivered to the user
- (covers `lessons/`, and any `assignments/` / `reference/` that lesson includes);
- The session wraps up and the workspace has meaningful changes (mission, resources,
  notes, learning records).

**How (the only sanctioned procedure):**

```sh
./scripts/lesson-done.sh "lesson: 0002-prefill-vs-decode"
```

- The script: stages everything, commits with your message, rebases onto `origin/main`, pushes `origin main`.
  It is idempotent (exits cleanly with nothing to commit) and refuses to run off `main`.
- Add `-t` to skip the safety rebase when you know the remote is a fixup mess you want to overwrite
  (force-with-lease): `./scripts/lesson-done.sh "msg" -t`.
- **Do not** hand-roll `git add`/`commit`/`push` for lesson work — use the script so history stays uniform.
- **Do not** claim "lesson done" before the lesson HTML, its linked references, and its assignment
  (if any) actually exist at final quality.

## Content conventions

- Lesson numbering: `lessons/NNNN-dash-case-name.html`, increments.
- Never edit `../DeepInfer` (the subject repo). Only read from it.
- `NOTES.md`, `MISSION.md`, `RESOURCES.md`, `learning-records/` are living docs — keep them in the
  same commit as the lesson they support.
