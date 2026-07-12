# Evals for WebMCP tools

WebMCP tools are called by generative-AI-backed agents, which means calls are probabilistic, not deterministic — the same tool, description, and user request can produce a correct call most of the time and a wrong one occasionally. Before shipping tools to production, write evals that check the touchpoints between your tool and the model, not just classic unit tests of the tool's own code.

An eval suite should verify:
- The model understands your tool's purpose from its `description` and schema alone.
- The model picks the *right* tool, with the *right* parameters, for a given user intent.
- The model correctly threads information from one tool call into the next (e.g. using a search result's ID in a follow-up call).
- Full user journeys actually complete given the tools you've exposed.

Keep writing classic deterministic tests too, for anything that doesn't touch the model (tool internals, UI updates, side effects) — evals are additive, not a replacement.

## Failure modes to design tests around

Concrete example: a user wants to add a t-shirt to their cart.

| Failure | Example | What to check |
|---|---|---|
| Agent picks the wrong tool, or skips one | Skips `addToCart`, goes straight to `checkout` | Is `description` clear and accurate? Is the tool name intuitive? Is its schema too similar to another tool's, causing ambiguity? |
| Agent calls tools in the wrong order | Calls `checkout` before `addToCart` | Do descriptions overlap and confuse required sequencing? Does a preceding tool's output supply context the next tool needs? Is newly-relevant state/tools correctly exposed after each step? |
| Agent calls the right tool with wrong arguments | Calls `addToCart` but adds shoes instead of the t-shirt | Is `inputSchema` precise, with `enum` values and clear per-property `description`s? Are required params actually marked required? Does the description tell the model exactly how to map fuzzy user language onto structured values (specific IDs/formats)? |
| Tool output is wrong or incomplete | User asks `viewCart`, gets total cost instead of item names/prices | Bugs in the tool's own logic (catch with deterministic tests)? Was UI state actually updated before the tool read it? Is the output formatted for easy LLM ingestion, and free of unnecessary verbosity? |
| The tool code itself throws | Any runtime JS error inside `execute` | Are errors caught and reported back to the agent gracefully, not left to crash silently? Is the error message specific enough that the model can tell "retry-worthy transient issue" from "hard failure, give up"? Are dependent external services actually healthy? |

## Test tools in isolation before testing full journeys

If the model can't figure out which tool to call for something as simple as "I'd like a small pizza," it has no chance in a longer multi-tool journey — start narrow. Trigger a single tool call directly with `document.modelContext.executeTool(...)` to validate your schema/description choices before layering on complexity.

### Deterministic, rule-based call assertions

Given a message and the full list of tools currently exposed by the page (matching the actual app state you're testing — e.g. what's available right when a co-browsing session opens a specific view), assert the exact expected function/arguments:

```json
{
  "messages": [{ "role": "user", "content": "I'd like a small pizza." }],
  "expectedCall": [
    { "functionName": "set_pizza_size", "arguments": { "size": "Small" } }
  ]
}
```

Always provide the **complete** tool list relevant to the state under test, not just the one tool you're focused on — an agent's tool-selection accuracy depends on what else is available to compare against, so testing a tool in artificial isolation from its siblings can give a false read.

### Deterministic tests (no model involved)

For everything that's pure code — verify tool logic directly, confirm dependencies are called correctly, confirm UI/state side effects happen, verify returned values match expectations, validate parameter handling. Mock dependencies like you would for any other integration test (e.g. mock a `SearchComponent` the tool calls into), and simulate the surrounding app state realistically.

### Probabilistic tests (evals proper)

Needed whenever a tool call depends on model reasoning rather than a fixed code path. Write **both**:
- **Direct queries** — unambiguous asks that name the action plainly ("Add pepperoni to my pizza").
- **Open-ended queries** — ambiguous asks requiring the model to infer intent and map it onto a tool ("I want all of the meat on my pizza" → must know which toppings count as meat, then call `add_topping` for each).

Chain-dependent example: a coffee shop wants "reorder what I got last month" to work. That requires `get_order_history` (mocked to return a product ID) *before* `order_product` — the eval should confirm the model calls history-lookup first and correctly threads its result into the order call; if it skips straight to `order_product` without an `item_id`, that's the failure this eval catches.

## End-to-end testing

Beyond individual tool calls, verify multi-step journeys complete in the right order, with unordered flexibility only where genuinely order-independent. Example: "I am looking to buy a black jacket and a pair of jeans. Could you provide a breakdown of the materials used?" — a correct journey navigates to the category, then searches + fetches details for each item (jacket-then-jeans or jeans-then-jacket is fine, but within each item, search must precede detail-fetch):

```json
{
  "messages": [{ "role": "user", "content": "I am looking to buy a black jacket and a pair of jeans. Could you provide a breakdown of the materials used?" }],
  "expectedCall": [
    { "functionName": "navigate_to_category", "arguments": { "category": "clothes" } },
    {
      "unordered": [
        { "ordered": [
          { "functionName": "search_clothes", "arguments": { "query": "black jacket" } },
          { "functionName": "get_product_details", "arguments": { "productId": "JACKET002" } }
        ]},
        { "ordered": [
          { "functionName": "search_clothes", "arguments": { "query": "jeans" } },
          { "functionName": "get_product_details", "arguments": { "productId": "JEANS001" } }
        ]}
      ]
    }
  ]
}
```

Use `unordered`/`ordered` nesting like this to express "these two branches can happen in either order, but each branch's own steps must stay in sequence."

## Evaluate mid-chain failures

Sequential tool chains can partially fail — e.g. ordering a discounted pizza calls `start_pizza_creator` → `set_pizza_style` → `set_pizza_size` → `start_checkout` → `add_discount_coupon` → `complete_checkout`, and if `add_discount_coupon` silently fails, the agent might still complete checkout at full price, which is a bad outcome even though nothing "crashed."

To test this without needing the model to reliably reach that exact state via natural conversation, **manually drive the tool sequence up to the failure point** (bypass the model for setup), then evaluate the specific tool-under-test (`add_discount_coupon`) in isolation from that known state. This is more reliable than trying to coax a model into a specific mid-journey state through prompting alone.

## Tooling

Google ships an experimental CLI for exactly this kind of testing: `github.com/GoogleChromeLabs/webmcp-tools/tree/main/evals-cli`. Point the user there instead of building a bespoke test harness from scratch if they need to actually run these evals, not just design them. Chrome's broader "Create AI evaluations" course (`developer.chrome.com/docs/ai/evals`) covers eval methodology beyond WebMCP specifically, if the user wants the general background.
