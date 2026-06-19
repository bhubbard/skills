Skill: Kumo UI CLI

Description

This skill covers the usage of the Kumo UI CLI (@cloudflare/kumo). Kumo is Cloudflare's accessible, design-system-compliant component library for building modern React web applications. It combines Base UI primitives with semantic color tokens adapting to light and dark mode using Tailwind CSS v4.

The CLI provides tools to query component documentation directly from the terminal and scaffold customizable "Blocks" directly into a project's source directory.

Prerequisites

Before using Kumo in a project, ensure the required peer dependencies are installed:

pnpm add react react-dom @phosphor-icons/react


Installation of the main library:

pnpm add @cloudflare/kumo


Available CLI Commands

The CLI is invoked using npx @cloudflare/kumo <command>.

1. List Components

Outputs a complete list of all available UI components in the Kumo library.

npx @cloudflare/kumo ls


2. View Component Documentation

Query detailed documentation, props, and usage examples for a specific component right from the command line.

npx @cloudflare/kumo doc <ComponentName>
# Example: npx @cloudflare/kumo doc Button


3. View All Documentation

Fetch and print the documentation for all components.

npx @cloudflare/kumo docs


4. Add/Scaffold Blocks

Adds customizable blocks (e.g., PageHeader, DeleteResource) directly into the local source directory (by default into a folder like src/components/kumo/).

npx @cloudflare/kumo add <BlockName>
# Example: npx @cloudflare/kumo add PageHeader


Note: Blocks usually depend on standard Kumo components. The CLI will warn you if you attempt to add a block without @cloudflare/kumo installed.

Usage Guidelines & Conventions

When operating within a codebase that uses Kumo UI, adhere to the following rules:

Components vs. Blocks:

Components (Button, Input, Dialog, etc.) are imported directly from the package: import { Button } from '@cloudflare/kumo';.

Blocks are larger, complex UI patterns that are NOT exported from the package index. They must be installed via the CLI kumo add command so the raw code can be edited locally.

Styling & Theming:

Always use Kumo's semantic color tokens (kumo-*, e.g., bg-kumo-base, bg-kumo-elevated).

Never use raw Tailwind colors (like bg-blue-500) or raw dark variants (dark:bg-black).

Mode switching is handled exclusively via data attributes on parent elements: data-mode="light" or data-mode="dark".

Compose class names using the provided utility: import { cn } from '@cloudflare/kumo';.

Tailwind v4 Configuration:

Tailwind CSS v4 does not scan node_modules by default. To ensure Kumo components render correctly (e.g., Dialogs centering properly), the project's main CSS file MUST include a source directive pointing to the Kumo package:

@source "../node_modules/@cloudflare/kumo/dist/**/*";


ESM Only:

Kumo is exclusively an ESM library ("type": "module"). Avoid CommonJS (require()) imports when working with Kumo configurations or extending components.
