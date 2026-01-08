
# Forbidden BPMN Patterns

❌ Sequence flows pointing left  
❌ Gateways with only one outgoing path  
❌ Complex gateways used for two-way decisions (use XOR instead)  
❌ Orphan nodes  
❌ Start → End with no activity  
❌ Pools without lanes  
❌ Link events across pools  
❌ Boundary events not touching activity  
❌ Boundary-event exception paths that rejoin the main flow without a terminating end event or a dedicated collapsed subprocess  
❌ Collapsed subprocesses sized larger than standard task size  
