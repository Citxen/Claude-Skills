---
name: code-review
description: Reviews pending code changes for bugs, security issues, and maintainability problems. Use when the user asks to review code, check a diff, or look over changes before committing
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(python *)
argument-hint: optional file path, commit range, or branch to review
---

# Code Reviewer

Review the pending changes and report problems worth fixing before they are committed.

## Workflow

1. Work out what to review:
   - If an argument is given, review that file, commit range, or branch (for a branch, use `git diff master...<branch>`; if it is the current branch, also run `git diff HEAD` to include uncommitted edits)
   - Otherwise run `git diff HEAD` for staged and unstaged changes. If `git rev-parse --verify HEAD` fails (a repo with no commits yet), run `git diff --cached` and `git diff` instead
   - Also run `git status --porcelain --untracked-files=all` to find untracked files (lines starting with `??`), which the diff does not show; this lists each file inside new folders rather than just the folder
   - If there are no changes and no untracked files, say there is nothing to review and stop
2. Run `git diff --stat` with the same commands used in step 1 (for example `git diff HEAD --stat`, or `git diff --cached --stat` and `git diff --stat` in a repo with no commits) to see which files changed, and add any untracked files to that list
3. Read the full diff, then open each changed file to see the surrounding code, not just the changed lines
4. Check each change for:
   - **Correctness**: logic errors, off-by-one mistakes, unhandled null or empty input, wrong error handling
   - **Security**: read `.claude/skills/code-review/references/security_checklist.md` and check the changes against each item
   - **Maintainability**: duplicated logic, unclear names, dead code, code that doesn't match the surrounding style. For each changed `.py` file, run `python .claude/skills/code-review/scripts/complexity_check.py <file>` and report any function it flags as a Suggestion. If Python is not available, skip this check and say it was skipped
   - **Tests**: new behaviour with no test, or tests that no longer match the code
5. Confirm each finding against the code before reporting it. Drop anything you can't point to a concrete failure for

## Output Format

Group findings by severity, most severe first:

- **Critical**: bugs or security issues that must be fixed
- **Warning**: likely problems or risky patterns
- **Suggestion**: optional improvements

For each finding give the location as `file_path:line_number`, one sentence describing the problem, and a concrete fix. Skip empty severity groups. If there are no findings, say the changes look good in one line. Never pad the review with praise or restate what the diff does.
