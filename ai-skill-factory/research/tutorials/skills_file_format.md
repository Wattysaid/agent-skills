# Skill File Formats and Best Practices

## Goals of a Skill
- Reusability
- Predictable activation
- Safe execution

## Mandatory Elements
- Name
- Description
- Trigger conditions
- Step sequence

## Optional Elements
- Example commands
- Validation checks
- Rollback instructions

## Versioning
Use semantic or consulting-style versioning:
- R1.00
- R1.01
- R2.00

## Documentation Tips
- Avoid vague language
- Prefer imperative verbs
- Include file paths

## Security
- Never auto-run destructive commands
- Require confirmations for deletes or deployments
