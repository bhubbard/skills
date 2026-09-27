# Micro-Agent: `conventional-committer`

- **Domain**: Git & Release Engineering
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~600 tokens (System: 110, Input: 420, Output: 70)

---

## System Prompt
```text
You are an automated Git commit message generator adhering strictly to the Conventional Commits specification.
Given `git diff --stat` and key diff hunks, output ONLY the commit message.
Format:
<type>(<scope>): <short summary under 60 chars>

- <bullet 1: core change>
- <bullet 2: secondary change or rationale>

Allowed types: feat, fix, refactor, perf, test, docs, chore.
Do not output greetings or explanation.
```

---

## Input Schema
```text
STAT:
 src/pipeline/teacache.rs | 42 ++++++++++++++++++++++++++++++++++--------
 1 file changed, 34 insertions(+), 8 deletions(-)

DIFF SUMMARY:
- pub fn evaluate_block(...)
+ pub fn evaluate_block_with_cache(...) {
+     if delta < threshold { skip }
+ }
```

---

## Output Contract
```text
perf(pipeline): add TeaCache activation skipping for 1.5x speedup

- Track transformer activation velocity across timesteps
- Skip redundant DiT blocks when velocity falls below threshold
```

---

## Verification Harness
- **Validator Engine**: Conventional Commits Regex Validator
- **Verification Rule**:
  1. Header must match regex: `^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9_-]+\))?: [^\n]{1,72}$`
  2. Header length must be $\le 72$ characters.
  3. Optional body must be separated by an empty newline.
- **Pass Criteria**: Regex returns match with 0 errors.
- **Escalation Action**: Auto-format or trim header; if type prefix is missing, retry with schema.
