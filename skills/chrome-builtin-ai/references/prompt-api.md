# Prompt API (`LanguageModel`) reference

The free-form escape hatch: send natural language (and optionally images/audio) straight to Gemini Nano running in Chrome. Use it for anything that doesn't fit Summarizer/Writer/Rewriter/Proofreader's specialized shapes — classification, extraction, Q&A over page content, structured JSON output, multimodal description.

`LanguageModel` follows the shared availability → create → use lifecycle (see main SKILL.md). Specifics below.

## Availability and creation

```js
const availability = await LanguageModel.availability({
  // pass the SAME options you'll use in prompt()/promptStreaming()
});
```

**Always pass matching options to `availability()` and `create()`/`prompt()`** — some modalities/languages aren't supported by every configuration, and mismatched options are a common source of silent failures.

```js
const session = await LanguageModel.create({
  monitor(m) {
    m.addEventListener('downloadprogress', (e) => {
      console.log(`Downloaded ${e.loaded * 100}%`);
    });
  },
});
```

### Model parameters (Chrome Extensions / origin trial only)

`LanguageModel.params()` returns `{defaultTopK, maxTopK, defaultTemperature, maxTemperature}`. These tuning parameters (`topK`, `temperature` in `create()`) only apply when using the Prompt API for Chrome Extensions, or with the sampling-parameters origin trial enabled on the web — not in default web usage. If you specify one, you must specify both.

## Initial prompts (conversation history / system prompt)

Seed a session with prior turns — useful for resuming a stored conversation across a browser restart, or setting a system prompt:

```js
const session = await LanguageModel.create({
  initialPrompts: [
    { role: 'system', content: 'You are a helpful and friendly assistant.' },
    { role: 'user', content: 'What is the capital of Italy?' },
    { role: 'assistant', content: 'The capital of Italy is Rome.' },
  ],
});
```

### Constrain output with a prefix

Add `prefix: true` to a trailing `"assistant"`-role message to make the model continue from that exact text — useful for forcing a response format (e.g. starting a fenced code block):

```js
const characterSheet = await session.prompt([
  { role: 'user', content: 'Create a TOML character sheet for a gnome barbarian' },
  { role: 'assistant', content: '```toml\n', prefix: true },
]);
```

## Expected inputs/outputs (languages and modalities)

```js
const session = await LanguageModel.create({
  expectedInputs: [
    { type: 'text', languages: ['en', 'ja'] }, // system prompt lang, user prompt lang
  ],
  expectedOutputs: [{ type: 'text', languages: ['ja'] }],
});
```
- `expectedInputs[].type`: `text`, `image`, or `audio`.
- `expectedOutputs[].type`: `text` only.
- Supported languages (Chrome 149+): `en`, `ja`, `es`, `de`, `fr`.
- An unsupported input/output raises a `"NotSupportedError"` DOMException.

## Multimodal input

Supported input object types: audio (`AudioBuffer`, `ArrayBufferView`, `ArrayBuffer`, `Blob`), visual (`HTMLImageElement`, `SVGImageElement`, `HTMLVideoElement` — current frame, `HTMLCanvasElement`, `ImageBitmap`, `OffscreenCanvas`, `VideoFrame`, `Blob`, `ImageData`).

```js
const session = await LanguageModel.create({
  expectedInputs: [
    { type: 'text', languages: ['en'] },
    { type: 'audio' },
    { type: 'image' },
  ],
  expectedOutputs: [{ type: 'text', languages: ['en'] }],
});

const response = await session.prompt([
  {
    role: 'user',
    content: [
      { type: 'text', value: 'Compare these two images:' },
      { type: 'image', value: referenceImageBlob },
      { type: 'image', value: canvasElement },
    ],
  },
]);
```

## Append messages ahead of time

For multimodal or slow inputs, `append()` lets you push context into the session before you actually need a response — the model can start processing early:

```js
await session.append([
  { role: 'user', content: [{ type: 'text', value: 'Notes...' }, { type: 'image', value: file }] },
]);
// later:
const result = await session.prompt(userQuestion);
```
The promise resolves once the prompt is validated and appended; rejects if it can't be appended.

## Structured output (JSON Schema)

Pass `responseConstraint` (a JSON Schema) to `prompt()`/`promptStreaming()` to force conformant output:

```js
const schema = { type: 'boolean' };
const result = await session.prompt(`Is this post about pottery?\n\n${post}`, {
  responseConstraint: schema,
});
console.log(JSON.parse(result)); // true
```
The schema is included in the prompt sent to the model (costs context tokens) — measure with `session.measureContextUsage()`. Use `omitResponseConstraintInput: true` to skip sending the schema as text, but then explicitly describe the desired shape in your own prompt text so the model still knows what's expected.

## Prompting: request-based vs streaming

```js
// Short result — wait for the whole thing
const result = await session.prompt('Write me a poem!');

// Longer result — stream chunks
const stream = session.promptStreaming('Write me an extra-long poem!');
for await (const chunk of stream) {
  console.log(chunk);
}
```
Both accept an optional `{ signal }` for `AbortController`-based cancellation.

## Session management

Every session tracks a token budget:
```js
console.log(`${session.contextUsage}/${session.contextWindow}`);
```
When a prompt would overflow the window, Chrome evicts the oldest prompt/response pairs (never the system prompt) until there's room. Listen for the eviction:
```js
session.addEventListener('contextoverflow', () => {
  console.log("Some inputs were dropped due to context overflow.");
});
```
If there's nothing left to evict and the prompt still doesn't fit, `prompt()`/`promptStreaming()` rejects with `QuotaExceededError` (has `.requested` and `.contextWindow` properties) and nothing is removed.

**Clone** a session to fork the conversation (preserves context + initial prompt) without re-paying setup cost:
```js
const clonedSession = await session.clone({ signal: controller.signal });
```

**Destroy** a session you no longer need — frees resources, aborts in-flight work, and any further calls on it reject:
```js
session.destroy();
```
Keep a session alive if you expect to prompt it repeatedly — recreating sessions has overhead.

## Demos worth pointing to
- Prompt API playground, Mediarecorder Audio Prompt demo, Canvas Image Prompt demo (all under `chrome.dev/web-ai-demos/`).
- Chrome Extension sample: `GoogleChrome/chrome-extensions-samples` → `functional-samples/ai.gemini-on-device`.
