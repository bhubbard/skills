# Summarizer, Writer, Rewriter, Proofreader reference

These four are all Gemini-Nano-backed, text-to-text, task-specific APIs. They share the create/generate shape from the main SKILL.md lifecycle. Internally, Chrome implements every one of them as a fixed system prompt wrapped around the Prompt API — the options you pass just get woven into that system prompt in natural language (see `polyfills.md` if you ever need to replicate this behavior yourself).

**Quick disambiguation:** Summarizer condenses; Writer drafts new content from an instruction; Rewriter transforms existing text (tone/length/format) while keeping its meaning and length roughly intact; Proofreader only fixes grammar/spelling/punctuation and explains the fix.

## Summarizer

```js
if ('Summarizer' in self) { /* supported */ }
const availability = await Summarizer.availability();
const summarizer = await Summarizer.create({
  sharedContext: 'This is a scientific article',
  type: 'key-points',      // 'key-points' (default) | 'tldr' | 'teaser' | 'headline'
  format: 'markdown',      // 'markdown' (default) | 'plain-text'
  length: 'medium',        // 'short' (default) | 'medium' | 'long'
  preference: 'auto',      // 'auto' (default) | 'speed' | 'capability'
  expectedInputLanguages: ['en', 'ja', 'es'],
  outputLanguage: 'es',
  expectedContextLanguages: ['en'],
});
```

`type` × `length` determines output shape:

| type | short | medium | long |
|---|---|---|---|
| `tldr` | 1 sentence | 3 sentences | 5 sentences |
| `teaser` | 1 sentence | 3 sentences | 5 sentences |
| `key-points` | 3 bullets | 5 bullets | 7 bullets |
| `headline` | 12 words | 17 words | 22 words |

```js
// Batch
const summary = await summarizer.summarize(longText, {
  context: 'This article is intended for a tech-savvy audience.',
});

// Streaming
const stream = summarizer.summarizeStreaming(longText, { context: '...' });
for await (const chunk of stream) { /* ... */ }
```

Strip HTML before summarizing — use `element.innerText`, not `innerHTML`.

Cross-origin iframe policy token: `allow="summarizer"`. Not available in Web Workers.

## Writer

```js
if ('Writer' in self) { /* supported */ }
const writer = await Writer.create({
  tone: 'neutral',       // 'formal' | 'neutral' (default) | 'casual'
  format: 'markdown',    // 'markdown' (default) | 'plain-text'
  length: 'medium',      // 'short' (default) | 'medium' | 'long'
  sharedContext: 'This is an email to acquaintances about an upcoming event.',
  expectedInputLanguages: ['en', 'ja', 'es'],
  expectedContextLanguages: ['en', 'ja', 'es'],
  outputLanguage: 'es',
});

// Request-based
const result = await writer.write(
  'An inquiry to my bank about how to enable wire transfers on my account.',
  { context: "I'm a longstanding customer" },
);

// Streaming
const stream = writer.writeStreaming(prompt, { context: '...' });
for await (const chunk of stream) { composeTextbox.append(chunk); }
```

Reuse one `writer` for multiple pieces of content sharing `sharedContext` (e.g. batch-drafting review responses). Abort with `AbortController` + `{ signal }`, and call `writer.destroy()` when done.

Requires the joint Writer/Rewriter origin trial (Chrome 137–148 at time of writing) or local flags: `chrome://flags/#optimization-guide-on-device-model` and `chrome://flags/#writer-api-for-gemini-nano` (plus `#prompt-api-for-gemini-nano-multimodal-input`), both **Enabled**, then relaunch.

Cross-origin iframe policy token: `allow="writer"`. Not available in Web Workers.

## Rewriter

```js
if ('Rewriter' in self) { /* supported */ }
const rewriter = await Rewriter.create({
  tone: 'as-is',          // 'more-formal' | 'as-is' (default) | 'more-casual'
  format: 'as-is',        // 'as-is' (default) | 'markdown' | 'plain-text'
  length: 'as-is',        // 'shorter' | 'as-is' (default) | 'longer'
  sharedContext: 'A review for the Flux Capacitor 3000 from TimeMachines Inc.',
  expectedInputLanguages: ['en', 'ja', 'es'],
  expectedContextLanguages: ['en', 'ja', 'es'],
  outputLanguage: 'es',
});

const result = await rewriter.rewrite(reviewEl.textContent, {
  context: 'Avoid any toxic language and be as constructive as possible.',
});

const stream = rewriter.rewriteStreaming(text, { context: '...', tone: 'more-casual' });
for await (const chunk of stream) { composeTextbox.append(chunk); }
```

**Note the option value differences from Writer**: Rewriter's `tone` values are `more-formal`/`as-is`/`more-casual` (relative), while Writer's are `formal`/`neutral`/`casual` (absolute). Don't mix these up.

Same origin trial/flags as Writer (joint trial). Cross-origin iframe policy token: `allow="rewriter"`. Not available in Web Workers.

## Proofreader

```js
if ('Proofreader' in self) { /* supported */ }
const proofreader = await Proofreader.create({
  expectedInputLanguages: ['en'],
  monitor(m) {
    m.addEventListener('downloadprogress', (e) => console.log(`${e.loaded * 100}%`));
  },
});

const result = await proofreader.proofread(
  'I seen him yesterday at the store, and he bought two loafs of bread.',
);
```

Returns a `ProofreadResult`: `correctedInput` (the fully corrected string) plus `corrections[]`, each with `startIndex`, `endIndex`, `correction` (replacement text), and optionally `type` (e.g. `"spelling"`, `"grammar"`) and `explanation`. `includeCorrectionTypes`/`includeCorrectionExplanation` options from the original explainer are **not** currently supported in Chrome's implementation — don't assume they work.

To render corrections inline, walk `corrections[]` and slice the original string by `startIndex`/`endIndex`, wrapping matched spans (e.g. in a `<span class="error">`) and leaving the rest untouched — see the docs' example for the exact loop.

Requires the Proofreader origin trial (Chrome 141–145) or local flags: `chrome://flags/#optimization-guide-on-device-model`, `#prompt-api-for-gemini-nano-multimodal-input`, `#proofreader-api-for-gemini-nano`, all **Enabled**, then relaunch. Also requires acknowledging Google's Generative AI Prohibited Uses Policy as part of origin trial signup.

Cross-origin iframe policy token: `allow="proofreader"`. Not available in Web Workers.
