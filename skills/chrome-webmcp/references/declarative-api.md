# WebMCP Declarative API reference

Turn an existing `<form>` into a WebMCP tool by adding HTML attributes — no JavaScript required for the basic case. Use this when the action already is a form (support requests, search, checkout) and you don't need the flexibility of the Imperative API.

## Register a tool from a form

Two required attributes on the `<form>` element:

- `toolname` — the tool's name (should clearly reflect its purpose).
- `tooldescription` — what the tool does.

```html
<form toolname="createSupportRequest" tooldescription="Submits a request for customer support.">
</form>
```

When an agent calls the tool, the browser **brings the form into focus and populates its fields** — the form stays visible, so the user sees exactly what the agent is doing. Remove either attribute and the tool unregisters itself automatically — no explicit teardown call needed (unlike the Imperative API's `AbortSignal` pattern).

## Tool parameters from form fields

Each form field becomes a schema property automatically. By default, the browser derives each property's description from the field's `<label>` (skipping labelable descendants), falling back to `aria-description` if there's no label. Override this with `toolparamdescription` when the label text alone isn't enough context for the model (e.g. a `<select>` where the option values encode routing logic, not just display text):

```html
<form toolname="supportRequestTool" tooldescription="Submit a request for support." action="/submit">
  <label for="firstName">First Name</label>
  <input type=text name=firstName>

  <label for="lastName">Last Name</label>
  <input type=text name=lastName>

  <select name="select" required
    toolparamdescription="Determines what team this request is routed to.">
    <option value="Customer happiness team">Return my purchase.</option>
    <option value="Distribution team">Check where my package is.</option>
    <option value="Website support team">Get help on the website.</option>
  </select>

  <button type=submit>Submit</button>
</form>
```

The browser derives this JSON Schema automatically (shown here for `supportRequestTool` above):
```json
{
  "name": "supportRequestTool",
  "description": "Submit a request for support.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "firstName": { "type": "string" },
      "lastName": { "type": "string" },
      "select": {
        "type": "string",
        "anyOf": [
          { "type": "string", "const": "Customer happiness team", "title": "Return my purchase." },
          { "type": "string", "const": "Distribution team", "title": "Check where my package is." },
          { "type": "string", "const": "Website support team", "title": "Get help on the website." }
        ],
        "enum": ["Customer happiness team", "Distribution team", "Website support team"],
        "description": "Determines what team this request is routed to."
      }
    },
    "required": ["select"]
  }
}
```
Note `<option>` display text becomes each choice's `title` and the `value` becomes the `const`/`enum` entry — the model sees the human-readable label, your code still gets the underlying value.

## Form submission: manual vs. auto

By default the **user must manually click Submit** even after the agent populates the fields — this is the safe default for anything consequential. Add `toolautosubmit` to skip that and submit automatically the moment the model invokes the tool:

```html
<form toolautosubmit toolname="search_tool" tooldescription="Search the web" action="/search">
  <input type=text name=query>
</form>
```

### Detecting agent-triggered submits and returning a result

`SubmitEvent` gains two things relevant to WebMCP:
- `agentInvoked` (boolean) — true when an AI agent triggered this submit, so you can branch your validation/UX logic.
- `respondWith(Promise<any>)` — pass a promise the browser resolves and serializes back to the model as the tool's output. You must call `preventDefault()` first to stop the browser's normal form submission.

```html
<form toolautosubmit toolname="search_tool" tooldescription="Search the web" action="/search">
  <input type=text name=query>
</form>
<script>
  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    if (!myFormIsValid()) {
      if (e.agentInvoked) { e.respondWith(myFormValidationErrorPromise); }
      return;
    }
    if (e.agentInvoked) { e.respondWith(Promise.resolve("Search is done!")); }
  });
</script>
```

## Lifecycle events

Fired on `window`, both non-cancelable, both carry a `toolName`:

```js
window.addEventListener('toolactivated', ({ toolName }) => {
  // Fires once the form is focused and fields are pre-filled by an agent.
  // Good place to run UI validation or highlight what changed.
});

window.addEventListener('toolcancel', ({ toolName }) => {
  // Fires if the user cancels the agentic operation, or reset() is called.
});
```

## Visual focus indicators

When a tool is actively populating/submitting, the browser applies CSS pseudo-classes so users can see it happening:

- `:tool-form-active` — applied to the tool's `<form>` element.
- `:tool-submit-active` — applied to the form's submit button, if present.

Both deactivate on submit, cancel, or reset. Chrome's own defaults:
```css
form:tool-form-active {
  outline: light-dark(blue, cyan) dashed 1px;
  outline-offset: -1px;
}
input:tool-submit-active {
  outline: light-dark(red, pink) dashed 1px;
  outline-offset: -1px;
}
```
Customize these rather than removing them entirely — a visible indicator that an agent is acting on the page is part of what makes WebMCP trustworthy to the end user; don't hide it.

## Reference demo

**Le Petit Bistro** (`GoogleChromeLabs/webmcp-tools/demos/french-bistro`) uses the Declarative API end to end — a good source of a complete, realistic example beyond the snippets here.
