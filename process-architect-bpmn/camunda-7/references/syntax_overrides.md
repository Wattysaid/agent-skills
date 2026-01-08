# Camunda 7 Syntax Overrides

Apply these rules in addition to `camunda-7/REFERENCE.md`.

## BPMN XML Constraints

- Output BPMN 2.0 XML intended for Camunda 7 execution.
- Do not use Camunda 8 `zeebe:` extensions.
- Only add `camunda:` extensions (e.g., `camunda:formKey`, task listeners) if explicitly requested.

## Naming and IDs

- Use stable, readable IDs without spaces.
- Keep labels concise and verb-led.

## Best Practices

- Default to `isExecutable="false"` unless automation is requested.
- Keep pools/lanes for ownership clarity; avoid crossing sequence flows.

## Sources (GitHub)

- Camunda 7 docs: https://github.com/camunda/camunda-docs-manual
