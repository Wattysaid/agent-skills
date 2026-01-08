
# BPMN Error Catalogue & Fix Recipes

## Missing BPMNShape
Fix:
1. Create <bpmndi:BPMNShape id="Shape_[NODE]">
2. Add Bounds.

## Missing BPMNEdge
Fix:
1. Create <bpmndi:BPMNEdge id="Edge_[FLOW]">
2. Add two+ waypoints.
