
# BPMN 2.0 Structural Grammar (LLM Guidance)

## 1. XML Hierarchy
- <bpmn:definitions>
  - <bpmn:process> OR <bpmn:collaboration>
  - <bpmndi:BPMNDiagram>
    - <bpmndi:BPMNPlane>

## 2. Process Allowed Children
startEvent, endEvent, intermediateCatchEvent, intermediateThrowEvent,
task, userTask, serviceTask, manualTask, sendTask, receiveTask,
exclusiveGateway, parallelGateway, eventBasedGateway,
sequenceFlow, boundaryEvent, subprocess, callActivity, laneSet.

## 3. BPMNShape Grammar
Each flow node MUST have:
```
<bpmndi:BPMNShape id="Shape_[ID]" bpmnElement="[ID]">
  <dc:Bounds x="[int]" y="[int]" width="[int]" height="[int]"/>
</bpmndi:BPMNShape>
```

## 4. BPMNEdge Grammar
Each flow MUST have:
```
<bpmndi:BPMNEdge id="Edge_[FLOW_ID]" bpmnElement="[FLOW_ID]">
  <di:waypoint x="[int]" y="[int]"/>
  <di:waypoint x="[int]" y="[int]"/>
</bpmndi:BPMNEdge>
```
