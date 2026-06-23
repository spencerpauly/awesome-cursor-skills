---
name: database-migration
description: Create and manage database migrations using goose, generating complete migration files following best practices for schema changes, data transformations, and zero-downtime deployments. Use when creating database migrations, schema changes, or data transformations.
---

# Database Migration

Create safe, reversible database migrations with goose framework.

## Migration Process

### 1. Migration Analysis

- Review current database schema changes needed
- Identify data transformation requirements
- Check for potential data loss or corruption risks
- Analyze performance impact of schema changes
- Consider index changes and their impact

### 2. Migration Script Generation

- Create up and down migration scripts (goose format)
- Include proper indexing and constraint management
- Add data migration logic where needed
- Implement rollback procedures

### 3. Best Practices

- Ensure migrations are atomic and reversible
- Add proper error handling and validation
- Include progress monitoring for large datasets
- Consider zero-downtime deployment strategies
- Handle NULL values and default constraints properly

### 4. Testing Strategy

- Create test data scenarios
- Verify migration on staging environment
- Plan rollback procedures and testing
- Document deployment steps and timing

## Output Format

1. **Analysis**: Risks, performance impact, data transformation requirements
2. **Migration Up Script**: Complete goose up migration
3. **Migration Down Script**: Complete goose rollback script
4. **Deployment Steps**: Step-by-step deployment guide

## Example (goose format)

```sql
-- +goose Up
-- +goose StatementBegin
ALTER TABLE orders ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'pending';
CREATE INDEX idx_orders_status ON orders(status);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP INDEX IF EXISTS idx_orders_status;
ALTER TABLE orders DROP COLUMN status;
-- +goose StatementEnd
```

## Checklist

- [ ] Reviewed schema changes and data transformation requirements
- [ ] Checked for potential data loss or corruption risks
- [ ] Created up and down migration scripts
- [ ] Included proper indexing and constraint management
- [ ] Ensured migrations are atomic and reversible
- [ ] Added error handling and validation
- [ ] Created test data scenarios
- [ ] Verified migration on staging environment
- [ ] Documented deployment steps and timing
