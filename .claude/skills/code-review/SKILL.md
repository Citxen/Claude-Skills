---
name: code-review
description: Reviews pending code changes for bugs, security issues, and maintainability problems. Use when the user asks to review code, check a diff, or look over changes before committing
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git *)
argument-hint: optional file path, commit range, or branch to review
---

# Code Reviewer

Review the pending changes and report problems worth fixing before they are committed.

## Workflow

1. Work out what to review:
   - If an argument is given, review that file, commit range, or branch (for a branch, use `git diff master...<branch>`)
   - Otherwise run `git diff --cached` for staged changes and `git diff` for unstaged changes
   - If both are empty, say there is nothing to review and stop
2. Run `git diff --stat` on the chosen range to see which files changed
3. Read the full diff, then open each changed file to see the surrounding code, not just the changed lines
4. Check each change for:
   - **Correctness**: logic errors, off-by-one mistakes, unhandled null or empty input, wrong error handling
   - **Security**: injection, hard-coded secrets, unsafe input handling, missing authorisation checks
   - **Maintainability**: duplicated logic, unclear names, dead code, code that doesn't match the surrounding style
   - **Tests**: new behaviour with no test, or tests that no longer match the code
5. Confirm each finding against the code before reporting it. Drop anything you can't point to a concrete failure for

## Output Format

Group findings by severity, most severe first:

- **Critical**: bugs or security issues that must be fixed
- **Warning**: likely problems or risky patterns
- **Suggestion**: optional improvements

For each finding give the location as `file_path:line_number`, one sentence describing the problem, and a concrete fix. Skip empty severity groups. If there are no findings, say the changes look good in one line. Never pad the review with praise or restate what the diff does.
