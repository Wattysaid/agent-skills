# Camunda 7 BPMN Support Matrix (Compact)

## Start Events

- None: executable
- Message: executable
- Timer: executable
- Signal: use for documentation unless explicitly requested

## Tasks

- User Task: executable
- Service Task: executable (requires implementation details if automated)
- Manual Task: documentation

## Gateways

- Exclusive: executable
- Parallel: executable
- Event-Based: only if events are provided
