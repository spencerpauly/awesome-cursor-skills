# PostgreSQL → Data Contract Spec Type Mappings

Use these mappings when reviewing or enriching the skeleton YAML produced by `parse_migrations.py`.
The script applies them automatically; this reference helps when you need to override or understand a type.

## Scalar Types

| PostgreSQL type            | Data Contract type | Notes |
|----------------------------|--------------------|-------|
| `bigserial`, `serial8`     | `bigint`           | Auto-increment PK |
| `serial`, `serial4`        | `int`              | |
| `smallserial`, `serial2`   | `int`              | |
| `bigint`, `int8`           | `bigint`           | |
| `integer`, `int`, `int4`   | `int`              | |
| `smallint`, `int2`         | `int`              | |
| `real`, `float4`           | `float`            | |
| `double precision`, `float8` | `double`         | |
| `numeric`, `decimal`       | `decimal`          | |
| `text`                     | `text`             | |
| `varchar(N)`, `character varying(N)` | `varchar` | Add `maxLen: N` to preserve the length constraint |
| `varchar`, `character varying` (no length) | `text` | No length constraint to preserve |
| `char(N)`, `character(N)` | `varchar`          | Add `maxLen: N` |
| `char`, `character` (no length) | `text`        | |
| `bytea`                    | `bytes`            | Used for MongoDB ObjectIDs |
| `boolean`, `bool`          | `boolean`          | |
| `timestamp` / `timestamp without time zone` | `timestamp_ntz` | Always UTC in JumpCloud services |
| `timestamptz` / `timestamp with time zone`  | `timestamp_tz`  | |
| `date`                     | `date`             | |
| `time`                     | `time`             | |
| `json`, `jsonb`            | `object`           | Add `fields:` sub-mapping for known keys |
| `uuid`                     | `text`             | |
| `inet`, `cidr`, `macaddr`  | `text`             | |

## Special Types

| PostgreSQL type     | Data Contract type | Extra YAML |
|---------------------|--------------------|------------|
| `VARCHAR[]`, `TEXT[]`, any `[]` | `array` | Add `config: { postgresType: array }` and `items: { type: text }` |
| `USER-DEFINED` enum | `text`             | Add `config: { postgresType: USER-DEFINED }` and `enum:` list |

## Classification Guidelines

Always set `classification` on every field. Default to `level3` unless a field contains PII:

| Classification | When to use |
|----------------|-------------|
| `level2`       | Email addresses, user display names, IP addresses |
| `level3`       | Internal IDs, object IDs, timestamps, status flags, config blobs |
| `level1`       | Passwords, secrets, PII like SSN — rare in these services |

Fields that typically get `level2`:
- `created_by` (email)
- `last_updated_by` (email)
- Any column named `email`, `user_email`, `admin_email`

## Object Fields (`jsonb` / `json`)

For `jsonb` columns where you know the structure, expand under `fields:`:

```yaml
filters:
  type: object
  description: JSON object containing filter criteria
  classification: level3
  fields:
    some_key:
      type: string
      description: ...
      classification: level3
      example: 'value'
```

If the JSONB schema is unknown or highly dynamic, leave `fields: {}` and note it in the description.

## Array Fields

```yaml
reference_fields:
  type: array
  config:
    postgresType: array
  items:
    type: string
  description: Array of field name paths
  classification: level3
  example: '["resource.id", "organization"]'
```

## Example Values

Good example values help data consumers understand the data:
- `bytes` fields (MongoDB ObjectIDs): `'\x671766674dd4bd0001ec87e1'`
- `timestamp_ntz`: `'2024-10-07 12:10:46.531157'`
- `bigint` PKs: `'1'`
- `boolean`: `'true'` or `'false'`
- `text` status enums: use the actual enum value string
- Email fields: `'user@jumpcloud.com'`
