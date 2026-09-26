#!/usr/bin/env node
// Accessibility scan across BOTH light and dark mode, using Pa11y and Puppeteer.
// Emulates media feature `prefers-color-scheme: light` and `prefers-color-scheme: dark`
// before navigating to each page so client-side and CSS media queries render correctly.

import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer';
import pa11y from 'pa11y';
import { getSitemapPaths } from './lib/sitemap.mjs';

const origin = process.env.PREVIEW_ORIGIN || 'http://localhost:4321';
const CONCURRENCY = parseInt(process.env.A11Y_CONCURRENCY || '4', 10);

// Load .pa11yci config from cwd if present, otherwise use defaults
let pa11yOptions = {
  standard: 'WCAG2AA',
  timeout: 30000,
  wait: 500,
  runners: ['axe'],
};
let chromeArgs = ['--no-sandbox', '--disable-setuid-sandbox'];

const pa11yCiPath = path.join(process.cwd(), '.pa11yci');
if (fs.existsSync(pa11yCiPath)) {
  try {
    const raw = JSON.parse(fs.readFileSync(pa11yCiPath, 'utf8'));
    if (raw.defaults) {
      const { concurrency: _c, chromeLaunchConfig, ...rest } = raw.defaults;
      pa11yOptions = { ...pa11yOptions, ...rest };
      if (chromeLaunchConfig?.args) {
        chromeArgs = chromeLaunchConfig.args;
      }
    }
  } catch (err) {
    console.warn(`Warning: Could not parse .pa11yci (${err.message}). Using standard WCAG2AA defaults.`);
  }
}

async function runPool(items, limit, worker) {
  const results = Array.from({ length: items.length });
  let next = 0;
  async function runNext() {
    const i = next++;
    if (i >= items.length) return;
    results[i] = await worker(items[i], i);
    return runNext();
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, runNext));
  return results;
}

async function scanOne(browser, url, colorScheme) {
  const page = await browser.newPage();
  try {
    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: colorScheme }]);
    const result = await pa11y(url, { ...pa11yOptions, browser, page });
    return { url, colorScheme, issues: result.issues, failed: false };
  } catch (error) {
    return { url, colorScheme, issues: [], failed: true, error: error.message };
  } finally {
    await page.close();
  }
}

function printIssue(issue) {
  console.log(`   • ${issue.message}`);
  console.log(`     ${issue.code}`);
  console.log(`     ${issue.selector}`);
}

async function main() {
  const paths = getSitemapPaths();
  const urls = paths.map((p) => {
    const norm = p.startsWith('/') ? p : `/${p}`;
    return `${origin.replace(/\/$/, '')}${norm}`;
  });
  const jobs = urls.flatMap((url) => [
    { url, colorScheme: 'light' },
    { url, colorScheme: 'dark' },
  ]);

  console.log(`Scanning ${urls.length} pages × 2 themes (${jobs.length} runs)...\n`);

  const browser = await puppeteer.launch({ args: chromeArgs, headless: true });
  let results;
  try {
    results = await runPool(jobs, CONCURRENCY, (job) => scanOne(browser, job.url, job.colorScheme));
  } finally {
    await browser.close();
  }

  const byUrl = new Map();
  for (const r of results) {
    if (!byUrl.has(r.url)) byUrl.set(r.url, {});
    byUrl.get(r.url)[r.colorScheme] = r;
  }

  let lightErrorPages = 0;
  let darkErrorPages = 0;
  let lightTotalIssues = 0;
  let darkTotalIssues = 0;
  const darkOnly = [];

  for (const [url, { light, dark }] of byUrl) {
    const lightCount = light.issues.length;
    const darkCount = dark.issues.length;
    if (lightCount > 0) {
      lightErrorPages++;
      lightTotalIssues += lightCount;
    }
    if (darkCount > 0) {
      darkErrorPages++;
      darkTotalIssues += darkCount;
    }
    if (light.failed || dark.failed) {
      console.log(`! ${url} — failed to run (light: ${light.failed}, dark: ${dark.failed})`);
      continue;
    }
    if (lightCount === 0 && darkCount === 0) continue;

    console.log(`${url}`);
    console.log(` light: ${lightCount} issue(s)${lightCount ? '' : ' — pass'}`);
    for (const issue of light.issues) printIssue(issue);
    console.log(` dark:  ${darkCount} issue(s)${darkCount ? '' : ' — pass'}`);
    for (const issue of dark.issues) printIssue(issue);
    console.log('');

    if (lightCount === 0 && darkCount > 0) {
      darkOnly.push({ url, count: darkCount });
    }
  }

  console.log('=== Summary ===');
  console.log(
    `Light mode: ${lightErrorPages}/${urls.length} pages with issues (${lightTotalIssues} total)`,
  );
  console.log(
    `Dark mode:  ${darkErrorPages}/${urls.length} pages with issues (${darkTotalIssues} total)`,
  );

  if (darkOnly.length > 0) {
    console.log(
      `\nDark-mode-only failures (pass in light, fail in dark — likely real dark-mode bugs):`,
    );
    for (const { url, count } of darkOnly) {
      console.log(` - ${url} (${count} issue(s))`);
    }
  } else {
    console.log('\nNo pages pass in light but fail in dark.');
  }

  process.exit(lightTotalIssues + darkTotalIssues > 0 ? 2 : 0);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
