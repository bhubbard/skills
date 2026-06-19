# Brandon's AI Skills Library

A comprehensive repository of custom AI Agent Skills covering various platforms, tools, plugins, and workflows. These skills are designed to enhance the capabilities of AI coding assistants (like Gemini, Claude, and Cursor) by providing them with deep, specific domain knowledge.

Currently, this repository contains **190+ skills** organized into logical categories.

## 📂 Repository Structure

The skills are organized into the following main directories:

*   **/filevine/** - Skills for the Filevine legal case management platform (Reporting, Project Management, API).
*   **/localwp/** - Skills for managing LocalWP development environments (Blueprints, Live Links, Xdebug, MCP).
*   **/wordpress-com/** - Skills for the WordPress.com Developer ecosystem (Studio, Blueprints, MCP, REST API, Webhooks).
*   **/wordpress-plugins/** - Extensive library of skills for popular WordPress plugins (Jetpack, Yoast, Elementor, Gravity Forms, WooCommerce, etc.).
*   **/wordpress/** - Core WordPress development skills (Theme development, Block API).
*   **/zimaboard-casaos/** - Skills for managing CasaOS on ZimaBoard hardware.
*   **/cloudflare/** - Cloudflare routing and caching configurations.
*   **/astro-seo/** - Astro framework SEO best practices.
*   *(And many more...)*

---

## 🤖 How to Provide Specific Skills to AI Agents

You don't want to load all 190+ skills into every project; doing so would bloat the AI's context window. Instead, you can configure your AI assistants to pull **only the skills necessary** for the specific project you are working on.

Here is how to do this depending on the AI tool you are using:

### 1. Google Gemini (DeepMind Agentic Coding)

Gemini agents natively support custom skill manifests. To load specific skills into a project, create a `skills.json` file inside an `.agents/` directory at the root of your project:

**File Path:** `YOUR-PROJECT/.agents/skills.json`

**Contents:**
```json
{
  "entries": [
    { "path": "/Users/bhubbard/PROJECTS/brandon-skills/skills/localwp" },
    { "path": "/Users/bhubbard/PROJECTS/brandon-skills/skills/wordpress-plugins/elementor" }
  ]
}
```
When Gemini starts up in that project, it will automatically discover and load *only* the skills found in those specific directories.

### 2. Cursor / Claude / GitHub Copilot

Other AI assistants (like Cursor, Claude, or Copilot) do not yet natively support the `skills.json` manifest. For these tools, you have two primary options:

**Option A: The `.cursorrules` Approach (Recommended for Cursor)**
You can use your project's `.cursorrules` file to instruct the AI to reference specific files in this repository before taking action. 
*Example `.cursorrules`:*
> "Before writing any code related to WordPress.com, you MUST read the documentation stored in `/Users/bhubbard/PROJECTS/brandon-skills/skills/wordpress-com/wpcom-rest-api-reference/SKILL.md`."

**Option B: The Local Copy Approach**
If the AI cannot access files outside of the immediate workspace, you can copy the specific `SKILL.md` files you need directly into your project repository (e.g., inside an `.ai-docs/` or `.cursor/` folder).

**Option C: The Context Mention Approach**
In Cursor or Claude, simply use the `@` feature in chat (e.g., `@/Users/bhubbard/PROJECTS/brandon-skills/skills/localwp/localwp-mcp-integration/SKILL.md`) and say: *"Read this skill document, then complete my task according to its rules."*

---

## 🛠️ Anatomy of a Skill

Each skill resides in its own directory and contains a primary `SKILL.md` file. 

The `SKILL.md` file consists of:
1.  **YAML Frontmatter**: Defines the `name` and `description` of the skill so the AI knows when to trigger it.
2.  **Markdown Body**: The actual instructions, rules, constraints, and context the AI needs to follow.
