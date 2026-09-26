#!/usr/bin/env node
// Prints every URL from the built sitemap, rewritten to point at the local
// preview server, one per line — piped into `xargs pa11y-ci` so pa11y-ci
// receives a plain list of URLs instead of trying to fetch the sitemap over HTTP.
import { getSitemapPaths } from './lib/sitemap.mjs';

const origin = process.env.PREVIEW_ORIGIN || 'http://localhost:4321';

for (const pagePath of getSitemapPaths()) {
  const normalizedPath = pagePath.startsWith('/') ? pagePath : `/${pagePath}`;
  console.log(`${origin.replace(/\/$/, '')}${normalizedPath}`);
}
