# BPMN Shape Catalogue (Camunda 7, LLM)

Use this guide to select BPMN shapes in Camunda 7.

## Events

- Start: None, Message, Timer (use others only if requested).
- End: None, Error, Message (use only if supported by scenario).
- Boundary events: Timer and Error are common; attach only to tasks/subprocesses.

## Tasks

- User Task for human work.
- Service Task for system work.
- Manual Task for offline work.

## Gateways

- XOR for decisions.
- AND for parallel paths.
- Avoid OR unless explicitly required.

## Subprocesses

- Use collapsed subprocess to hide details.
- Use expanded only when internal flow is provided.
