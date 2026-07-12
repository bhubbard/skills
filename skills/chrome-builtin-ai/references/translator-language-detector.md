# Translator and Language Detector reference

Unlike the other five APIs, these two use small **expert models** (not Gemini Nano) trained specifically for translation and language ranking. They're desktop-only (no mobile support at all, ever) and their model downloads are per-language-pair rather than one shared blob.

## Translator

```js
if ('Translator' in self) { /* supported */ }

// Language pairs use BCP 47 codes, e.g. 'es', 'fr', 'zh-Hant'
const translatorCapabilities = await Translator.availability({
  sourceLanguage: 'es',
  targetLanguage: 'fr',
});

const translator = await Translator.create({
  sourceLanguage: 'en',
  targetLanguage: 'fr',
  monitor(m) {
    m.addEventListener('downloadprogress', (e) => console.log(`${e.loaded * 100}%`));
  },
});

await translator.translate('Where is the next bus stop, please?');
// "Où est le prochain arrêt de bus, s'il vous plaît ?"

// Streaming for longer text
const stream = translator.translateStreaming(longText);
for await (const chunk of stream) { console.log(chunk); }
```

**Privacy note:** `availability()` always reports language pairs as `downloadable` regardless of whether they're actually already cached, specifically to avoid leaking which language pairs a given site's users have previously used — don't build UI that assumes `availability()` reflects true cache state.

**Sequential processing:** translations queue — a large batch blocks subsequent calls until earlier ones finish. Chunk your requests and show a loading indicator (spinner) rather than firing many translations in parallel and expecting concurrency.

Supported language codes (Chrome's implementation, 38 total as of writing — check `references/translator-language-detector.md`'s source page for the live list since Chrome is tracking a dynamic-retrieval API to replace this static one): `ar bg bn cs da de el en es fi fr he hi hr hu id it ja kn ko lt mr nl no pl pt ro ru sk sl sv ta te th tr uk vi zh zh-Hant`.

Cross-origin iframe policy token: `allow="translator"`. Not available in Web Workers.

## Language Detector

Use before Translator when you don't already know the source language, or to route text-classification/labeling/UI-localization logic.

```js
if ('LanguageDetector' in self) { /* supported */ }

const detector = await LanguageDetector.create({
  monitor(m) {
    m.addEventListener('downloadprogress', (e) => console.log(`${e.loaded * 100}%`));
  },
});

const results = await detector.detect('Hallo und herzlich willkommen!');
for (const result of results) {
  console.log(result.detectedLanguage, result.confidence);
}
// de 0.999...
// en 0.0003...
// nl 0.0001...
```

`detect()` returns a list ranked highest-to-lowest confidence (`0.0`–`1.0`), not a single answer — pick the top result(s) above whatever confidence threshold your use case needs, and treat low-confidence results as `"unknown"` rather than trusting a shaky top pick.

**Accuracy caveat:** very short phrases or single words produce unreliable results — don't run this on a two-word input and expect a solid answer. From Chrome 132+, you can check whether a specific language is available for detection before relying on it.

Cross-origin iframe policy token: `allow="language-detector"`. Not available in Web Workers.

## Demo

Both APIs share a combined playground: `chrome.dev/web-ai-demos/translation-language-detection-api-playground/`.
