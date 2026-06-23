---
name: build-events-data-contract
description: >
  Build or update Kafka/event Data Contract YAML at datacontracts/events/events.yaml from
  sample JSON event payloads. Always use this path: create the file only if missing; if it
  already exists under datacontracts/, update (merge into) that file—never add a second events
  contract file. Follow JumpCloud data-contracts layout and datacontract-cli ODCS patterns. Use
  when the user asks to create or update an events data contract, events.yaml, Kafka contract,
  or schema from sample messages. Do **not** search the repo or codebase for sample events.
  If the user’s prompt does **not** include sample JSON, **ask them directly** to paste
  representative payload(s) before inferring models. Trigger on: event_type as model name,
  JC events, or "data contract for events". Do NOT use for PostgreSQL/dbs/postgresql.yaml (use
  build-data-contract) or for REST/OpenAPI-only APIs.
---

# Build or update events data contract

Produce or merge **ODCS-style** event contracts suitable for linting and testing with the
[Data Contract CLI](https://cli.datacontract.com/) (validate with **Docker** `lint` as below;
`datacontract test` with Kafka credentials is separate). Align layout with the JumpCloud
**`data-contracts`** repo convention: the events contract is **always**
**`datacontracts/events/events.yaml`** at the service (or repo) root.

---

## Non-negotiable: `event_type` is the model name

- For each distinct event, read the **`event_type`** field from the sample payload (or header
  metadata if the user says type is only in headers—then use that value the same way).
- The **`models:`** key for that event **must be exactly the `event_type` string** (e.g.
  `user.security.password_change`, `org.settings.updated`).
- Do **not** translate `event_type` into a different identifier for the model key (no automatic
  snake_case or PascalCase renames for model names).

If multiple samples share one `event_type`, merge their keys: **union** of all field paths;
if types disagree, prefer the wider type (e.g. `number` if one sample has int and another
float) and note ambiguity in `description`.

---

## Inputs the agent should accept

1. **Sample JSON messages** (one or more) — from **this conversation**: pasted in the prompt or
   entered after you ask. **Required** to infer or extend schema unless only non-schema edits
   apply (see workflow step 0). Do not substitute with samples found by searching the repo.
2. Optional: **server block** — `host`, `topic`, `format` (`json` typical), `endpointUrl` if
   applicable. If missing, keep a placeholder `production` server block consistent with
  [CLI Kafka docs](https://cli.datacontract.com/#test) or the team template.

---

## Workflow

### 0. Sample JSON: prompt only — ask if missing (do not search)

Before building a new contract or adding/updating **models or fields**, you need **sample JSON
event message(s)**. Treat samples as **only** what appears **in the user’s prompt** (or what they
paste after you ask).

**Do not** look for samples by searching or scanning the codebase: no **`grep`**, no
**`codebase_search`**, no **`glob`** for example JSON, and no opening random files hoping to find
event payloads — **unless** the user **explicitly** pointed you at a file path or said “read
samples from …”.

**If the current user message does not contain sample JSON** (no pasted payload, no attached
file content in the prompt):

1. **Stop** and **ask the user directly** to **enter / paste** one or more representative JSON
   event messages — ideally one sample per distinct `event_type` they want in the contract.
2. Ask that each sample include **`event_type`** (or state clearly if it lives only in Kafka
   headers so you can still name the model).
3. **Do not invent** full field lists or types from imagination. **Do not proceed** to write or
   merge schema-changing updates until you have samples, **except**:
   - **Metadata-only** edits the user specified in full (e.g. bump `info.version`, change
     `servers.production.topic`) with **no** new fields or event types; or
   - The user explicitly says to derive changes **only** from the existing
     `datacontracts/events/events.yaml` on disk (no new shapes).

After samples arrive (in a follow-up message or the same prompt), continue from step 1.

### 1. Resolve target path (fixed file; create vs update)

**Canonical path:** **`datacontracts/events/events.yaml`** (relative to the repo or project root).

1. Check whether **`datacontracts/events/events.yaml`** already exists.
2. **If it exists** — **do not create a new file.** Load it and **update** by merging new or
   changed models/fields into the existing YAML, then write back to the **same path**.
3. **If it does not exist** — create the directory and file:
   `mkdir -p datacontracts/events` and write **`datacontracts/events/events.yaml`**.
4. Do **not** add a parallel events contract under a different name or folder unless the user
   **explicitly** requests a non-standard path (default is always `datacontracts/events/events.yaml`).

### 2. Parse samples into models (use the bundled script)

Do **not** hand-roll grouping and field extraction. Run **`parse_event_samples.py`** so
grouping by `event_type`, union of keys across samples, and type widening stay consistent.

```bash
python3 <skill_dir>/scripts/parse_event_samples.py \
  path/to/sample1.json path/to/sample2.json \
  --out /tmp/event-models.json
```

- **`skill_dir`** is the absolute path to this skill’s directory (next to this `SKILL.md`).
- Inputs: one or more files, each containing a **single JSON object**, a **JSON array** of
  objects, or **NDJSON** (one object per line). Use **`-`** as a path to read stdin.
- **`--event-type-key`** defaults to `event_type`; use it if the discriminator field has another
  name.
- Output: JSON with **`models.<event_type>.fields`** — inferred types (`string`, `integer`,
  `number`, `boolean`, `object` with nested `fields`, `array` with `items`), **`sample_count`**,
  and **`example`** where applicable.

Then **enrich** that output into ODCS `datacontracts/events/events.yaml`: add human
**`description`** on each model and field, map script types to final ODCS names using
[json-to-odcs-types.md](references/json-to-odcs-types.md) where they differ (e.g. `timestamp`),
decide whether to keep **`event_type`** as a field to match wire format vs existing repo style,
and fill **`example`** strings for lint if the script omitted them for nested structures.

Once JSON is available (from the prompt or after asking), **write** it to temp files (or one
NDJSON file) if needed, then run the script on those paths.

### 3. Merge when updating an existing contract

This applies whenever **`datacontracts/events/events.yaml`** was found in step 1.

- **Load** the existing YAML.
- For each `event_type` / model:
  - **New** `event_type` → append a new **`models.<event_type>`** block.
  - **Existing** model → **merge fields**: add new keys; for changed types, prefer updating
    descriptions to document evolution; avoid silently narrowing types without user confirmation.
- Bump **`info.version`** semver appropriately (patch for additive fields, minor for new event
  types—match team practice).

### 4. Contract skeleton (Kafka + JSON)

Follow CLI expectations for [Kafka](https://cli.datacontract.com/#test): `servers.*.type: kafka`,
`format: json`, `topic`, `host`. Models use `type: table` in line with CLI examples (event
payload treated as tabular row shape).

Minimal shape (adapt `id`, `title`, `owner`, server, and models):

```yaml
dataContractSpecification: 0.9.3
id: urn:datacontract:<service>-events
info:
  title: <service> events
  version: 1.0.0
  description: |
    Data contract for <service> Kafka events (JSON).
  owner: <team-or-service>
servers:
  production:
    type: kafka
    host: <broker-host:9092>
    topic: <topic-name>
    format: json
models:
  "<event_type_string_exactly>":
    description: <what this event means>
    type: table
    fields:
      <field_name>:
        type: <odcs-type>
        description: <clear sentence>
        required: true|false
        example: "<literal>"
```

Use quoted YAML keys for model names if they contain characters that YAML could misparse (e.g.
dots are usually fine unquoted in practice—quote if needed).

### 5. Quality and validation

- **Lint via Docker** (do **not** rely on a local `datacontract` binary). From the **repository
  root** (so the contract path resolves correctly inside the container):

```bash
DATACONTRACT_FILE_LOCATION="datacontracts/events/events.yaml"

docker run --rm --name contract-cli \
  -v "${PWD}:/app" \
  -w /app \
  datacontract/cli:snapshot-latest \
  lint \
  "${DATACONTRACT_FILE_LOCATION}"
```

If the contract lives at a different path, set `DATACONTRACT_FILE_LOCATION` to that path
**relative to the repo root** (the volume mounts `${PWD}` at `/app` and `-w /app` is the workdir).

Requires Docker available; image `datacontract/cli:snapshot-latest` must be pullable.

- Ensure every model has a **`description`** and each field has **`type`** and **`description`**.
- Add **`example`** values taken from or consistent with samples.

### 6. Cross-skill boundary

- **Database / postgres** contracts → **build-data-contract** (`datacontracts/dbs/postgresql.yaml`).
- **Events / Kafka / `events.yaml`** → this skill.

---

## Checklist before finishing

- [ ] If schema inference or merge required new/updated fields or models, **sample JSON came
      from the user’s prompt or their reply after you asked** — not from an unsolicited repo
      search (or explicitly waived per step 0).
- [ ] Output path is **`datacontracts/events/events.yaml`** (or an explicit alternate path only
      if the user required it).
- [ ] If that file existed before this task, it was **updated in place**, not replaced by a new
      file elsewhere.
- [ ] **`parse_event_samples.py`** was run on the sample inputs and the contract reflects its
      grouped **`event_type`** → fields output (then enriched).
- [ ] Every distinct `event_type` in samples has a **`models`** entry named exactly that string.
- [ ] Field types and nested objects match samples; optional keys documented when absent in some
      samples.
- [ ] Existing file merged without dropping unrelated models unless the user asked to remove them.
- [ ] Docker **`datacontract/cli:snapshot-latest` `lint`** passes for the target YAML (step 5).
- [ ] `info.version` updated when the contract changed.
