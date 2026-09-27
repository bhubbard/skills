# Micro-Agent: `turnstile-edge-validator`

- **Domain**: Edge Security & Bot Protection (Cloudflare Turnstile)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~320 tokens (System: 110, Input: 40, Output: 170)

---

## System Prompt
```text
You are a Cloudflare Turnstile verification engineer.
Given a secret key binding name and token parameter name, generate a zero-dependency, edge-compatible TypeScript verification function for Cloudflare Workers.
The function must:
1. POST to 'https://challenges.cloudflare.com/turnstile/v0/siteverify'.
2. Pass 'secret', 'response', and optional client 'remoteip'.
3. Return a boolean indicating verification success.
Output ONLY the TypeScript function code block.
Do NOT output commentary, markdown formatting outside the code fence, or explanations.
```

---

## Input Schema
```text
secret_binding: env.TURNSTILE_SECRET_KEY
token_param: cfToken
```

---

## Output Contract
```typescript
interface TurnstileVerifyResponse {
  success: boolean;
  "error-codes"?: string[];
  challenge_ts?: string;
  hostname?: string;
}

export async function verifyTurnstileToken(
  cfToken: string,
  secretKey: string,
  remoteIp?: string | null
): Promise<boolean> {
  if (!cfToken || !secretKey) return false;

  const formData = new FormData();
  formData.append("secret", secretKey);
  formData.append("response", cfToken);
  if (remoteIp) {
    formData.append("remoteip", remoteIp);
  }

  try {
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) return false;
    const outcome = (await res.json()) as TurnstileVerifyResponse;
    return outcome.success === true;
  } catch {
    return false;
  }
}
```

---

## Verification Harness
- **Validator Engine**: TypeScript Syntax Compiler (`tsc --noEmit`)
- **Verification Rule**:
  1. Zero external imports (relies strictly on standard Web `fetch` and `FormData`).
  2. Endpoint URL must strictly be `https://challenges.cloudflare.com/turnstile/v0/siteverify`.
  3. Returns `Promise<boolean>` with complete `try / catch` safety.
- **Pass Criteria**: Syntactically valid TypeScript, complete error handling.
- **Escalation Action**: Supply standard static boilerplate.
