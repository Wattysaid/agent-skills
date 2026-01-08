# Camunda 8 Syntax Overrides

Apply these rules in addition to `camunda-8/REFERENCE.md`.

## BPMN XML Constraints

- Output BPMN 2.0 XML intended for Camunda 8 execution.
- Do not use Camunda 7 `camunda:` extensions unless explicitly requested.
- Only add `zeebe:` extensions if the user provides worker or variable mappings.

## Naming and IDs

- Use stable, readable IDs without spaces.
- Keep labels concise and verb-led.

## Best Practices

- Default to `isExecutable="false"` unless automation is requested.
- Keep pools/lanes for ownership clarity; avoid crossing sequence flows.

## Sources (GitHub)

- Camunda 8 docs: https://github.com/camunda/camunda-docs
