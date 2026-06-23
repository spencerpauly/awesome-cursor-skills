# JSON sample → ODCS logical types

Use these mappings when inferring `type` for event payload fields. Prefer logical types from the [Open Data Contract Standard](https://cli.datacontract.com/) conventions used by `datacontract-cli`.

| JSON value shape | ODCS `type` | Notes |
|------------------|-------------|--------|
| string (ISO 8601 date only) | `date` | If clearly a calendar date |
| string (ISO 8601 datetime) | `timestamp` or `timestamptz` | Use `timestamptz` if timezone or `Z` is present |
| string (UUID) | `string` | Add `format: uuid` in `config` if your contract style supports it |
| string (enum-sized set) | `string` | Add `enum: [...]` when samples show a closed set |
| string (free text) | `string` | Default |
| number (integer) | `integer` | |
| number (float) | `number` | |
| boolean | `boolean` | |
| null in samples | make field optional / nullable per contract style | Document in `description` |
| array of strings | `array` with `items: { type: string }` | |
| array of objects | `array` with `items: { type: object, fields: { ... } }` | |
| nested object | `object` with `fields:` | Recurse for each nested key |

**`event_type`:** The **model name** in `models:` must equal the `event_type` string for that event. Do not rename models to snake_case if the wire format uses dotted names (e.g. `identity.user.created`).
