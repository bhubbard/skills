#!/usr/bin/env bash
#
# Description-optimization loop for all 12 code-porting skills.
#
# Tunes each skill's `description` frontmatter for trigger accuracy using the
# skill-creator run_loop.py optimizer. Each skill is evaluated against its
# eval set (this directory), iterated up to 5 times, and the best description
# (selected on the held-out test split) is reported.
#
# REQUIREMENTS
#   - Run in an AUTHENTICATED Claude Code session (`claude` CLI logged in, or
#     ANTHROPIC_API_KEY set). The optimizer shells out to `claude -p`, so it
#     will NOT work in an unauthenticated sandbox.
#   - The skill-creator skill must be available locally.
#
# USAGE
#   SKILL_CREATOR=/path/to/skill-creator \
#   MODEL=claude-opus-4-8 \
#   ./run-optimization.sh
#
# The script writes per-skill reports and a summary to ./results/.

set -uo pipefail

EVALS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(dirname "$EVALS_DIR")"          # .../skills/code-porting
RESULTS_DIR="$EVALS_DIR/results"
MODEL="${MODEL:-claude-opus-4-8}"
MAX_ITERS="${MAX_ITERS:-5}"

# Point this at your local skill-creator directory (contains scripts/run_loop.py).
SKILL_CREATOR="${SKILL_CREATOR:-}"
if [[ -z "$SKILL_CREATOR" || ! -f "$SKILL_CREATOR/scripts/run_loop.py" ]]; then
  echo "ERROR: set SKILL_CREATOR to your skill-creator dir (must contain scripts/run_loop.py)." >&2
  exit 1
fi

mkdir -p "$RESULTS_DIR"

SKILLS=(
  port-planning
  porting-workflow-loops
  adversarial-code-review
  compiler-errors-as-work-queue
  test-suite-driven-port
  semantic-porting-pitfalls
  port-verification-checklist
  port-to-rust-playbook
  rust-lifetimes-analysis
  zig-to-rust-mapping
  rust-crate-decomposition
  rust-porting-mistakes
)

echo "Optimizing ${#SKILLS[@]} skills with model=$MODEL, max-iterations=$MAX_ITERS"
echo "Results -> $RESULTS_DIR"
echo

for skill in "${SKILLS[@]}"; do
  echo "=============================================================="
  echo "  $skill"
  echo "=============================================================="
  ( cd "$SKILL_CREATOR" && python3 -m scripts.run_loop \
      --eval-set   "$EVALS_DIR/$skill.json" \
      --skill-path "$SKILLS_DIR/$skill" \
      --model      "$MODEL" \
      --max-iterations "$MAX_ITERS" \
      --report     "$RESULTS_DIR/$skill.report.html" \
      --verbose \
      > "$RESULTS_DIR/$skill.log" 2>&1 )
  echo "  done -> $RESULTS_DIR/$skill.log (report: $RESULTS_DIR/$skill.report.html)"
  echo
done

echo "All skills processed. Review the .log files and .report.html files in $RESULTS_DIR."
echo "run_loop.py prints the best_description as JSON at the end of each log; apply it to the"
echo "corresponding SKILL.md frontmatter (or re-run with --verbose to watch train/test scores)."
