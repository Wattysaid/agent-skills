# Camunda 8 BPMN Shape Catalogue (Formal Documentation Format)

This document provides a formal definition of BPMN 2.0 symbols as supported by **Camunda 8**, including execution coverage and modelling constraints for processes, collaborations, and subprocesses.

It serves as an authoritative reference for process model authors producing executable or illustrative diagrams in Camunda 8 Modeler or Web Modeler.

---

## 1. Participants

### 1.1 Pool (Participant)
A pool represents a participant in a collaboration. Pools may contain a single process.  
Camunda requires a pool when modelling message flows between participants.

### 1.2 Lane
A lane partitions a pool for organisational clarity. Lanes do not alter process execution semantics.

### 1.3 Collaboration
When multiple pools are present, the BPMNPlane must reference the Collaboration element.  
Message flows must be defined between pools only.

---

## 2. Events

Camunda 8 supports a subset of BPMN 2.0 events for execution. All other event types may be used for documentation but will not execute.

### 2.1 Start Events

| Type                     | Executable |
|--------------------------|------------|
| None                     | Yes        |
| Message                  | Yes        |
| Timer                    | Yes        |
| Signal                   | No         |
| Conditional              | No         |
| Multiple / Parallel Mult | No         |

The following start events are invalid in BPMN and cannot be used: Error, Escalation, Compensation, Cancel, Terminate.

---

### 2.2 Intermediate Catch Events

| Type         | Executable |
|--------------|------------|
| Message      | Yes        |
| Timer        | Yes        |
| Signal       | No         |
| Conditional  | No         |
| Link         | No         |
| Escalation   | No         |
| Compensation | No         |

Link events must not cross pools.

---

### 2.3 Intermediate Throw Events

Camunda 8 supports throwing of messages for executable processes.  
All other throwing event types are illustrative only.

---

### 2.4 Boundary Events

| Type         | Executable |
|--------------|------------|
| Timer        | Yes        |
| Message      | Yes        |
| Error        | Yes        |
| Signal       | No         |
| Conditional  | No         |
| Escalation   | No         |
| Compensation | No         |

Boundary events may be interrupting or non-interrupting (`cancelActivity="false"`).

---

### 2.5 End Events

| Type         | Executable |
|--------------|------------|
| None         | Yes        |
| Message      | Yes        |
| Error        | Yes        |
| Terminate    | Yes        |
| Signal       | No         |
| Escalation   | No         |
| Compensation | No         |
| Cancel       | No (only valid inside Transaction Subprocess) |

---

## 3. Activities

### 3.1 Tasks

| Task Type        | Executable |
|------------------|------------|
| User Task        | Yes        |
| Service Task     | Yes        |
| Receive Task     | Yes        |
| Send Task        | Yes        |
| Manual Task      | No         |
| Business Rule Task | Limited  |
| Script Task      | No         |

Multi-instance markers are executable for User and Service tasks.

---

## 4. Subprocesses

| Type                    | Executable |
|-------------------------|------------|
| Embedded Subprocess     | Yes        |
| Collapsed Subprocess    | Yes        |
| Event Subprocess        | Yes        |
| Call Activity           | Yes        |
| Transaction Subprocess  | No         |
| Ad-hoc Subprocess       | No         |

---

## 5. Gateways

| Gateway          | Executable |
|------------------|------------|
| Exclusive (XOR)  | Yes        |
| Parallel (AND)   | Yes        |
| Event-Based      | Yes        |
| Inclusive (OR)   | No         |
| Complex          | No         |

Modelling constraints:
- Exclusive split gateways must have ≥2 outgoing flows; exclusive merges may have a single outgoing flow.
- Complex gateways are reserved for multi-branch scenarios (>2 branches). Complex splits must have >2 outgoing flows; complex merges must have >2 incoming flows and a single outgoing flow.

---

## 6. Flows

### 6.1 Sequence Flow
Sequence flows connect flow nodes within a process.  
Camunda supports conditional expressions on outgoing flows from XOR gateways (and, illustratively, inclusive gateways).

### 6.2 Message Flow
Message flows may only connect pools, not nodes within the same pool.

### 6.3 Associations
Associations connect artefacts, annotations, or compensation handlers. They are non-executable.

---

## 7. Artefacts

- Text Annotations  
- Groups  
- Data Objects  
- Data Stores  

These elements are non-executable and serve documentation purposes only.

---

## 8. Camunda 8 Execution Support Overview

Camunda 8 executes the following BPMN elements:

### Start Events
- None  
- Message  
- Timer  

### Intermediate Events
- Message Catch  
- Timer Catch  

### Boundary Events
- Message  
- Timer  
- Error  

### Activities
- User Task  
- Service Task  
- Send Task  
- Receive Task  
- Subprocess  
- Call Activity  
- Event Subprocess  

### End Events
- None  
- Message  
- Error  
- Terminate  

All other BPMN symbols may be modelled for visual clarity but will not be executed by Camunda 8.
