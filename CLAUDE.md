# CLAUDE.md

## task-observer activation

Before the first tool call of any session — and before writing or
proposing a plan, not merely before executing one — invoke the
task-observer skill AND execute its Session Start Protocol (storage
check, frontmatter scan, review trigger). Loading the skill and running
the protocol are separate steps; a session that loads the file and stops
has activated nothing. Any turn that will involve a tool call counts; do
not classify the session as "too simple" from its opening message.

After completing each task, check the observation records written this
session and report a one-line summary (ids and titles, or "none logged
and why"). This is the activation backstop: it forces a look at the log,
so a session that silently skipped the protocol is discovered at the
first task boundary instead of never.

Loading a skill is not complete until you have queried the observation
log for OPEN observations naming it and read their bodies:
  grep -l "skill:.*<skill-name>" \
    /home/user/thegrowthedit/.claude/skill-observations/observation-log/*.md
Apply their insights to the current work, even if the skill file hasn't
been updated yet. Run this at every skill load, however many skills load
in one session. The session-start scan does not cover it: that is a
frontmatter sweep over every observation at session start, this is a
body-level lookup for one skill at the moment its rules are applied.

The task-observer workspace for this project is:
  /home/user/thegrowthedit/.claude
Every path the skill uses derives from that root and nothing else:
  /home/user/thegrowthedit/.claude/skill-observations/observation-log/   (the log)
  /home/user/thegrowthedit/.claude/skill-observations/cross-cutting-principles.md
  /home/user/thegrowthedit/.claude/skill-updates/                        (staging root)
  /home/user/thegrowthedit/.claude/skill-updates/PENDING.md              (staging manifest)
Never resolve any of them from the current working directory — a cwd
inside an ephemeral checkout (a git worktree, a temporary clone) is torn
down and takes the log with it. Never place the workspace inside a
skills-discovery directory or any path linked into one.
