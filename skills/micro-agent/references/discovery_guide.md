# Continuous Discovery Guide: Identifying Micro-Agents in Active Projects

As you develop software across projects in `~/PROJECTS`, you will repeatedly encounter micro-tasks that are:
1. Too small to warrant a massive 1M-token frontier subagent invocation.
2. Too tedious to execute manually every single time.
3. Completely deterministic in input and output structure.

This guide provides the framework for identifying and codifying these into reusable micro-agents.

---

## 🧭 The Discovery Matrix

Evaluate any candidate engineering task against the following matrix:

| Criterion | Threshold | Why It Matters for Micro-Agents |
| :--- | :--- | :--- |
| **Input Token Scope** | $\le 2,000$ tokens | Must fit into on-device SLM context with ample room for completion. |
| **Turn Count** | Exactly 1 turn | Micro-agents do not hold multi-turn debates; they transform inputs to outputs. |
| **Output Determinism** | High | Output is verifiable by a compiler, linter, regex, or JSON schema validator. |
| **Execution Frequency** | $\ge 5$ times/day | Micro-agents must provide tangible compound productivity gains. |

---

## 💡 Prime Micro-Agent Opportunities by Domain

### 1. Rust Ecosystem (`cargo`, `rustc`, `clippy`)
- **Unused Import Pruner**: Takes a compiler `unused_imports` warning and line number $\to$ produces the exact removal edit.
- **Lifetime & Clone Recommender**: Takes a borrow-checker error $\to$ suggests `.clone()` or lifetime annotation.
- **Cargo.toml Dependency Tidy**: Cleans duplicate or outdated feature flags in `Cargo.toml`.
- **Derive Macro Synthesizer**: Generates standard `#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]` blocks for structs.

### 2. Modern Web & Frontend (`astro`, `typescript`, `react`)
- **Tailwind Class Normalizer**: Orders utility classes according to standard CSS specificity rules.
- **TypeScript Interface Generator**: Converts a raw JSON API response into strict TypeScript `interface` types.
- **SEO Meta Tag Formatter**: Converts page frontmatter into OpenGraph and Twitter card `<meta>` tags.

### 3. Git & Release Engineering
- **Semantic Commit Formatter**: Turns `git diff --stat` into standard Conventional Commits format (`feat:`, `fix:`, `refactor:`).
- **PR Description Bulletizer**: Synthesizes branch commit logs into a 3-bullet PR description.
- **Changelog Entry Generator**: Formats a released version's git log into standard Keep-a-Changelog Markdown.

---

## 📝 Lifecycle: From Discovery to Skill Catalog

When you spot a repeating pattern in a project:

1. **Step 1: Capture the Diagnostic / Input**: Save an example input snippet.
2. **Step 2: Draft the System Prompt**: Keep it strictly under 200 tokens using the template.
3. **Step 3: Measure the Token Footprint**: Run `python3 scripts/token_counter.py`.
4. **Step 4: Commit to Catalog**: Add a new markdown definition under `skills/micro-agent/catalog/<name>.md`.
5. **Step 5: Call from Scripts or Parent Agents**: Hook the micro-agent into `apfel-rs`, git hooks, or IDE shortcuts.
