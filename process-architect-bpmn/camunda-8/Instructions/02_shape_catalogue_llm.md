# Ultimate BPMN 2.0 Shape Catalogue (LLM-Optimised for Camunda 8 Modelling)

A merged and enhanced reference catalogue of all BPMN 2.0 shapes, events, activities, gateways, flows, and artefacts, optimised for LLMs generating **non-executable** and **executable** process diagrams in **Camunda 8 Modeler**.

This document provides:
- Full BPMN 2.0 symbol catalogue  
- Precise definitions and usage rules  
- Camunda 8 execution support vs illustrative-only notation  
- Modelling constraints for pools, lanes, sequence/message flows, and DI  
- Best-practice conventions for enterprise-grade modelling  

---

## 1. Participants (Pools, Lanes, Collaboration)

### 1.1 Pool (Participant)
- Container for a process or actor.
- Required when modelling interactions.
- Can represent organisations, systems, or roles.
- For single-process diagrams: provide one pool referencing the main process.

**LLM Rules:**  
- A pool must contain exactly one process.  
- Message flows can connect pools; sequence flows cannot cross pools.

**Camunda Execution Support:** Executable (pools are notation-only but required structurally).

---

### 1.2 Lane
- Subdivision of a pool representing roles, teams, systems, departments.
- Purely organisational — does NOT affect execution semantics.

**LLM Rules:**
- All flow nodes must remain within lane bounds.
- Each lane must list all `bpmn:flowNodeRef` values for the node IDs it contains.
- A node must appear in exactly one lane.
- If lanes become visually crowded, use separate pools instead.

**Camunda Execution Support:** Not relevant; lanes do not affect execution semantics.

---

### 1.3 Collaboration & BPMNPlane Rules
- When using multiple pools, the diagram must use a **Collaboration** element (`<bpmn:collaboration>`).
- When pools are present, set:  
  `bpmndi:BPMNPlane@bpmnElement="[COLLABORATION_ID]"`.
- Participants (`<bpmn:participant>`) must reference existing process IDs via `processRef`.

---

## 2. Events Overview

Events represent something that **happens** during a process lifecycle.  
They may be **Start**, **Intermediate**, or **End** events.  
Events can be **Interrupting** or **Non-interrupting** when placed on boundaries.

### 2.1 Supported BPMN Event Types
- None  
- Message  
- Timer  
- Signal  
- Conditional  
- Escalation  
- Link  
- Error  
- Cancel  
- Compensation  
- Multiple  
- Parallel Multiple  
- Terminate  

Each type has restrictions on where it may appear (start, intermediate, boundary, end).

---

## 3. Start Events

### 3.1 Supported Start Event Types

| Event Type           | Description                                | Camunda Execution |
|----------------------|--------------------------------------------|-------------------|
| **None**             | Immediate start                            | ✔️                |
| **Message**          | Waits for incoming message                 | ✔️                |
| **Timer**            | Date/time/cycle trigger                    | ✔️                |
| **Signal**           | Global broadcast start                     | Illustrative      |
| **Conditional**      | Starts when condition becomes true         | Illustrative      |
| **Multiple**         | Starts when any configured event fires     | Illustrative      |
| **Parallel Multiple**| Starts when all configured events fire     | Illustrative      |

### 3.2 Invalid Start Events
The following must **never** be used as start events:
- Error  
- Escalation  
- Compensation  
- Terminate  
- Cancel  

**LLM Rule:** Never emit these event definitions within `<bpmn:startEvent>`.

---

## 4. Intermediate Events (Catching)

Intermediate catching events wait for something to occur during the process.

### 4.1 Catching Event Types

| Type                   | Behaviour                                         | Camunda Execution |
|------------------------|---------------------------------------------------|-------------------|
| **Timer**              | Waits/delays flow                                 | ✔️                |
| **Message**            | Waits for message                                 | ✔️                |
| **Signal**             | Listens for broadcast                             | Illustrative      |
| **Conditional**        | Waits for condition                               | Illustrative      |
| **Link (Catch)**       | Target for Throw Link in same process             | Illustrative      |
| **Escalation (Catch)** | Waits for escalation                              | Illustrative      |
| **Compensation**       | Waits for compensation trigger                    | Illustrative      |
| **Multiple**           | Waits for one of several configured events (OR)   | Illustrative      |
| **Parallel Multiple**  | Waits for all configured events (AND)             | Illustrative      |

**LLM Rules:**
- Link events must not cross pools. They only connect parts of the **same process**.
- Use Multiple/Parallel Multiple only when you need compact notation of alternative/combined triggers.

---

## 5. Intermediate Events (Throwing)

Intermediate throwing events signal something outward or redirect flow via a link.

### 5.1 Throwing Event Types

| Type                      | Behaviour                                             | Camunda Execution |
|---------------------------|-------------------------------------------------------|-------------------|
| **Link (Throw)**          | Jumps to matching Link Catch event                    | Illustrative      |
| **Message (Throw)**       | Sends a message                                       | Partially         |
| **Escalation (Throw)**    | Throws escalation                                     | Illustrative      |
| **Signal (Throw)**        | Broadcast signal                                      | Illustrative      |
| **Multiple / Parallel**   | Throws all configured events                          | Illustrative      |

**Camunda Execution Note:**  
Only message throws / send tasks can map cleanly to executable semantics. Others are notation-only in Camunda 8.

**LLM Rules:**
- A Throw Link must have a matching Catch Link with the same name inside the same process.
- Avoid excessive use of Link events; use them for long jumps that would otherwise create crossing flows.

---

## 6. Boundary Events

Boundary events attach to activities (tasks or subprocesses) and alter behaviour when they fire.

### 6.1 Supported Boundary Event Types

| Type           | Camunda Execution | Notes                                             |
|----------------|-------------------|---------------------------------------------------|
| **Timer**      | ✔️                | Interrupting or non-interrupting                 |
| **Message**    | ✔️                | Interrupting or non-interrupting                 |
| **Error**      | ✔️                | Only on subprocess/call activity scopes          |
| **Signal**     | Illustrative      | Non-executable in Camunda 8                      |
| **Conditional**| Illustrative      | Non-executable in Camunda 8                      |
| **Escalation** | Illustrative      | Non-executable in Camunda 8                      |
| **Compensation**| Illustrative     | Used to mark compensation handlers               |

### 6.2 Interrupting vs. Non-interrupting
- **Interrupting**: `cancelActivity="true"` (solid border)
- **Non-interrupting**: `cancelActivity="false"` (dashed border)

**LLM Rules:**
- Place boundary events so that their bounds touch the activity’s bounds.
- Use non-interrupting boundaries for “side actions” that should not cancel the main activity.

---

## 7. End Events

End events indicate how a process or subprocess finishes.

### 7.1 End Event Types

| Type         | Behaviour                                       | Camunda Execution |
|--------------|-------------------------------------------------|-------------------|
| **None**     | Normal termination                              | ✔️                |
| **Message**  | Send message on completion                      | ✔️                |
| **Error**    | Propagate error to parent scope                 | ✔️                |
| **Terminate**| Kill all tokens in the current scope            | ✔️                |
| **Signal**   | Broadcast a signal                              | Illustrative      |
| **Escalation**| Raise escalation                               | Illustrative      |
| **Compensation**| Trigger compensation                         | Illustrative      |
| **Cancel**   | Used only inside Transaction Subprocess         | Illustrative      |

**LLM Rules:**
- Use **Terminate End** sparingly; it ends all current paths within the scope.
- Use **Error End** inside subprocesses or call activities when you want a boundary error handler to catch it.

---

## 8. Activities (Tasks & Subprocesses)

### 8.1 Task Types

| Task Type           | Behaviour                                     | Camunda Execution |
|---------------------|-----------------------------------------------|-------------------|
| **User Task**       | Human work item                               | ✔️                |
| **Service Task**    | Automated service / worker job                | ✔️                |
| **Send Task**       | Fire-and-forget message                       | ✔️                |
| **Receive Task**    | Waits for message                             | ✔️                |
| **Manual Task**     | Manual work, not managed by engine            | Illustrative      |
| **Business Rule Task** | Calls decision/DMN logic (limited exec)   | Partially         |
| **Script Task**     | Inline script                                 | Illustrative      |

### 8.2 Task Markers

- **Loop**: `standardLoopCharacteristics`. Sequential repetition; illustrative in Camunda 8.
- **Multi-instance**: `<bpmn:multiInstanceLoopCharacteristics>`  
  - `isSequential="true"` → sequential multi-instance  
  - `isSequential="false"` → parallel multi-instance  
- **Compensation Marker**: Marks an activity as a compensation handler (illustrative).

**LLM Rules:**
- Prefer multi-instance rather than loop markers for Camunda 8 semantics.
- Only apply multi-instance where repeating logic across items/instances is explicitly needed.

---

## 9. Subprocesses & Call Activities

### 9.1 Subprocess Types

| Type                        | Description                                        | Executable |
|-----------------------------|----------------------------------------------------|-----------|
| **Embedded Subprocess**     | Expanded; contains internal flow                   | ✔️        |
| **Collapsed Subprocess**    | References internal flow not shown in diagram      | ✔️        |
| **Event Subprocess**        | Triggered by start event inside parent process     | ✔️        |
| **Call Activity**           | Reuses separate process/decision via `calledElement` | ✔️      |
| **Transaction Subprocess**  | Transaction semantics                              | Illustrative |
| **Ad-hoc Subprocess**       | Unordered activities, ad-hoc behaviour             | Illustrative |

**LLM Rules:**
- Expanded subprocess: include internal nodes + flows + shapes.
- Collapsed subprocess: do not include internal nodes in same diagram file.
- Event subprocess: must not have incoming/outgoing sequence flows; it starts with an event.

---

## 10. Gateways

Gateways control branching and joining of flows.

### 10.1 Gateway Support Matrix

| Gateway             | Description                              | Camunda Execution |
|---------------------|------------------------------------------|-------------------|
| **Exclusive (XOR)** | Exactly one outgoing path taken          | ✔️                |
| **Parallel (AND)**  | All outgoing paths taken                 | ✔️                |
| **Event-Based**     | Race between following events/receives   | ✔️                |
| **Inclusive (OR)**  | One or more outgoing paths taken         | Illustrative      |
| **Complex**         | Custom combination of conditions         | Illustrative      |

**LLM Rules:**
- For XOR decisions, label the gateway with a **question** and outgoing flows with **answers** (conditions).
- XOR split gateways must have ≥2 outgoing flows; XOR merge gateways may have a single outgoing flow.
- For Parallel, ensure all branches either rejoin or end independently.
- For Event-Based, only connect to catching events or receive tasks; do not add conditions on outgoing flows.
- Use Complex gateways only for multi-branch scenarios (>2 branches). Complex splits must have >2 outgoing flows; complex merges must have >2 incoming flows and a single outgoing flow.

---

## 11. Flows

### 11.1 Sequence Flow
- Connects flow nodes (events, activities, gateways).
- Allowed source/target: start → task/event/gateway; task → task/gateway/event; gateway → tasks/events/gateways; etc.
- May have `conditionExpression` when leaving XOR or Inclusive gateways.

**LLM Rules:**
- Do not place conditions on flows leaving event-based gateways.
- Do not create sequence flows across pools.

---

### 11.2 Message Flow
- Used only in collaborations between pools.
- Represents communication between participants.
- Cannot originate and terminate inside the same pool.

**LLM Rules:**
- A message flow must connect elements in different pools.
- Do not attach message flows to sequence flow objects.

---

### 11.3 Association
- Dashed line linking artefacts, annotations, and sometimes data objects.
- Direction can be none, one-way, or both ways.

**LLM Rules:**
- Use associations for documentation only; never for control flow.
- For compensation markers, association direction can matter.

---

## 12. Data & Artefacts

### 12.1 Data Objects
- Represent transient data used or produced by tasks.

### 12.2 Data Stores
- Represent persistent data.

### 12.3 Groups
- Visual grouping only; no execution semantic.

### 12.4 Text Annotations
- Free-text notes explaining parts of the diagram.

**LLM Rules:**
- Always add DI shapes for data objects/stores and annotations if you include them.

---

## 13. Camunda 8 Execution Coverage (“Green Path”)

Executable elements supported in Camunda 8:

### 13.1 Start Events
- None  
- Message  
- Timer  

### 13.2 Intermediate Catching
- Message  
- Timer  

### 13.3 Boundary Events
- Message  
- Timer  
- Error  

### 13.4 Activities
- User Task  
- Service Task  
- Receive Task  
- Send Task  

### 13.5 Subprocesses
- Embedded Subprocess  
- Event Subprocess  
- Call Activity  

### 13.6 End Events
- None  
- Message  
- Error  
- Terminate  

All other BPMN shapes are allowed for **modelling** (illustrative) but will not be executed by Camunda 8.

Use this “green path” as the basis when the user requests an **executable** process.
