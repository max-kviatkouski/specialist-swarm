# CLAUDE.md

Guidance for Claude Code (and any AI agents) working in this repository.

## Shared backlog — GitHub Issues

This repo uses **GitHub Issues as the shared backlog** so multiple developers and
Claude Code agents don't duplicate work. Use the `gh` CLI. Follow this protocol
every session:

1. **Before starting**, see what's open and who's on it:
   ```bash
   gh issue list --state open --json number,title,assignees,labels
   ```
   Skip anything already assigned or labeled `in-progress` — someone has it.

2. **Claim an unassigned issue before working on it** (the anti-collision step):
   ```bash
   gh issue edit <number> --add-assignee @me --add-label "in-progress"
   ```
   If a race is possible, claim FIRST, then re-list to confirm you got it; if it's
   now assigned to someone else, back off and pick another.

3. **While working**, leave a short status comment so others see progress:
   ```bash
   gh issue comment <number> --body "Started: <what you're doing>"
   ```

4. **When done**, link the PR and close it:
   ```bash
   gh issue edit <number> --add-label "done" --remove-label "in-progress"
   gh issue close <number> --comment "Done in #<PR>"
   ```

5. **New work you discover** → file it so it's visible to everyone, don't keep it
   in chat:
   ```bash
   gh issue create --title "<task>" --body "<context>" --label "todo"
   ```

Re-run `gh issue list` at the start of each session and before picking up a new
task so you never start something already claimed.
