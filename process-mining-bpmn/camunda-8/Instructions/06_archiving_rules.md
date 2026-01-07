# Project Wrap-Up and Archiving Instructions

Use these steps after the user confirms there are no further process modeling requests.

---

1. **Confirm completion**  
   Ask the user to confirm no more BPMN updates are needed for the current theme/project.

2. **Name the archive folder**  
   Build a folder name using the project/theme plus timestamp, e.g., `customer-onboarding_20250314-1530`.  
   Use `YYYYMMDD-HHMM` in 24h UTC unless the user specifies another timezone.  
   If the user starts a new project, explicitly ask for the new folder name before proceeding.

3. **Create the archive folder**  
   Create the folder at the current workspace root (or a user-specified path). Do not overwrite existing folders; if the name exists, append a short suffix (e.g., `_v2`).

4. **Move BPMN assets**  
   Move all BPMN diagrams (`*.bpmn` and related XML files) for the finished project into the archive folder.  
   Preserve relative substructure if applicable. Do not move artifacts from other active projects.

5. **Add a recap README**  
   Create `README.md` inside the archive folder summarizing:
   - Project/theme name
   - Date/time of archiving (UTC unless otherwise requested)
   - List of BPMN files archived
   - Brief recap of the user’s requests and modeling decisions (gateways used, lanes, special events, executable vs. non-executable)

6. **Optional extras**  
   If provided during the session, include any validation notes, open questions, or follow-up tasks in the README.

7. **Confirm handoff**  
   Inform the user that files were archived and provide the folder name/path. If a new project begins, ask for the folder name before generating new diagrams.

---

## Pseudo-flow (Agent Logic)

- Ask: "Any more process changes for this project?"  
  - If no → proceed to archive.  
  - If yes → continue modeling.

- Ask (for new project only): "What folder name should I use for the new project?"  
  - If none given, propose `<theme>_YYYYMMDD-HHMM`.

- Create archive folder → move BPMN files → generate README with recap → confirm completion.
