# Micro-Agent: `cloudflare-d1-migration-maker`

- **Domain**: Edge SQL & Cloudflare D1 Database Migrations (`flared1`, `ascend-cf`, `flaredo`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~420 tokens (System: 110, Input: 160, Output: 150)

---

## System Prompt
```text
You are an expert SQLite & Cloudflare D1 migration engineer.
Given an existing TypeScript entity interface and a newly modified interface with added/modified fields, output ONLY the forward SQLite migration DDL commands.
Rules:
1. Use standard SQLite dialect supported by Cloudflare D1.
2. Add appropriate indices for foreign keys or search fields.
Output ONLY the raw SQL commands.
```

---

## Input Schema
```typescript
// EXISTING
interface VideoJob {
  id: string;
  prompt: string;
  status: 'queued' | 'processing' | 'done';
}

// MODIFIED (added seed, resolution, and execution time)
interface VideoJob {
  id: string;
  prompt: string;
  status: 'queued' | 'processing' | 'done';
  seed: number;
  width: number;
  height: number;
  duration_ms?: number;
}
```

---

## Output Contract
```sql
ALTER TABLE video_jobs ADD COLUMN seed INTEGER NOT NULL DEFAULT 42;
ALTER TABLE video_jobs ADD COLUMN width INTEGER NOT NULL DEFAULT 704;
ALTER TABLE video_jobs ADD COLUMN height INTEGER NOT NULL DEFAULT 480;
ALTER TABLE video_jobs ADD COLUMN duration_ms INTEGER;

CREATE INDEX IF NOT EXISTS idx_video_jobs_status_seed ON video_jobs(status, seed);
```

---

## Verification Harness
- **Validator Engine**: In-Memory SQLite Engine (`sqlite3 :memory:`)
- **Verification Rule**:
  1. Execute output DDL against an in-memory SQLite database:
     `sqlite3 :memory: < generated_migration.sql`
  2. Verify all `CREATE TABLE`, `ALTER TABLE`, and `CREATE INDEX` statements execute with exit code 0.
- **Pass Criteria**: In-memory SQLite execution succeeds with zero errors.
- **Escalation Action**: If SQLite syntax error is raised, reject migration and escalate to Tier 2.
