---
name: build-data-contract
description: >
  Generate or update the PostgreSQL Data Contract YAML file (datacontracts/dbs/postgresql.yaml)
  for a JumpCloud Go service by parsing goose SQL migration files in db/migrations/. Always use
  this skill when someone asks to: create or generate a data contract for a JumpCloud service,
  build or scaffold the datacontracts/dbs/ folder, regenerate postgresql.yaml because new tables
  or columns were added, or when the data contract is described as missing or out of date. Also
  trigger when the user mentions "DB schema contract", "data contract is missing", "add the data
  contract yaml",   or wants to document the postgres schema of a jumpcloud-* service. Do NOT
  trigger for: creating new goose migration files, Kafka/event data contracts (events.yaml —
  use build-events-data-contract instead), Redis or non-postgres schemas, or OpenAPI/REST API specs.
---

# Build Data Contract

Generate a Data Contract Spec 0.9.3 `postgresql.yaml` for a JumpCloud service by replaying
its goose SQL migrations to reconstruct the live schema, then enriching it with descriptions,
examples, enums, and data classifications.

The gold-standard output to aim for is the style of
`jumpcloud-health-monitoring/datacontracts/dbs/postgresql.yaml` — every table has a
description, every column has a type, description, classification, and example value.

---

## Step 1 — Locate the repo and migrations

Determine the target repo root. If the user didn't specify one, use the current working
directory (or the repo they have open in their IDE).

```bash
# Confirm repo root by looking for db/migrations/
ls <repo_root>/db/migrations/
```

If `db/migrations/` doesn't exist or contains no `.sql` files, tell the user and stop — there
is nothing to parse yet.

Infer the **app name** from the repo directory name (e.g., `jumpcloud-identity-risk`). You'll
use it as the YAML `id`, `title`, `owner`, and database name (`jumpcloud_identity_risk`).

---

## Step 2 — Run the migration parser

The bundled script does the heavy lifting: it replays all goose `Up` sections chronologically,
accumulating `CREATE TABLE` / `ALTER TABLE` changes into a final schema, and outputs a skeleton
YAML with placeholder descriptions and examples.

```bash
python3 <skill_dir>/scripts/parse_migrations.py \
  <repo_root>/db/migrations/ \
  --app-name <app-name> \
  --out /tmp/<app-name>-skeleton.yaml
```

Where `<skill_dir>` is the absolute path to this skill's directory (next to this SKILL.md).

Read the stderr summary — it tells you how many tables were detected and lists any enum types
found. If 0 tables were detected, check that the migrations use `CREATE TABLE` statements (not
just seed data migrations).

Read the skeleton YAML to understand the full table/column inventory before moving on.

Quickly sanity-check the column names — if you see anything that looks like a SQL keyword,
a short preposition (e.g., `per`, `on`, `by`), or starts with `--`, the parser may have been
confused by a SQL comment inside a CREATE TABLE body. You can verify by grep-ing the migration
file for that column name. If it's a false positive, manually remove it from the skeleton
before enriching.

---

## Step 3 — Gather context for enrichment

Before enriching the YAML, quickly explore the repo to understand the domain:

1. **Go struct definitions** — look in `src/` or internal packages for Go structs that map to
   DB tables. Field comments often explain the purpose of a column.
   ```bash
   grep -r "type.*struct" <repo_root>/src/ --include="*.go" -l | head -20
   ```

2. **Proto / gRPC definitions** — if the service has a `proto/` or `api/` directory, proto
   field names and comments map closely to DB columns.

3. **Existing data contracts** in sibling repos for naming patterns and classification
   precedents. The health-monitoring contract at
   `jumpcloud-health-monitoring/datacontracts/dbs/postgresql.yaml` is a good reference.

4. **Migration comments** — the migration files themselves often contain comments explaining
   why a column was added. Skim a few migrations for context.

You don't need to be exhaustive — just enough context to write sensible descriptions.

---

## Step 4 — Enrich the skeleton YAML

Take the skeleton from Step 2 and fill in every `TODO` field. For each table and column, apply
the following:

### Table-level description
Write 1–2 sentences explaining what the table stores and its role in the system. Look at the
table name, its columns, and any FK relationships for clues.

### Column-level fields

**`type`** — Already set by the parser. Check `references/type_mappings.md` if anything looks
off (e.g., a USER-DEFINED column that you know is an enum). Columns from `VARCHAR(N)` /
`CHAR(N)` in the migration will be emitted as `type: varchar` with `maxLen: N` — do not
change these to `text`, as the length constraint is meaningful.

**`enum`** — Add an `enum:` list for columns with a fixed set of values. Sources:
- `CREATE TYPE ... AS ENUM (...)` in the migrations — the parser reports these in its stderr
  summary output ("Enum types found: ..."). Check the migration file that defines each type to
  get the exact values.
- Column names like `status`, `type`, `os_family`, `severity`, `category`
- Values referenced in seed-data `INSERT` statements in migrations
- Array columns with a custom enum element type (e.g., `applied_on translation_rule_applied_on_type[]`)
  should also have `enum:` listing the valid values

**`description`** — One clear sentence. For common patterns:
- `id` → `Internal id, primary key`
- `object_id` (bytea) → `External object id for the <entity>`
- `organization_object_id` → `Mongo ObjectID of the organization`
- `created_at` → `UTC Timestamp when the <entity> was created`
- `updated_at` / `last_updated_at` → `UTC Timestamp when the <entity> was last updated`
- `created_by` → `email id of the user who created the <entity>`
- Foreign key `<table>_id` → `reference to id from <table> table associated with this entry`

**`classification`** — See `references/type_mappings.md`. Default to `level3`. Use `level2`
for email addresses and user-facing PII like names.

**`example`** — A realistic single value (string-quoted):
- `bigint` PKs: `'1'`
- `bytes` (ObjectID): `'\x671766674dd4bd0001ec87e1'`
- `timestamp_ntz`: `'2024-10-07 12:10:46.531157'`
- `boolean`: `'true'`
- Email: `'user@jumpcloud.com'`
- `text` enums: one of the valid enum values

**`config`** — Already set for arrays and USER-DEFINED types. Don't add `config` unless
needed.

**`fields`** (for `object`/`jsonb` columns) — Expand the nested schema if you can determine
the JSON structure from migration comments, Go structs, or context. For a column like
`filters jsonb`, look for INSERT or UPDATE statements in the migrations that show the JSON
shape, or search Go source files for the struct that maps to this column.
If the structure is genuinely unknown or highly dynamic, `fields: {}` is acceptable — just note
it in the description (e.g., "JSON object containing filter criteria; schema is dynamic").

**`items`** (for `array` columns) — Set `items: { type: text }` for string/enum arrays.
For custom PostgreSQL enum array types (e.g., `translation_rule_applied_on_type[]`), set
`items: { type: text }` and add the enum values directly on the parent array field.

### CSV examples section

At the end of the YAML, fill in the `examples:` section with one realistic CSV data row per
table. The row should use plausible values consistent with the field examples above.

---

## Step 5 — Write the file

Create the output directory and write the enriched YAML:

```bash
mkdir -p <repo_root>/datacontracts/dbs/
```

Then write the file to `<repo_root>/datacontracts/dbs/postgresql.yaml`.

Verify the final YAML is valid:
```bash
python3 -c "import yaml, sys; yaml.safe_load(open('<repo_root>/datacontracts/dbs/postgresql.yaml'))" && echo "YAML valid"
```

---

## Step 6 — Generate the CI workflow file (first-time only)

When the data contract is being created **for the first time** in a repo (i.e.,
`datacontracts/dbs/postgresql.yaml` did not previously exist), the repo also needs the
generated GitHub Actions workflow file that CI checks for:

```
.github/workflows/events-datacontract-check.origin.yml
```

Check whether it already exists before running:

```bash
ls <repo_root>/.github/workflows/events-datacontract-check.origin.yml
```

If it is **missing**, generate it by running the following from the repo root:

```bash
cd <repo_root> && bin/origin generate
```

This is a code-generated file (`# Code generated by jumpcloud-origin. DO NOT EDIT.`) and must
not be edited manually. If `bin/origin generate` succeeds, verify the file was created:

```bash
ls <repo_root>/.github/workflows/events-datacontract-check.origin.yml
```

If the file already exists (e.g., the contract is being regenerated after schema changes), skip
this step entirely.

---

## Output format

The file must follow this exact structure (Data Contract Spec 0.9.3):

```yaml
dataContractSpecification: 0.9.3
id: urn:datacontract:<app-name>
info:
  title: <app-name>
  version: 1.0.0
  description: |
    Data contract for <app-name>
  owner: <app-name>
servers:
  production:
    type: postgres
    database: <app_name_with_underscores>
    schema: public
    host: host.docker.internal
    port: 5432
models:
  <table_name>:
    description: <table description>
    type: table
    fields:
      <col_name>:
        type: <dc_type>
        description: <description>
        classification: <level2|level3>
        example: '<value>'
      # ... more columns
  # ... more tables
examples:
  - type: csv
    model: <table_name>
    description: Example csv for <table_name> table
    data: |
      col1,col2,...
      val1,val2,...
  # ... one example per table
```

---

## Quality checklist

Before finishing, verify:
- [ ] Every table has a non-placeholder `description`
- [ ] Every column has `type`, `description`, `classification`, and `example` — no `TODO` remains
- [ ] Enum columns have `enum:` lists
- [ ] `jsonb` columns have either nested `fields:` or `fields: {}`
- [ ] `array` columns have `items: { type: ... }`
- [ ] CSV examples section has one entry per table with a realistic row
- [ ] YAML passes `yaml.safe_load` without errors
- [ ] If this was a first-time generation, `.github/workflows/events-datacontract-check.origin.yml` exists (generated via `bin/origin generate`)
