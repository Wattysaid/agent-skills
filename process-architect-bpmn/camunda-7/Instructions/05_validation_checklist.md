# Validation Checklist (Camunda 7)

- XML well-formed; all IDs unique.
- Start -> End connectivity for all paths.
- Gateways split and merge properly.
- All nodes appear in a lane and have DI shapes.
- All flows have DI edges and valid waypoints.
- No sequence flow crosses pools.
