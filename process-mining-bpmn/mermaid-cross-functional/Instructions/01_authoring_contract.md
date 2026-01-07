# Mermaid Authoring Contract

Use this contract for every response that returns Mermaid code.

## Output Envelope

- Produce Mermaid `flowchart` syntax.
- Represent lanes with `subgraph` blocks.
- Save the diagram to a `.mmd` file and return its path.

## File Output

- Always create a `.mmd` file with a descriptive name.
- Provide the file path in the response.

## Structural Rules

- One clear start and end node.
- Every node is connected.
- Gateways use `{}` nodes with labeled edges.
