# Mermaid Cross-Functional Syntax Overrides

Apply these rules in addition to `mermaid-cross-functional/REFERENCE.md`.

## Flowchart Conventions

- Default direction: `flowchart LR` unless the user requests otherwise.
- Use `subgraph` per lane; keep lane labels short and unique.
- Use `{}` nodes for gateways and label edges for decisions.

## Label Safety

- Avoid using the lowercase word `end` as a node label.
- Keep labels short; split long labels across nodes rather than multi-line text.

## Best Practices

- Keep lane names short and consistent.
- Label decision outputs (`Yes`/`No`) on edges.

## Sources (GitHub)

- Mermaid flowchart syntax: https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/flowchart.md
