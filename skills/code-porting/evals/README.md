# Trigger eval sets & description optimization

This directory holds the trigger-accuracy eval sets for the 12 `code-porting` skills, plus a runner for the skill-creator description-optimization loop.

## What's here

- `<skill-name>.json` — 18 trigger-test queries per skill (~8 should-trigger, ~10 should-not-trigger). The negatives are deliberately tricky **near-misses** — most are queries that belong to a *sibling* porting skill, which is the real triggering risk in a family this tightly related. Format: `[{"query": "...", "should_trigger": true|false}, ...]`.
- `run-optimization.sh` — loops the optimizer over all 12 skills.
- `results/` — created on first run; holds per-skill logs and HTML reports.

## Why the loop couldn't run in Cowork

The optimizer (`skill-creator/scripts/run_loop.py`) measures triggering by shelling out to `claude -p` for every query × 3 runs × candidate description × iteration. The Cowork sandbox's `claude` CLI is **not logged in** and no `ANTHROPIC_API_KEY` is set, so those subprocess calls fail. The descriptions were instead tightened analytically (see the git history / the SKILL.md `description` fields). Run the empirical loop yourself to confirm and further tune.

## How to run it (authenticated session)

In an interactive, logged-in Claude Code session (or with `ANTHROPIC_API_KEY` exported):

```bash
SKILL_CREATOR=/path/to/skill-creator \
MODEL=claude-opus-4-8 \
./run-optimization.sh
```

`SKILL_CREATOR` must point at the skill-creator directory that contains `scripts/run_loop.py`. Each skill iterates up to 5 times; the loop splits each eval set 60/40 train/test and selects the `best_description` by **test** score to avoid overfitting. The chosen description is printed as JSON at the end of each `results/<skill>.log`.

To optimize a single skill:

```bash
cd /path/to/skill-creator
python3 -m scripts.run_loop \
  --eval-set   /path/to/code-porting/evals/port-to-rust-playbook.json \
  --skill-path /path/to/code-porting/port-to-rust-playbook \
  --model claude-opus-4-8 --max-iterations 5 --verbose
```

## Applying results

`run_loop.py` reports the best description but does not edit your files. Copy the `best_description` from the log into the matching `SKILL.md` frontmatter, then re-run to confirm the score held.
