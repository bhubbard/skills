# WordPress AI Agent Skills

This directory contains skills that help AI coding agents work effectively in this WordPress codebase. Each skill is a focused playbook for one slice of WordPress: when to use which API, what the conventions are, and where in the source to look when the skill isn't enough.

The codebase here is **WordPress 7.1-alpha** (master branch). Some of the APIs documented below — particularly the Abilities API, the AI Client, Block Bindings, and the Font Library — are recent additions and may not be in older training data. Treat the source files referenced at the bottom of each skill as the authoritative reference.

## Skills

### High-level / cross-cutting

| Skill | When it triggers |
| --- | --- |
| [`wordpress-development`](./wordpress-development/SKILL.md) | Writing PHP that runs inside WordPress — hooks, custom post types, REST routes, shortcodes, admin pages, enqueueing assets, cron, plugin/theme bootstrapping. |
| [`wordpress-data`](./wordpress-data/SKILL.md) | Querying or manipulating data — `WP_Query`, `WP_User_Query`, options, transients, meta, `$wpdb`, custom tables. |
| [`wordpress-block-editor`](./wordpress-block-editor/SKILL.md) | Building Gutenberg blocks, configuring `theme.json`, block patterns, block themes, the Interactivity API. |
| [`wordpress-admin`](./wordpress-admin/SKILL.md) | Operating a WordPress install — `wp-config.php`, debugging, security hardening, performance, multisite, WP-CLI, capabilities. |
| [`wordpress-coding-standards`](./wordpress-coding-standards/SKILL.md) | Writing code that passes WPCS — sanitize/escape discipline, nonces, i18n, naming, security best practices. |
| [`wordpress-abilities-ai`](./wordpress-abilities-ai/SKILL.md) | The new 6.9/7.0+ Abilities API (`wp_register_ability`) and AI Client (`wp_ai_client_prompt`), including function-calling that bridges the two. |

### File-focused subsystem skills (wp-includes/)

| Skill | Source files | When it triggers |
| --- | --- | --- |
| [`wordpress-http-api`](./wordpress-http-api/SKILL.md) | `http.php`, `class-wp-http*.php` | Outbound HTTP/HTTPS via `wp_remote_*`, transports (cURL/Streams), proxy support, SSRF protection. |
| [`wordpress-mail`](./wordpress-mail/SKILL.md) | `pluggable.php` (wp_mail), `PHPMailer/`, `class-wp-phpmailer.php` | Sending email, SMTP setup, attachments/embeds, `wp_mail_*` filters, `phpmailer_init`. |
| [`wordpress-filesystem`](./wordpress-filesystem/SKILL.md) | `wp-admin/includes/file.php`, `class-wp-filesystem-*.php` | `WP_Filesystem` abstraction, `FS_METHOD`, credential prompts, `download_url`, `unzip_file`. |
| [`wordpress-image-editor`](./wordpress-image-editor/SKILL.md) | `class-wp-image-editor*.php`, `media.php` | `WP_Image_Editor` (GD/Imagick), resize/crop, intermediate sizes, `add_image_size`. |
| [`wordpress-rewrite`](./wordpress-rewrite/SKILL.md) | `class-wp-rewrite.php`, `rewrite.php` | Pretty permalinks, `add_rewrite_rule`, endpoints, query vars, flushing. |
| [`wordpress-oembed`](./wordpress-oembed/SKILL.md) | `class-wp-oembed.php`, `class-wp-embed.php`, `embed.php` | Custom oEmbed providers, embed handlers, oEmbed-as-provider (REST), embed caching. |
| [`wordpress-feeds`](./wordpress-feeds/SKILL.md) | `feed.php`, `feed-rss2.php`, `class-feed.php`, `SimplePie/` | RSS/Atom output, custom feed types, `fetch_feed` for parsing remote feeds. |
| [`wordpress-customizer`](./wordpress-customizer/SKILL.md) | `class-wp-customize-*.php`, `customize/` | Theme Customizer panels/sections/controls/settings, live preview, selective refresh. |
| [`wordpress-cron`](./wordpress-cron/SKILL.md) | `cron.php`, `wp-cron.php` | Recurring/single events, custom schedules, replacing WP-cron with system cron. |
| [`wordpress-object-cache`](./wordpress-object-cache/SKILL.md) | `cache.php`, `class-wp-object-cache.php` | `wp_cache_*` API, cache groups, persistent drop-ins, transient vs object cache. |
| [`wordpress-site-health`](./wordpress-site-health/SKILL.md) | `wp-admin/includes/class-wp-site-health.php` | Adding tests to Site Health, async tests, debug info tab. |
| [`wordpress-sitemaps`](./wordpress-sitemaps/SKILL.md) | `sitemaps.php`, `sitemaps/`, `sitemaps/providers/` | Core XML sitemaps, custom providers, disabling for SEO plugins. |
| [`wordpress-block-bindings`](./wordpress-block-bindings/SKILL.md) | `block-bindings.php`, `block-bindings/` | Binding block attributes to dynamic sources (6.5+), post meta in blocks, pattern overrides. |
| [`wordpress-fonts`](./wordpress-fonts/SKILL.md) | `fonts.php`, `fonts/`, font library REST controllers | Font Library (6.5+), `wp_print_font_faces`, font collections, theme.json fontFamilies. |
| [`wordpress-xmlrpc`](./wordpress-xmlrpc/SKILL.md) | `xmlrpc.php`, `class-wp-xmlrpc-server.php`, `class-IXR.php`, `class-wp-http-ixr-client.php` | XML-RPC server hardening, custom methods, IXR client for outbound calls. |
| [`wordpress-pluggable`](./wordpress-pluggable/SKILL.md) | `pluggable.php` | Overriding pluggable functions via mu-plugins, when to prefer a filter, conflict pitfalls. |
| [`wordpress-l10n`](./wordpress-l10n/SKILL.md) | `l10n.php`, `class-wp-locale.php`, `class-wp-locale-switcher.php` | `load_textdomain`, locale switching mid-request, `WP_Locale`, `date_i18n`, per-user locales. |

## How to use them

These follow the standard SKILL.md format: a YAML frontmatter block with `name` and `description`, then markdown body. The `description` is what the agent matches against when deciding which skill to load — keep it specific so it triggers on the right tasks.

When you're using Claude Code or another agent that supports skills, this folder is read automatically. To invoke one manually in a conversation: `Read .claude/skills/<slug>/SKILL.md`.

## Coverage strategy

The skills come in two layers:

1. **Cross-cutting playbooks** (the first six in the table above). These cover the topics every WordPress developer encounters — hooks, queries, the block editor, admin operations, coding standards, and the new AI APIs.
2. **File-focused subsystem skills** (the rest). One skill per significant wp-includes subsystem — usually corresponding to a single PHP file or directory. These surface the lesser-known APIs that don't come up often but are exactly the right tool when they do.

Together they cover the surface area where an AI agent is most likely to be wrong or shallow: not the headline features (everyone knows about `WP_Query`), but the auxiliary systems that take real WordPress experience to know about — like `WP_Filesystem`, the Font Library, oEmbed providers, sitemap providers, or the right way to override `wp_mail` from a mu-plugin.

## What's not covered

- Specific third-party plugins (WooCommerce, ACF, Yoast). Those have their own conventions; add a skill for the specific plugin you're working with.
- Frontend HTML/CSS styling beyond what theme.json and block-supports provide.
- Server administration outside WordPress's own constants (Nginx tuning, MySQL tuning, etc.).
- The bundled themes' individual design systems. Each `wp-content/themes/twentytwenty*/` is documented in its own `style.css`, `theme.json`, and `readme.txt`.
- Deep block-editor JS internals beyond the introductory coverage in `wordpress-block-editor`. The full `@wordpress/*` package surface is large; add a skill scoped to the package you're working with if needed.

## Extending

To add a new skill: create `<slug>/SKILL.md` with the frontmatter shape used by the existing files. Keep the `description` field action-oriented ("Use when…") so the agent's matcher fires on the right kinds of requests, and end the body with a "Where to look in this codebase" section that points at the canonical source files. The `skill-creator` skill that ships with Cowork can scaffold this for you.
