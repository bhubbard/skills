# Brandon's AI Skills Library

A comprehensive repository of custom AI Agent Skills covering platforms, tools, plugins, and workflows. These skills enhance AI coding assistants (Gemini/Antigravity, Claude, Cursor) with deep domain knowledge.

**33 skill groups | 190+ individual skills | 7 Antigravity plugins | 6 project profiles**

---

## 🔌 Antigravity Plugins (Auto-Loaded)

The easiest way to use these skills in Antigravity is via the pre-built plugins installed in `~/.gemini/config/plugins/`. These are automatically discovered and can be enabled globally or per-project.

| Plugin | Skills Included | Install Path |
|---|---|---|
| `brandon-wordpress-plugin` | WordPress core, WordPress.com, 52+ WP plugins | `~/.gemini/config/plugins/brandon-wordpress-plugin/` |
| `brandon-cloudflare-plugin` | Cloudflare routing/caching, Kumo UI (components, charts, styling) | `~/.gemini/config/plugins/brandon-cloudflare-plugin/` |
| `brandon-seo-plugin` | Astro SEO, Google Search Central, Search Console, Unlighthouse | `~/.gemini/config/plugins/brandon-seo-plugin/` |
| `brandon-analytics-plugin` | Google Analytics, Looker Studio, Google Ads API, CallRail | `~/.gemini/config/plugins/brandon-analytics-plugin/` |
| `brandon-crm-plugin` | Filevine, LeadDocket, RingCentral, CallRail | `~/.gemini/config/plugins/brandon-crm-plugin/` |
| `brandon-dev-tools-plugin` | GitHub, 1Password, Chrome DevTools MCP, Chrome Extensions | `~/.gemini/config/plugins/brandon-dev-tools-plugin/` |
| `brandon-services-plugin` | Kinsta, LocalWP, Gravatar, SendGrid, Zapier, ClickCease, ZimaBoard | `~/.gemini/config/plugins/brandon-services-plugin/` |

---

## 📦 Project Profiles (Drop-In `skills.json`)

For per-project skill loading, copy a profile from `/profiles/` into your project's `.agents/` directory as `skills.json`.

```bash
# Example: activate WordPress skills for a project
cp /Users/bhubbard/PROJECTS/brandon-skills/profiles/wordpress-full.json YOUR_PROJECT/.agents/skills.json
```

| Profile | Skills Loaded |
|---|---|
| `profiles/wordpress-full.json` | WordPress + WordPress.com + all WP plugins |
| `profiles/cloudflare-full.json` | Cloudflare + Kumo UI |
| `profiles/seo-audit.json` | SEO + Search Console + Unlighthouse + GA |
| `profiles/client-crm.json` | Filevine + LeadDocket + RingCentral + CallRail |
| `profiles/dev-tools.json` | GitHub + 1Password + Chrome DevTools + Extensions |
| `profiles/all-skills.json` | Everything (use sparingly — large context) |

---

## 📂 All Skill Groups

| Group | Description |
|---|---|
| `1password` | 1Password secrets management, CLI, SDKs |
| `astro-seo` | SEO best practices in Astro framework |
| `callrail` | CallRail call tracking API and integrations |
| `chrome-devtools-mcp` | Chrome DevTools via MCP server |
| `chrome-extensions` | Chrome Extensions (Manifest V3) |
| `clickcease` | ClickCease click fraud protection |
| `cloudflare` | Cloudflare routing, caching, Workers |
| `emdash-github-actions` | GitHub Actions via Emdash |
| `filevine` | Filevine legal case management API |
| `github` | GitHub API, PRs, Actions, CLI |
| `gmail-postmaster` | Gmail Postmaster Tools — deliverability |
| `google-ads-api` | Google Ads API integration |
| `google-analytics` | Google Analytics 4 — setup, reporting |
| `google-looker-studio` | Looker Studio dashboards and connectors |
| `google-search-central` | Google Search Central documentation |
| `google-search-console` | Search Console API and workflows |
| `gravatar` | Gravatar profile and image APIs |
| `isitagentready` | IsItAgentReady.com agent compatibility checks |
| `kinsta` | Kinsta hosting — deployments, caching, CLI |
| `kumo-ui` | Kumo UI component library by Cloudflare |
| `leaddocket` | LeadDocket legal lead management |
| `localwp` | LocalWP — local WordPress development |
| `privacy-laws` | GDPR, CCPA, and privacy law compliance |
| `ringcentral` | RingCentral business communications API |
| `sendgrid` | SendGrid transactional email API |
| `specification-website` | Specification website patterns |
| `uc-berkeley` | UC Berkeley-related skills |
| `unlighthouse` | Unlighthouse site-wide Lighthouse auditing |
| `wordpress` | WordPress core — themes, blocks, plugins |
| `wordpress-com` | WordPress.com Developer API and tools |
| `wordpress-plugins` | 52+ individual WordPress plugin skills |
| `zapier` | Zapier automation and Zap building |
| `zimaboard-casaos` | ZimaBoard hardware + CasaOS setup |

---

## 🤖 Using Skills by Tool

### Antigravity (Gemini)

**Option 1: Plugin (Recommended)**
Plugins in `~/.gemini/config/plugins/` are auto-discovered globally. All 7 `brandon-*` plugins are installed.

**Option 2: Per-Project Profile**
Create `.agents/skills.json` in your project root:
```json
{
  "entries": [
    { "path": "/Users/bhubbard/PROJECTS/brandon-skills/skills/wordpress" }
  ]
}
```
Or use a pre-built profile:
```bash
cp /Users/bhubbard/PROJECTS/brandon-skills/profiles/wordpress-full.json .agents/skills.json
```

**Option 3: Custom skills.json**
Mix and match specific skill directories:
```json
{
  "entries": [
    { "path": "/Users/bhubbard/PROJECTS/brandon-skills/skills/localwp" },
    { "path": "/Users/bhubbard/PROJECTS/brandon-skills/skills/wordpress-plugins/elementor" }
  ]
}
```

---

### Claude Code

**Option 1: `@` Mention a SKILL.md directly**
In any Claude conversation:
> `@/Users/bhubbard/PROJECTS/brandon-skills/skills/filevine/SKILL.md Read this skill, then help me with...`

**Option 2: Copy profile to project**
```bash
cp /Users/bhubbard/PROJECTS/brandon-skills/profiles/client-crm.json .agents/skills.json
```
Claude Code respects `.agents/skills.json` in project directories.

**Option 3: CLAUDE.md reference**
Add to your project's `CLAUDE.md`:
```markdown
Before working with WordPress, read: /Users/bhubbard/PROJECTS/brandon-skills/skills/wordpress/SKILL.md
```

---

### Cursor / GitHub Copilot

**Option A: `.cursorrules` reference**
```
Before writing any WordPress code, read: /Users/bhubbard/PROJECTS/brandon-skills/skills/wordpress/SKILL.md
```

**Option B: `@` mention in chat**
```
@/Users/bhubbard/PROJECTS/brandon-skills/skills/cloudflare/SKILL.md
```

**Option C: Copy skill file into project**
```bash
mkdir -p .ai-docs
cp /Users/bhubbard/PROJECTS/brandon-skills/skills/kumo-ui/kumo-ui-components/SKILL.md .ai-docs/
```

---

## 🛠️ Anatomy of a Skill

```
skills/<group>/
└── <skill-name>/
    └── SKILL.md          # Required: YAML frontmatter + markdown body
    └── references/       # Optional: extended docs
    └── examples/         # Optional: code examples
```

`SKILL.md` structure:
```yaml
---
name: skill-name
description: What the skill covers and when to trigger it.
---

# Skill Title
...instructions...
```

---

## 🏗️ Kumo UI Skills

Three new skills for the Cloudflare Kumo UI component library (v2.6.0):

| Skill | Path | Covers |
|---|---|---|
| `kumo-ui-components` | `skills/kumo-ui/kumo-ui-components/` | 34+ components, import patterns, recipes |
| `kumo-ui-charts` | `skills/kumo-ui/kumo-ui-charts/` | TimeseriesChart, SankeyChart, colors, legends |
| `kumo-ui-styling` | `skills/kumo-ui/kumo-ui-styling/` | Semantic tokens, dark mode, Tailwind v4 setup |
| `kumo-cli` | `skills/kumo-ui/kumo-cli/` | CLI commands (`ls`, `doc`, `add`) |
