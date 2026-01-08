# Domain Templates (PlantUML)

## Simple Approval

start
:Submit;
:Review;
if (Approved?) then (yes)
  :Approve;
else (no)
  :Reject;
endif
stop
