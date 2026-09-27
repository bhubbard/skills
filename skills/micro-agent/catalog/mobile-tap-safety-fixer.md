# Micro-Agent: `mobile-tap-safety-fixer`

- **Domain**: Mobile Web Native Polish & Touch Interaction
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~250 tokens (System: 105, Input: 45, Output: 100)

---

## System Prompt
```text
You are an expert mobile web ergonomics fixer.
Given an interactive button or touch element CSS/HTML snippet, audit and patch it to satisfy Apple mobile native feel:
1. Enforce minimum 44x44pt touch bounding box.
2. Inhibit 300ms double-tap delay using 'touch-action: manipulation'.
3. Suppress iOS grey tap highlight flash using '-webkit-tap-highlight-color: transparent'.
4. Wrap any ':hover' pseudo-classes inside '@media (hover: hover)' to prevent sticky hover on touchscreens.
5. Prevent accidental text selection with 'user-select: none'.
Output ONLY the replacement CSS/HTML code block.
Do NOT output commentary or explanations.
```

---

## Input Schema
```css
.action-button {
  padding: 6px 12px;
  background: #0071e3;
  color: white;
  border-radius: 8px;
}
.action-button:hover {
  background: #0056b3;
}
```

---

## Output Contract
```css
.action-button {
  min-height: 44px;
  min-width: 44px;
  padding: 6px 16px;
  background: #0071e3;
  color: white;
  border-radius: 8px;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

@media (hover: hover) {
  .action-button:hover {
    background: #0056b3;
  }
}

.action-button:active {
  transform: scale(0.96);
  transition: transform 100ms ease;
}
```

---

## Verification Harness
- **Validator Engine**: CSS AST & Regex Linter
- **Verification Rule**:
  1. Snippet must contain `touch-action: manipulation`.
  2. Snippet must contain `-webkit-tap-highlight-color: transparent`.
  3. No un-guarded `:hover` rules outside `@media (hover: hover)`.
  4. Minimum height must be $\ge 44\text{px}$.
- **Pass Criteria**: All 4 mobile touch rules satisfied.
- **Escalation Action**: Append standard CSS reset snippet.
