import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Common locations for Astro / static build sitemaps
const CANDIDATE_PATHS = [
  process.env.SITEMAP_PATH,
  path.join(process.cwd(), 'dist', 'client', 'sitemap-0.xml'),
  path.join(process.cwd(), 'dist', 'sitemap-0.xml'),
  path.join(process.cwd(), 'dist', 'client', 'sitemap-index.xml'),
  path.join(process.cwd(), 'dist', 'sitemap.xml'),
  path.join(__dirname, '..', '..', '..', '..', 'dist', 'client', 'sitemap-0.xml'),
].filter(Boolean);

/**
 * Reads the most recent build output's sitemap and returns every page as a
 * relative pathname (e.g. "/services/" or "/contact").
 */
export function getSitemapPaths() {
  const sitemapPath = CANDIDATE_PATHS.find((p) => existsSync(p));

  if (!sitemapPath) {
    throw new Error(
      `Could not find sitemap file in candidates: ${CANDIDATE_PATHS.join(', ')}. Run "npm run build" first.`,
    );
  }

  let xml;
  try {
    xml = readFileSync(sitemapPath, 'utf8');
  } catch (error) {
    throw new Error(`Failed to read sitemap at ${sitemapPath}: ${error.message}`, {
      cause: error,
    });
  }

  const paths = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(([, loc]) => {
    try {
      const parsed = new URL(loc);
      return parsed.pathname;
    } catch {
      return loc;
    }
  });

  if (paths.length === 0) {
    throw new Error(`No <loc> entries found in ${sitemapPath}.`);
  }

  return paths;
}
