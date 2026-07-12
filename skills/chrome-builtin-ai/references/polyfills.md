# Polyfills for unsupported browsers/platforms

Built-in AI only exists in Chrome/Chromium-based browsers on specific OS/hardware (see main SKILL.md requirements). For everyone else — Safari, Firefox, mobile, older hardware — there are two official experimental polyfills. Use these when the user needs the feature to work broadly, not just in a Chrome-on-a-good-laptop demo.

## Prompt API polyfill (`prompt-api-polyfill`)

A spec-compliant polyfill of `LanguageModel` on top of either a **cloud backend** (OpenAI, Gemini API, etc.) or a **local backend** (Transformers.js running the model in-browser via WebGPU/WASM). Ships as npm package `prompt-api-polyfill`; source at `GoogleChromeLabs/web-ai-demos/prompt-api-polyfill`.

**For production use, Chrome's own docs recommend Firebase AI Logic Hybrid SDK instead of this polyfill** — mention that to the user if they're building something beyond a prototype.

```bash
npm install prompt-api-polyfill
```

Cloud backend config (`.env.json`):
```json
{ "apiKey": "y0ur-Api-k3Y", "modelName": "model-name" }
```
⚠️ Never ship a raw cloud API key client-side without protection — Firebase AI Logic Hybrid SDK + App Check is the safe pattern; a bare key in client JS is stealable.

Local backend config (no real API key needed, Transformers.js runs in-browser):
```json
{ "apiKey": "dummy", "device": "webgpu", "dtype": "q4f16", "modelName": "onnx-community/gemma-3-1b-it-ONNX-GQA" }
```
`device`: `"webgpu"` for speed, `"wasm"` for max compatibility. Pick models from the Hugging Face catalog filtered to `transformers.js` + `text-generation`.

Loading pattern — only pull in the polyfill when the browser doesn't already support the real API:
```js
import config from './.env.json' with { type: 'json' };
window.$BACKEND_CONFIG = config; // e.g. window.OPENAI_CONFIG, window.FIREBASE_CONFIG

if (!('LanguageModel' in window)) {
  await import('prompt-api-polyfill');
}

const session = await LanguageModel.create({
  expectedInputs: [{ type: 'text', languages: ['en'] }],
  expectedOutputs: [{ type: 'text', languages: ['en'] }],
});
await session.prompt('Tell me a joke!');
```

### What's different vs. the real browser API
- **Cloud-backed = not actually private/offline.** If you pick a cloud backend, you lose the "nothing leaves the device" and "works offline" guarantees — the provider's own privacy policy applies instead. Listen for `online`/`offline` window events if you need to detect connectivity.
- **No real download for cloud backends** — the polyfill fakes `downloadprogress` events (one at `loaded: 0`, one at `loaded: 1`) so your existing UI code doesn't need special-casing.
- **Cost.** Cloud backends bill per token. Use `session.contextUsage` × your provider's per-token price to track/cap spend if that matters for your app.
- **Bigger context windows** than on-device (cloud provider limits apply instead of the local 4k-ish window), so overflow is rarely a practical concern with cloud backends.
- Supports structured output (`responseConstraint`) except on the Transformers.js backend; supports multimodal input except the OpenAI backend can't take audio+image together (only one at a time).

### Writing a custom backend
Extend `PolyfillBackend`, implement `static availability(options)`, `createSession(options, sessionParams, monitorTarget)`, `generateContent(contents)`, `generateContentStream(contents)`, `countTokens(contents)`, then register it in the polyfill's `#backends` static array with a `config` key (the `window` global name to look for) and a `path`. Add a default model in `backends/defaults.js`. Validate against the Web Platform Tests suite (`npm run test:wpt`) before trusting it matches spec behavior — the polyfill's whole value proposition is spec fidelity.

## Task API polyfills (`built-in-ai-task-apis-polyfills`)

Covers `Summarizer`, `Writer`, `Rewriter`, `Translator`, `LanguageDetector` — the task-specific APIs don't have their own dedicated fallback the way Prompt API does, so this package builds one **on top of** the Prompt API polyfill, by replicating the exact system prompts Chrome uses internally for each task API (extracted via `chrome://on-device-internals` → Event Logs).

```bash
npm install built-in-ai-task-apis-polyfills
```

```js
import config from './.env.json' with { type: 'json' };
window.FIREBASE_CONFIG = config; // or whichever backend

const polyfills = [];
if (!('Summarizer' in window)) polyfills.push(import('built-in-ai-task-apis-polyfills/summarizer'));
if (!('Writer' in window)) polyfills.push(import('built-in-ai-task-apis-polyfills/writer'));
if (!('Rewriter' in window)) polyfills.push(import('built-in-ai-task-apis-polyfills/rewriter'));
if (!('LanguageDetector' in window)) polyfills.push(import('built-in-ai-task-apis-polyfills/language-detector'));
if (!('Translator' in window)) polyfills.push(import('built-in-ai-task-apis-polyfills/translator'));
await Promise.all(polyfills);

// Then use exactly like the real API:
if ((await Summarizer.availability()) === 'available') {
  const summarizer = await Summarizer.create();
  const summary = await summarizer.summarize('Long text to summarize...');
}
```

This is the recommended "just make it work everywhere" loading pattern: check each global first, only import what's missing, so browsers with native support never download polyfill code they won't use.

### How Chrome's task APIs actually work internally (useful background, not something to replicate unless building your own polyfill)

Every task API is just the Prompt API with a fixed system prompt. For example, Summarizer's internal call looks like:
```
<system>
You are a skilled assistant that accurately summarizes content provided in the
TEXT section... [conveys type/format/length/language as natural language rules]
<end>
<user>
TEXT: foo
<end><model>
```
Proofreader works the same way but Chrome **post-processes** the raw model text response into the `correctedInput`/`corrections[]` structure itself — it does not rely on the model to output correct `startIndex`/`endIndex` values directly, because models are unreliable at counting characters. If you're ever building a from-scratch proofreading polyfill, don't trust the model for indices either; diff the corrected text against the original programmatically instead.
