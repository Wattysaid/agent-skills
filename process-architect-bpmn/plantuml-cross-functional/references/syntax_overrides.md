# PlantUML Cross-Functional Syntax Overrides

Apply these rules in addition to `plantuml-cross-functional/REFERENCE.md`.

## Activity Conventions

- Use `@startuml` / `@enduml`.
- Use `start` / `stop` for boundaries.
- Use `|Lane Name|` for swimlanes.
- Use `if/then/else` for gateways.

## Label Safety

- Keep lane names concise; avoid punctuation that could be parsed as syntax.

## Best Practices

- Keep `if/then/else` blocks shallow; avoid deep nesting.
- Keep lane switches minimal to reduce crossing flows.

## Sources

- PlantUML activity diagram syntax: https://plantuml.com/activity-diagram-beta
