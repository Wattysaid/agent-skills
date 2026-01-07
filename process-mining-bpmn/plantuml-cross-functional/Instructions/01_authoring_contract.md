# PlantUML Authoring Contract

Use this contract for every response that returns PlantUML code.

## Output Envelope

- Use PlantUML activity diagram syntax.
- Use swimlanes with `|Lane Name|`.
- Save the diagram to a `.puml` file and return its path.

## Structural Rules

- Use `start` and `stop`.
- Each decision uses `if/then/else`.
- Keep the flow top-to-bottom unless requested otherwise.
