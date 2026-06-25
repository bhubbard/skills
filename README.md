# Brandon's AI Skills Library

A comprehensive repository of AI Agent Skills covering platforms, tools, plugins, and workflows. These skills enhance AI coding assistants (Gemini/Antigravity, Claude, Cursor) with deep domain knowledge.

> **Open source & shareable.** Fork this repo and adapt the skills to your own projects. No machine-specific paths are included in the repository itself — configure your local paths using the setup instructions below.

**33 skill groups | 190+ individual skills | 7 plugin themes | 6 project profiles**

---

## 🚀 Quick Setup

Clone the repo, then set `SKILLS_ROOT` to its location. This variable is used in all examples below:

```bash
git clone https://github.com/bhubbard/skills.git ~/skills
export SKILLS_ROOT=~/skills   # add to your shell profile
```

---

## 🔌 Antigravity Plugins

Install the themed plugins into your Gemini config directory. Each plugin auto-discovers its skills from this repo.

```bash
# Clone or copy each plugin.json + skills.json into your plugins directory
~/.gemini/config/plugins/brandon-wordpress-plugin/
~/.gemini/config/plugins/brandon-cloudflare-plugin/
~/.gemini/config/plugins/brandon-seo-plugin/
~/.gemini/config/plugins/brandon-analytics-plugin/
~/.gemini/config/plugins/brandon-crm-plugin/
~/.gemini/config/plugins/brandon-dev-tools-plugin/
~/.gemini/config/plugins/brandon-services-plugin/
```

> **Note:** The `skills.json` files in each plugin must point to the absolute path of your skills clone. After cloning this repo, update the `skills.json` path entries in each plugin to match your local `$SKILLS_ROOT`.

| Plugin | Skills Included |
|---|---|
| `brandon-wordpress-plugin` | WordPress core, WordPress.com, 52+ WP plugins |
| `brandon-cloudflare-plugin` | Cloudflare routing/caching, Kumo UI (components, charts, styling, colors, registry) |
| `brandon-seo-plugin` | Astro SEO, Google Search Central, Search Console, Unlighthouse |
| `brandon-analytics-plugin` | Google Analytics, Looker Studio, Google Ads API, CallRail |
| `brandon-crm-plugin` | Filevine, LeadDocket, RingCentral, CallRail |
| `brandon-dev-tools-plugin` | GitHub, 1Password, Chrome DevTools MCP, Chrome Extensions |
| `brandon-services-plugin` | Kinsta, LocalWP, Gravatar, SendGrid, Zapier, ClickCease, ZimaBoard |

---

## 📦 Project Profiles (Drop-In `skills.json`)

Profiles are pre-built `skills.json` files in [`/profiles/`](./profiles/) that activate the right skills for a project context.

### Setup

Replace `<SKILLS_ROOT>` in any profile with your actual path before using:

```bash
# Option 1: sed substitution
sed "s|<SKILLS_ROOT>|$SKILLS_ROOT|g" profiles/wordpress-full.json > .agents/skills.json

# Option 2: Manual — open the profile, replace <SKILLS_ROOT> with your path
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

## 🏗️ Kumo UI Skills

Five skills for the Cloudflare Kumo UI component library (`@cloudflare/kumo` v2.6.0):

| Skill | Covers |
|---|---|
| `kumo-ui/kumo-ui-components` | 34+ components, import patterns, Button/Dialog/Input/Select/Toast/Tabs recipes |
| `kumo-ui/kumo-ui-charts` | TimeseriesChart, SankeyChart, base Chart, color systems, ChartLegend |
| `kumo-ui/kumo-ui-styling` | Semantic tokens, dark mode via data-mode, Tailwind v4 @source setup, helpers |
| `kumo-ui/kumo-ui-colors` | All token values with exact light/dark OKLCH values, animation tokens |
| `kumo-ui/kumo-ui-registry` | Machine-readable registry, KUMO_*_VARIANTS, CLI doc commands, code gen |
| `kumo-ui/kumo-ui-agents` | Official AGENTS.md context — package structure, codegen, CLI, architecture |

---

## 🤖 Using Skills by Tool

### Antigravity (Gemini)

**Option 1: Plugin (Recommended for global use)**

Update the `skills.json` in each plugin under `~/.gemini/config/plugins/brandon-*-plugin/` to use your local `$SKILLS_ROOT` path, then Antigravity auto-discovers them.

**Option 2: Per-project `skills.json`**

Create `.agents/skills.json` in your project root:

```json
{
  "entries": [
    { "path": "/your/path/to/skills/wordpress" },
    { "path": "/your/path/to/skills/wordpress-plugins/elementor" }
  ]
}
```

Or use a profile as a starting point:

```bash
sed "s|<SKILLS_ROOT>|$SKILLS_ROOT|g" profiles/cloudflare-full.json > .agents/skills.json
```

---

### Claude Code

**Option 1: `@` mention a SKILL.md directly**

In any Claude conversation, reference a SKILL.md by its path:

```
@/path/to/skills/filevine/SKILL.md
```

**Option 2: Per-project profile**

Copy and configure a profile as `.agents/skills.json` in the project root.

**Option 3: CLAUDE.md reference**

Add to your project's `CLAUDE.md`:

```markdown
Before working with WordPress, read: /path/to/skills/wordpress/SKILL.md
```

---

### Cursor / GitHub Copilot

**`.cursorrules` reference:**

```
Before writing Kumo UI code, read: /path/to/skills/kumo-ui/kumo-ui-components/SKILL.md
```

**Inline `@` mention:** Reference any SKILL.md in the chat input.

**Copy to `.ai-docs/`:** Drop skill files directly into the project for automatic context.

---

## 🛠️ Anatomy of a Skill

```
skills/<group>/
└── <skill-name>/
    └── SKILL.md          # Required: YAML frontmatter + markdown body
    └── references/       # Optional: extended documentation
    └── examples/         # Optional: code examples
```

### `SKILL.md` Frontmatter

```yaml
---
name: skill-name
description: What the skill covers and when to trigger it. This text drives auto-triggering in Antigravity.
---
```

The `description` field is what AI assistants match against to auto-load relevant skills.

---

## Contributing

1. Fork the repo
2. Add a new `skills/<group>/<skill-name>/SKILL.md`
3. Include a clear `name` and `description` in the YAML frontmatter
4. Keep the SKILL.md under ~500 lines; put extended docs in `references/`
5. Submit a PR
