# WebMCP Imperative API reference

`document.modelContext` — register tools with plain JavaScript. Use this when the tool's logic doesn't map cleanly onto a single HTML `<form>`, or you need full control (navigation, multi-step state, arbitrary computation).

**Deprecation note:** `navigator.modelContext` is deprecated as of Chrome 150 — always use `document.modelContext`.

## Register a tool

```js
await document.modelContext.registerTool({
  name: 'toggle_layer',
  description: 'Control pizza layers (sauce, cheese). Use "add", "remove", or "toggle".',
  inputSchema: {
    type: 'object',
    properties: {
      layer: { type: 'string', enum: ['sauce-layer', 'cheese-layer'] },
      action: { type: 'string', enum: ['add', 'remove', 'toggle'] },
    },
    required: ['layer'],
  },
  execute: async ({ layer, action }) => {
    await toggleLayer(layer, action);
    return `Performed ${action || 'toggle'} on layer: ${layer}`;
  },
});
```

`inputSchema` is a standard JSON Schema — use `enum`/`oneOf` with `title` to give the model human-readable option labels, which measurably improves call accuracy over bare enum values with no titles:

```js
inputSchema: {
  type: "object",
  properties: {
    timeframe: {
      type: "string",
      oneOf: [
        { type: "string", const: "today", title: "Today" },
        { type: "string", const: "yesterday", title: "Yesterday" },
        { type: "string", const: "last_7_days", title: "Last 7 Days" },
      ],
      enum: ["today", "yesterday", "last_7_days"],
      description: "Timeframe for the order lookup.",
    },
  },
  required: ["timeframe"],
}
```

`execute` is the function actually run when the agent calls the tool — it can be async, do whatever DOM/state work is needed, and its return value (a string) is what the agent sees as the tool's result. Keep it focused and the return value concise — see `evals.md`'s failure-mode table for what happens when tool output is too verbose or the wrong shape.

### Annotations and hints

```js
const addTodoTool = {
  name: "addTodo",
  description: "Add a new item to the to-do list",
  inputSchema: { type: "object", properties: { text: { type: "string" } } },
  execute: async ({ text }) => { /* persistence logic */ return `Added to-do: ${text}`; },
  annotations: {
    readOnlyHint: false,        // does this tool mutate state?
    untrustedContentHint: true, // does its output include user-authored/untrusted text?
  },
};
```

### Unregister with AbortSignal

```js
const controller = new AbortController();
await document.modelContext.registerTool(addTodoTool, { signal: controller.signal });
controller.abort(); // unregisters the tool
```

## Discover tools

```js
const tools = await document.modelContext.getTools();
// alphabetically ordered, same-origin tools only by default
```

Each returned tool object includes `name`, `description`, `inputSchema` (as a JSON string), `annotations`, `origin`, and `window`.

### Cross-origin discovery

By default `getTools()` only returns same-origin tools. To see tools from other origins, list them explicitly (secure origins only) — and the hosting origin must have separately opted your origin in via `exposedTo` (see below):

```js
// https://example.com
const allTools = await document.modelContext.getTools({
  fromOrigins: ['https://partner.org'],
});
```

## Execute a tool manually

Useful for building your own in-page agent/chat UI on top of discovered tools, or for testing:

```js
const result = await document.modelContext.executeTool(tool, '{"text": "Buy milk"}');
// input arguments must be a valid JSON string
```

Returns the tool's result, or `null` if the tool triggered a navigation. Cancel with `AbortSignal`:

```js
const controller = new AbortController();
document.modelContext.executeTool(tool, '{"text": "Buy milk"}', { signal: controller.signal });
controller.abort();
```

## Listen for tool list changes

```js
document.modelContext.addEventListener('toolchange', (event) => {
  // re-render available-tools UI, etc.
});
```

## Cross-origin iframes

Tool registration is **disabled by default** inside cross-origin iframes. Two things must both be true for a cross-origin tool to be usable:

1. The parent page delegates access via Permissions Policy:
```html
<iframe src="https://example.com" allow="tools"></iframe>
```
2. The tool's own origin explicitly exposes it to the consuming origin via `exposedTo` at registration time:
```js
// https://partner.org
await document.modelContext.registerTool(
  { name: 'my_shared_tool', description: 'Shared across origins', /* ... */ },
  { exposedTo: ['https://example.com'] },
);
```
Even with both of those, the consuming page must still explicitly ask for it via `fromOrigins` in `getTools()` — see the Discover tools section above. All three checks (Permissions Policy, `exposedTo`, `fromOrigins`) are required; missing any one means the tool stays invisible cross-origin.

## Angular

Angular has experimental WebMCP support (`angular.dev/ai/webmcp`) — tools can be tied to a component's dependency-injection lifecycle, and Signal Forms can become WebMCP tools directly without manual `registerTool()` calls. Prefer this over hand-rolling the imperative API in an Angular app.

## Reference demos

- **WebMCP zaMaker** (pizza customizer) and **Travel demo** (React, multi-city/passenger flight search) in `GoogleChromeLabs/webmcp-tools/demos/` both use this API — read their source for a full working example rather than piecing one together from snippets alone.
- **Page Agent demo** shows retrieving tools from an iframe (`fromOrigins`) and executing them from a host-page chat UI.
